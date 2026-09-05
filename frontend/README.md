# ClinicOS frontend

This is a framework-free static frontend for the ClinicOS FastAPI API.

## Run locally

1. Start the backend from `backend` using `poetry run uvicorn app.main:app --reload`.
2. In another terminal, run `py -m http.server 5500` from this `frontend` directory.
3. Open `http://127.0.0.1:5500`.

The default API URL is `http://127.0.0.1:8000`. Change it in **Settings** if required; it is saved in browser local storage. The FastAPI app permits the local frontend origins above through CORS.

## API limitations represented in the UI

- The API has no list endpoint for lab orders, prescriptions, payments, or invoices.
- The API has no department detail endpoint and no laboratory/pharmacy edit endpoints.
- Billing can create an invoice and record a payment for a known invoice UUID; it cannot show invoice history without a list endpoint.
