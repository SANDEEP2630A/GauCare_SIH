const API_BASE = 'http://127.0.0.1:8000/api';

export async function getCows() {
  const response = await fetch(`${API_BASE}/cows/`);

  if (!response.ok) {
    throw new Error('Failed to fetch cows');
  }

  return response.json();
}

export async function getLatestScan(cowId) {
  const data = await getCowScans(cowId);
  const scans = data.scans || [];
  if (scans.length === 0) return { new_scan: false };
  const latest = scans[scans.length - 1];
  return { new_scan: !!latest.prediction, scan: latest };
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