// Central app state management
const state = {
  people: [],
  connections: [],
  selectedPerson: null,
  highlightedPath: [],
  highlightedNeighbors: new Set(),
  zoomLevel: 'FAR',
  showLabels: false,
  showEdges: false,
  searchQuery: '',
  searchResults: new Set(),
  isWebSocketConnected: false
};

function updateState(updates) {
  Object.assign(state, updates);
  return state;
}

function getState() {
  return { ...state };
}

function selectPerson(personId) {
  state.selectedPerson = personId;
}

function clearSelection() {
  state.selectedPerson = null;
  state.highlightedPath = [];
  state.highlightedNeighbors.clear();
}

function setZoomLevel(level) {
  state.zoomLevel = level;
  state.showLabels = level === 'CLOSE';
  state.showEdges = level !== 'FAR';
}

function search(query) {
  state.searchQuery = query.toLowerCase();
  state.searchResults.clear();

  if (!query) return;

  state.people.forEach(person => {
    const matchesName = person.name.toLowerCase().includes(state.searchQuery);
    const matchesCity = person.city?.toLowerCase().includes(state.searchQuery);
    const matchesRole = person.role?.toLowerCase().includes(state.searchQuery);
    const matchesTags = person.tags?.toLowerCase().includes(state.searchQuery);

    if (matchesName || matchesCity || matchesRole || matchesTags) {
      state.searchResults.add(person.id);
    }
  });
}

function getConnectionBetween(personAId, personBId) {
  return state.connections.find(
    conn =>
      (conn.source === personAId && conn.target === personBId) ||
      (conn.source === personBId && conn.target === personAId)
  );
}

function getNeighbors(personId) {
  return state.connections
    .filter(conn => conn.source === personId || conn.target === personId)
    .map(conn => (conn.source === personId ? conn.target : conn.source));
}

export {
  state,
  updateState,
  getState,
  selectPerson,
  clearSelection,
  setZoomLevel,
  search,
  getConnectionBetween,
  getNeighbors
};
