from datetime import datetime, timedelta, timezone

from app.modules.appointments.schemas import normalize_appointment_datetime


def patient_payload(phone="9000000001"):
    return {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "date_of_birth": "1990-01-01",
        "gender": "FEMALE",
        "phone_number": phone,
    }


def appointment_dependencies(client):
    patient = client.post("/patients", json=patient_payload()).json()
    doctor = client.post(
        "/doctors",
        json={
            "first_name": "Grace", "last_name": "Hopper",
            "specialization": "Cardiologist", "phone_number": "9000000002",
            "qualification": "MD", "years_of_experience": 10,
            "consultation_fee": "500.00",
        },
    ).json()
    receptionist = client.post(
        "/receptionists",
        json={"first_name": "Lin", "last_name": "Chen", "phone_number": "9000000003", "shift": "MORNING"},
    ).json()
    return patient, doctor, receptionist


def appointment_payload(patient, doctor, receptionist, when):
    return {
        "patient_id": patient["id"], "doctor_id": doctor["id"],
        "receptionist_id": receptionist["id"], "problem": "Fever",
        "appointment_datetime": when,
    }


def test_patient_duplicate_and_deactivate(client):
    first = client.post("/patients", json=patient_payload())
    assert first.status_code == 201
    assert first.json()["patient_code"] == "PT000001"
    assert client.post("/patients", json=patient_payload()).status_code == 409
    assert client.delete(f"/patients/{first.json()['id']}").json()["is_active"] is False


def test_normalizes_aware_and_naive_datetimes_to_utc():
    aware = normalize_appointment_datetime(datetime(2026, 9, 1, 15, tzinfo=timezone(timedelta(hours=5))))
    naive = normalize_appointment_datetime(datetime(2026, 9, 1, 10))
    assert aware == datetime(2026, 9, 1, 10, tzinfo=timezone.utc)
    assert naive == datetime(2026, 9, 1, 10, tzinfo=timezone.utc)


def test_appointment_accepts_utc_aware_datetime(client):
    patient, doctor, receptionist = appointment_dependencies(client)
    when = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    response = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, when))
    assert response.status_code == 201


def test_appointment_accepts_naive_datetime_as_utc(client):
    patient, doctor, receptionist = appointment_dependencies(client)
    when = (datetime.now(timezone.utc) + timedelta(days=1)).replace(tzinfo=None).isoformat()
    response = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, when))
    assert response.status_code == 201


def test_appointment_rejects_past_datetime(client):
    patient, doctor, receptionist = appointment_dependencies(client)
    when = (datetime.now(timezone.utc) - timedelta(minutes=1)).replace(tzinfo=None).isoformat()
    response = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, when))
    assert response.status_code == 400
    assert response.json()["detail"] == "Appointment time must be in the future"


def test_appointment_prevents_double_booking_for_equivalent_offsets(client):
    patient, doctor, receptionist = appointment_dependencies(client)
    utc_time = datetime.now(timezone.utc) + timedelta(days=1)
    first = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, utc_time.isoformat()))
    equivalent_offset = utc_time.astimezone(timezone(timedelta(hours=5, minutes=30))).isoformat()
    second = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, equivalent_offset))
    assert first.status_code == 201
    assert second.status_code == 409


def test_appointment_status_transitions_remain_validated(client):
    patient, doctor, receptionist = appointment_dependencies(client)
    when = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    appointment = client.post("/appointments", json=appointment_payload(patient, doctor, receptionist, when)).json()
    appointment_id = appointment["id"]
    assert client.post(f"/appointments/{appointment_id}/status", json={"appointment_status": "WAITING"}).status_code == 200
    assert client.post(f"/appointments/{appointment_id}/status", json={"appointment_status": "COMPLETED"}).status_code == 400
