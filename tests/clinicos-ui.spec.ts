import { expect, test, type Page, type Route } from '@playwright/test';

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://127.0.0.1:5500/frontend/index.html';
const API_URL = 'http://127.0.0.1:8000';
const future = '2030-12-20T09:30:00Z';

const patients = [{ id: '11111111-1111-4111-8111-111111111111', patient_code: 'PT000001', first_name: 'Ada', last_name: 'Lovelace', date_of_birth: '1990-01-01', gender: 'FEMALE', phone_number: '9000000001', email: 'ada@example.test', blood_group: 'A+', is_active: true }];
const doctors = [{ id: '22222222-2222-4222-8222-222222222222', doctor_code: 'DR000001', first_name: 'Grace', last_name: 'Hopper', specialization: 'Cardiologist', phone_number: '9000000002', email: 'grace@example.test', qualification: 'MD', years_of_experience: 10, consultation_fee: '500.00', is_active: true }];
const receptionists = [{ id: '33333333-3333-4333-8333-333333333333', receptionist_code: 'RC000001', first_name: 'Lin', last_name: 'Chen', phone_number: '9000000003', email: 'lin@example.test', shift: 'MORNING', is_active: true }];
const departments = [{ id: '44444444-4444-4444-8444-444444444444', department_code: 'DP000001', name: 'Cardiology', description: 'Heart care', is_active: true }];
const appointments = [{ id: '55555555-5555-4555-8555-555555555555', patient_id: patients[0].id, doctor_id: doctors[0].id, receptionist_id: receptionists[0].id, appointment_datetime: future, problem: 'Follow-up', notes: null, appointment_status: 'PENDING' }];
const labTests = [{ id: '66666666-6666-4666-8666-666666666666', test_code: 'LT000001', name: 'Complete blood count', price: '350.00', description: 'CBC', is_active: true }];
const medicines = [{ id: '77777777-7777-4777-8777-777777777777', medicine_code: 'MD000001', name: 'Paracetamol', description: '500mg tablet', unit_price: '5.00', stock_quantity: 30, reorder_level: 10, is_active: true }];

const json = (route: Route, body: unknown, status = 200) => route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });

async function mockClinicApi(page: Page, captured: { method?: string; path?: string; body?: unknown } = {}) {
  await page.route(`${API_URL}/**`, async route => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    const method = request.method();
    if (method !== 'GET') {
      captured.method = method;
      captured.path = path;
      captured.body = request.postDataJSON();
    }
    if (method === 'GET') {
      const resources: Record<string, unknown> = {
        '/patients': patients, '/doctors': doctors, '/receptionists': receptionists,
        '/departments': departments, '/appointments': appointments,
        '/laboratory/tests': labTests, '/pharmacy/medicines': medicines,
        [`/appointments/${appointments[0].id}`]: appointments[0],
      };
      return json(route, resources[path] ?? []);
    }
    if (path.endsWith('/status')) return json(route, { ...appointments[0], appointment_status: 'WAITING' });
    if (path.endsWith('/cancel')) return json(route, { ...appointments[0], appointment_status: 'CANCELLED' });
    return json(route, { id: '99999999-9999-4999-8999-999999999999' }, 201);
  });
}

async function open(page: Page, hash = 'dashboard') {
  await page.goto(`${FRONTEND_URL}#${hash}`);
  await expect(page.locator('#app h1')).not.toHaveText('Loading…');
}

test.describe('ClinicOS frontend', () => {
  test('renders a live dashboard without browser errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    await mockClinicApi(page);
    await open(page);
    await expect(page.getByRole('heading', { name: 'Good day, clinic team' })).toBeVisible();
    await expect(page.locator('.stat').filter({ hasText: 'Total patients' }).locator('.stat-value')).toHaveText('1');
    expect(errors).toEqual([]);
  });

  test('navigates every implemented module and renders its primary UI', async ({ page }) => {
    await mockClinicApi(page);
    const checks: Array<[string, string]> = [
      ['patients', 'Patients'], ['doctors', 'Doctors'], ['departments', 'Departments'],
      ['appointments', 'Appointments'], ['receptionists', 'Receptionists'],
      ['laboratory', 'Laboratory'], ['pharmacy', 'Pharmacy'], ['billing', 'Billing'], ['settings', 'Settings'],
    ];
    for (const [route, heading] of checks) {
      await open(page, route);
      await expect(page.getByRole('heading', { name: heading })).toBeVisible();
    }
  });

  test('submits an appointment with exact API field names and ISO datetime', async ({ page }) => {
    const captured: { method?: string; path?: string; body?: any } = {};
    await mockClinicApi(page, captured);
    await open(page, 'appointments');
    await page.getByRole('button', { name: 'Create appointment', exact: true }).click();
    await page.locator('#f-patient_id').selectOption(patients[0].id);
    await page.locator('#f-doctor_id').selectOption(doctors[0].id);
    await page.locator('#f-receptionist_id').selectOption(receptionists[0].id);
    await page.locator('#f-appointment_datetime').fill('2030-12-20T15:00');
    await page.locator('#f-problem').fill('Annual review');
    await page.locator('#modal-form button[type=submit]').click();
    await expect(page.getByText('Appointment created successfully.')).toBeVisible();
    expect(captured.method).toBe('POST');
    expect(captured.path).toBe('/appointments');
    expect(captured.body).toMatchObject({ patient_id: patients[0].id, doctor_id: doctors[0].id, receptionist_id: receptionists[0].id, problem: 'Annual review' });
    expect(captured.body.appointment_datetime).toMatch(/^2030-12-20T/);
  });

  test('shows and advances the appointment lifecycle using the status endpoint', async ({ page }) => {
    const captured: { method?: string; path?: string; body?: any } = {};
    await mockClinicApi(page, captured);
    await open(page, `appointments/${appointments[0].id}`);
    await expect(page.getByText('Appointment lifecycle')).toBeVisible();
    await page.getByRole('button', { name: 'Move to WAITING' }).click();
    await expect(page.getByText('Appointment moved to WAITING.')).toBeVisible();
    expect(captured).toMatchObject({ method: 'POST', path: `/appointments/${appointments[0].id}/status`, body: { appointment_status: 'WAITING' } });
  });

  test('opens all operational creation dialogs with valid dynamic select options', async ({ page }) => {
    await mockClinicApi(page);
    for (const [route, button, fieldId] of [
      ['laboratory', 'Create lab order', '#f-lab_test_id'],
      ['pharmacy', 'Dispense prescription', '#f-medicine_id'],
      ['billing', 'Create invoice', '#f-patient_id'],
    ]) {
      await open(page, route);
      await page.getByRole('button', { name: button, exact: true }).click();
      await expect(page.locator('#modal-form')).toBeVisible();
      await expect(page.locator(fieldId).locator('option')).toHaveCount(2);
      await page.getByRole('button', { name: 'Cancel' }).click();
    }
  });

  test('uses semantic, keyboard-focusable navigation and opens the mobile menu', async ({ page }) => {
    await mockClinicApi(page);
    await page.setViewportSize({ width: 390, height: 844 });
    await open(page);
    await expect(page.getByRole('navigation', { name: 'Main navigation' })).toBeVisible();
    await page.getByRole('button', { name: 'Open navigation' }).click();
    await expect(page.locator('#sidebar')).toHaveClass(/open/);
    await page.getByRole('link', { name: 'Patients' }).focus();
    await expect(page.getByRole('link', { name: 'Patients' })).toBeFocused();
  });
});
