import { expect, test } from '@playwright/test';

const API_URL = process.env.API_URL || 'http://127.0.0.1:8000';

test.describe('ClinicOS live API contract', () => {
  test('publishes an OpenAPI document and all frontend list resources return arrays', async ({ request }) => {
    const schema = await request.get(`${API_URL}/openapi.json`);
    expect(schema.ok()).toBeTruthy();
    const openapi = await schema.json();
    expect(openapi.info.title).toBe('ClinicOS API');

    for (const path of ['/patients', '/doctors', '/receptionists', '/departments', '/appointments', '/laboratory/tests', '/pharmacy/medicines']) {
      const response = await request.get(`${API_URL}${path}`);
      expect(response.status(), path).toBe(200);
      expect(await response.json(), path).toEqual(expect.any(Array));
    }
  });
});
