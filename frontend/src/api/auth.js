// src/api/auth.js

// URL сервера — замените при необходимости
const BASE_URL = 'http://localhost:8000';

export async function registerUser({ username, password, role }) {
  const url = `${BASE_URL}/register`;

  const payload = {
    username: username.trim(),
    password: password.trim(),
    role: role.trim()
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to register');
  }

  return response.json();
}

export async function loginUser(username, password) {
  const url = `${BASE_URL}/login`;

  // Для login эндпоинт ожидает данные в форм-дате (OAuth2PasswordRequestForm)
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(url, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Login failed');
  }

  const data = await response.json();
  // Сохраняем токены
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  return data;
}

export function getAuthHeaders() {
  const accessToken = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(accessToken ? { 'Authorization': `Bearer ${accessToken}` } : {})
  };
}

export async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) throw new Error('No refresh token available');

  const url = `${BASE_URL}/refresh`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to refresh token');
  }

  const data = await response.json();
  // Обновляем токены в хранилище
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  return data;
}

// Хелпер для выполнения запросов с попыткой автоматического обновления токена при 401 ошибке
export async function authFetch(url, options = {}) {
  let response = await fetch(url, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...(options.headers || {})
    }
  });

  if (response.status === 401) {
    // Попытка обновить токен
    try {
      await refreshAccessToken();
      // Повторяем запрос с обновлённым токеном
      response = await fetch(url, {
        ...options,
        headers: {
          ...getAuthHeaders(),
          ...(options.headers || {})
        }
      });
    } catch (err) {
      throw new Error('Authentication failed, please log in again.');
    }
  }

  return response;
}
