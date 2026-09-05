import { API_BASE_URL } from './config.js';

export class ApiError extends Error { constructor(message, status) { super(message); this.status = status; } }
const messageFor = (status, detail) => detail || ({400:'The request could not be completed.',404:'The requested record could not be found.',409:'This conflicts with an existing record.',422:'Please check the entered information.',500:'Something went wrong on the server. Please try again.'}[status] || 'Unable to connect to ClinicOS.');
export async function request(path, options = {}) {
  let response;
  try { response = await fetch(`${API_BASE_URL}${path}`, {headers:{'Content-Type':'application/json', ...(options.headers||{})}, ...options}); }
  catch { throw new ApiError('Unable to reach the ClinicOS API. Check that the backend is running.', 0); }
  const body = await response.json().catch(()=>null);
  if (!response.ok) { const detail = Array.isArray(body?.detail) ? 'Please check the entered information.' : body?.detail; throw new ApiError(messageFor(response.status, detail), response.status); }
  return body;
}
export const api = { get:p=>request(p), post:(p,data)=>request(p,{method:'POST',body:JSON.stringify(data)}), patch:(p,data)=>request(p,{method:'PATCH',body:JSON.stringify(data)}), delete:p=>request(p,{method:'DELETE'}) };
