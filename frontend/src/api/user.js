// src/api/user.js
import { authFetch } from './auth';

// URL сервера — замените при необходимости
const BASE_URL = 'http://localhost:8000';


export async function getUserInfo(id) {
  const response = await authFetch(`http://localhost:8000/id/${id}`, {
    method: 'GET'
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to get user info');
  }

  return await response.json();
}


export async function deleteUser(username) {
  const url = `${BASE_URL}/delete`;

  const response = await authFetch(url, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to delete user');
  }

  return await response.json();
}