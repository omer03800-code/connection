// API fetch wrapper for backend communication
const API_BASE = 'http://localhost:3001/api';

async function getGraph() {
  const response = await fetch(`${API_BASE}/graph`);
  if (!response.ok) throw new Error('Failed to fetch graph');
  return response.json();
}

async function getPeople() {
  const response = await fetch(`${API_BASE}/people`);
  if (!response.ok) throw new Error('Failed to fetch people');
  return response.json();
}

async function getPerson(id) {
  const response = await fetch(`${API_BASE}/people/${id}`);
  if (!response.ok) throw new Error('Failed to fetch person');
  return response.json();
}

async function getConnections() {
  const response = await fetch(`${API_BASE}/connections`);
  if (!response.ok) throw new Error('Failed to fetch connections');
  return response.json();
}

async function getShortestPath(fromId, toId) {
  const response = await fetch(`${API_BASE}/connections/path/${fromId}/${toId}`);
  if (!response.ok) throw new Error('Failed to fetch path');
  return response.json();
}

async function createPerson(data) {
  const response = await fetch(`${API_BASE}/people`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error('Failed to create person');
  return response.json();
}

async function createConnection(data) {
  const response = await fetch(`${API_BASE}/connections`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error('Failed to create connection');
  return response.json();
}

async function deletePerson(id) {
  const response = await fetch(`${API_BASE}/people/${id}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Failed to delete person');
  return response.json();
}

async function deleteConnection(id) {
  const response = await fetch(`${API_BASE}/connections/${id}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Failed to delete connection');
  return response.json();
}

export {
  getGraph,
  getPeople,
  getPerson,
  getConnections,
  getShortestPath,
  createPerson,
  createConnection,
  deletePerson,
  deleteConnection
};
