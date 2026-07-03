// Create sprite-based text labels for nodes
function createNameSprite(name, fontSize = 48) {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 128;

  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'rgba(0, 0, 0, 0)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.font = `bold ${fontSize}px Arial`;
  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(name, canvas.width / 2, canvas.height / 2);

  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.SpriteMaterial({ map: texture });
  const sprite = new THREE.Sprite(material);
  sprite.scale.set(100, 25, 1);

  return sprite;
}

function createLabelsGroup(people) {
  const group = new THREE.Group();

  people.forEach((person, i) => {
    const sprite = createNameSprite(person.name);
    sprite.position.copy(person.pos);
    sprite.position.z += 100;
    sprite.userData = {
      personId: person.id,
      isLabel: true
    };
    group.add(sprite);
  });

  return group;
}

function setLabelsVisibility(labelsGroup, visible) {
  labelsGroup.children.forEach(label => {
    label.visible = visible;
  });
}

export { createNameSprite, createLabelsGroup, setLabelsVisibility };
