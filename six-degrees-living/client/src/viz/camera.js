// Camera management with OrbitControls and zoom-level state machine
function setupCamera(camera, canvas) {
  // OrbitControls will be initialized after the global is available
  const controls = {
    enabled: true,
    autoRotate: true,
    autoRotateSpeed: 0.5,
    enableZoom: true,
    enablePan: false,
    enableRotate: true,
    minDistance: 100,
    maxDistance: 5000,
    target: new THREE.Vector3(0, 0, 0)
  };

  // Zoom level state machine
  const zoomState = {
    FAR: { threshold: 2000, showLabels: false, showEdges: false },
    MID: { threshold: 600, showLabels: false, showEdges: true },
    CLOSE: { threshold: 0, showLabels: true, showEdges: true }
  };

  let currentZoomLevel = 'FAR';

  function getZoomLevel(distance) {
    if (distance > zoomState.FAR.threshold) return 'FAR';
    if (distance > zoomState.MID.threshold) return 'MID';
    return 'CLOSE';
  }

  function updateZoomLevel(distance) {
    const newLevel = getZoomLevel(distance);
    if (newLevel !== currentZoomLevel) {
      currentZoomLevel = newLevel;
      return {
        changed: true,
        level: newLevel,
        showLabels: zoomState[newLevel].showLabels,
        showEdges: zoomState[newLevel].showEdges
      };
    }
    return { changed: false };
  }

  return {
    controls,
    zoomState,
    currentZoomLevel,
    getZoomLevel,
    updateZoomLevel
  };
}

export { setupCamera };
