// Create connection edges with type-specific visual encoding
function createEdgesGroup() {
  return new THREE.Group();
}

function addConnectionEdge(edgesGroup, sourcePos, targetPos, type, strength = 3) {
  // Create bezier curve with organic offset
  const midpoint = new THREE.Vector3().addVectors(sourcePos, targetPos).multiplyScalar(0.5);
  const offset = new THREE.Vector3(
    (Math.random() - 0.5) * 100,
    (Math.random() - 0.5) * 100,
    (Math.random() - 0.5) * 100
  );
  const controlPoint = midpoint.clone().add(offset);

  const curve = new THREE.QuadraticBezierCurve3(sourcePos, controlPoint, targetPos);
  const points = curve.getPoints(32);
  const geometry = new THREE.BufferGeometry().setFromPoints(points);

  let material;
  const thickness = (strength / 5) * 2;

  switch (type) {
    case 'family_core':
      // Solid thick line
      material = new THREE.LineBasicMaterial({
        color: 0xff6b6b,
        linewidth: thickness * 1.5,
        opacity: 0.6,
        transparent: true
      });
      break;

    case 'family_extended':
      // Solid thin line
      material = new THREE.LineBasicMaterial({
        color: 0xff8c8c,
        linewidth: thickness * 0.8,
        opacity: 0.4,
        transparent: true
      });
      break;

    case 'friend':
      // Dashed line
      material = new THREE.LineDashedMaterial({
        color: 0x4ecdc4,
        linewidth: thickness,
        dashSize: 10,
        gapSize: 5,
        opacity: 0.5,
        transparent: true
      });
      break;

    case 'acquaintance':
    default:
      // Double parallel lines
      material = new THREE.LineBasicMaterial({
        color: 0x95a5a6,
        linewidth: thickness * 0.5,
        opacity: 0.3,
        transparent: true
      });
      break;
  }

  const line = new THREE.Line(geometry, material);
  line.userData = { type, strength };

  edgesGroup.add(line);
  return line;
}

function setEdgesVisibility(edgesGroup, visible) {
  edgesGroup.children.forEach(edge => {
    edge.visible = visible;
  });
}

export { createEdgesGroup, addConnectionEdge, setEdgesVisibility };
