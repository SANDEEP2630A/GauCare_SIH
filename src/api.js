const API_BASE = 'http://127.0.0.1:8000/api';

export async function getCows() {
  const response = await fetch(`${API_BASE}/cows/`);

  if (!response.ok) {
    throw new Error('Failed to fetch cows');
  }

  return response.json();
}

export async function getCowScans(cowId) {
  const response = await fetch(
    `${API_BASE}/cows/${cowId}/scans/`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch scans for ${cowId}`);
  }

  return response.json();
}