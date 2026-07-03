// Create glowing node dots with custom shader
function createNodesGeometry(people) {
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(people.length * 3);

  people.forEach((person, i) => {
    const pos = person.pos || new THREE.Vector3(0, 0, 0);
    positions[i * 3] = pos.x;
    positions[i * 3 + 1] = pos.y;
    positions[i * 3 + 2] = pos.z;
  });

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

  const vertexShader = `
    attribute float size;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
      gl_PointSize = size * (300.0 / -mvPosition.z);
      gl_Position = projectionMatrix * mvPosition;
    }
  `;

  const fragmentShader = `
    uniform sampler2D texture;
    varying vec2 vUv;

    void main() {
      vec2 uv = (gl_PointCoord - 0.5) * 2.0;
      float dist = length(uv);
      float alpha = exp(-dist * dist * 4.0);
      gl_FragColor = vec4(1.0, 1.0, 1.0, alpha * 0.8);
    }
  `;

  const material = new THREE.ShaderMaterial({
    uniforms: {
      texture: { value: null }
    },
    vertexShader,
    fragmentShader,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true
  });

  const points = new THREE.Points(geometry, material);
  return { geometry, material, points };
}

export { createNodesGeometry };
