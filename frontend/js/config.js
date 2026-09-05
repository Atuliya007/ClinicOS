export const API_BASE_URL = localStorage.getItem('clinicos_api_url') || 'http://127.0.0.1:8000';
export const setApiBaseUrl = value => localStorage.setItem('clinicos_api_url', value.replace(/\/$/, ''));
