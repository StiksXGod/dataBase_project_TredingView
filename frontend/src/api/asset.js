// src/api/asset.js
import { authFetch } from './auth';

export async function addAsset(payload) {
  const response = await authFetch('http://localhost:8000/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to add asset');
  }

  return await response.json(); 
}

export async function getAllAssets() {
  const response = await authFetch('http://localhost:8000/get_all_assets', {
    method: 'GET'
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to get assets');
  }

  return await response.json(); // { assets: [...] }
}
