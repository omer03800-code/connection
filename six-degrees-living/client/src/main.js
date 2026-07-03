// Main entry point - wire everything together
import { createRenderer } from './viz/renderer.js';
import { createNodesGeometry } from './viz/nodes.js';
import { createArmsForNode, animateArms } from './viz/arms.js';
import { setupCamera } from './viz/camera.js';
import { createEdgesGroup, addConnectionEdge, setEdgesVisibility } from './viz/edges.js';
import { createLabelsGroup, setLabelsVisibility } from './viz/labels.js';
import { getGraph } from './api.js';
import { updateState, setZoomLevel, selectPerson, clearSelection, search, getNeighbors } from './state.js';

let scene, camera, renderer, controls;
let masterGroup, nodesPoints, edgesGroup, labelsGroup, armsGroups;
let animationId;

async function init() {
  // Fetch graph data
  const { people, connections } = await getGraph();
  updateState({ people, connections });

  // Initialize Three.js
  const container = document.getElementById('visualization');
  const { scene: s, camera: c, renderer: r } = createRenderer(container);
  scene = s;
  camera = c;
  renderer = r;

  // Setup camera state machine
  const camManager = setupCamera(camera, renderer.domElement);

  // Create master group for auto-rotation
  masterGroup = new THREE.Group();
  scene.add(masterGroup);

  // Initialize data positions with D3 force simulation
  const simulation = d3.forceSimulation(people)
    .force('charge', d3.forceManyBody().strength(-500))
    .force('link', d3.forceLink(connections)
      .id(d => d.id)
      .distance(150))
    .force('collide', d3.forceCollide(80))
    .alpha(1)
    .alphaDecay(0.02);

  // Pre-tick simulation to settle nodes
  for (let i = 0; i < 200; i++) {
    simulation.tick();
  }

  // Convert D3 positions to Three.js
  people.forEach(person => {
    person.pos = new THREE.Vector3(person.x || 0, person.y || 0, (person.z || 0) * 2);
  });

  // Create nodes
  const { points: nodesPoints } = createNodesGeometry(people);
  masterGroup.add(nodesPoints);

  // Create arms for each node
  armsGroups = new Map();
  people.forEach(person => {
    const armsGroup = createArmsForNode(person.id, person.pos);
    armsGroups.set(person.id, armsGroup);
    masterGroup.add(armsGroup);
  });

  // Create edges
  edgesGroup = createEdgesGroup();
  masterGroup.add(edgesGroup);

  connections.forEach(conn => {
    const sourcePerson = people.find(p => p.id === conn.source);
    const targetPerson = people.find(p => p.id === conn.target);
    if (sourcePerson && targetPerson) {
      addConnectionEdge(
        edgesGroup,
        sourcePerson.pos,
        targetPerson.pos,
        conn.type,
        conn.strength
      );
    }
  });
  setEdgesVisibility(edgesGroup, false);

  // Create labels
  labelsGroup = createLabelsGroup(people);
  masterGroup.add(labelsGroup);
  setLabelsVisibility(labelsGroup, false);

  // Setup mouse interaction
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  renderer.domElement.addEventListener('click', (e) => {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    // Would implement node selection here
  });

  // Animation loop
  function animate() {
    animationId = requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Animate arms breathing
    armsGroups.forEach(armsGroup => {
      animateArms(armsGroup, time);
    });

    // Auto-rotate when idle
    if (camManager.controls.autoRotate) {
      masterGroup.rotation.y += camManager.controls.autoRotateSpeed * 0.01;
    }

    // Update zoom level
    const distance = camera.position.length();
    const zoomChange = camManager.updateZoomLevel(distance);
    if (zoomChange.changed) {
      setZoomLevel(zoomChange.level);
      setEdgesVisibility(edgesGroup, zoomChange.showEdges);
      setLabelsVisibility(labelsGroup, zoomChange.showLabels);
    }

    renderer.render(scene, camera);
  }

  animate();
}

// Start when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

export { init };
