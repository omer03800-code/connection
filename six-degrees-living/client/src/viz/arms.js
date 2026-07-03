// Create animated arms/tendrils for each node
function createArmsForNode(nodeId, nodePos) {
  const armsGroup = new THREE.Group();
  const armCount = 4;

  for (let i = 0; i < armCount; i++) {
    const angle = (i / armCount) * Math.PI * 2;
    const armLength = 80 + Math.random() * 40;

    // Create bezier curve for organic arm
    const startPoint = nodePos.clone();
    const controlPoint = new THREE.Vector3(
      nodePos.x + Math.cos(angle) * armLength * 0.7,
      nodePos.y + Math.sin(angle) * armLength * 0.7,
      nodePos.z + (Math.random() - 0.5) * armLength * 0.3
    );
    const endPoint = new THREE.Vector3(
      nodePos.x + Math.cos(angle) * armLength,
      nodePos.y + Math.sin(angle) * armLength,
      nodePos.z + (Math.random() - 0.5) * armLength * 0.5
    );

    const curve = new THREE.QuadraticBezierCurve3(startPoint, controlPoint, endPoint);
    const points = curve.getPoints(16);

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({
      color: 0xffffff,
      opacity: 0.15,
      transparent: true,
      linewidth: 2,
      blending: THREE.AdditiveBlending
    });

    const armMesh = new THREE.Line(geometry, material);
    armMesh.userData = {
      nodeId,
      phase: Math.random() * Math.PI * 2,
      speed: 0.01 + Math.random() * 0.01,
      baseScale: 1.0,
      rotSpeedX: (Math.random() - 0.5) * 0.002,
      rotSpeedY: (Math.random() - 0.5) * 0.002
    };

    armsGroup.add(armMesh);
  }

  armsGroup.userData = {
    nodeId,
    isArmsGroup: true
  };

  return armsGroup;
}

function animateArms(armsGroup, time) {
  armsGroup.children.forEach(arm => {
    const data = arm.userData;
    const breatheScale = 0.8 + 0.2 * Math.sin(time * data.speed + data.phase);
    arm.scale.set(1, breatheScale, 1);
  });

  armsGroup.rotation.x += armsGroup.userData.rotSpeedX || 0;
  armsGroup.rotation.y += armsGroup.userData.rotSpeedY || 0;
}

export { createArmsForNode, animateArms };
