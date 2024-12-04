from app.entities.appointment.schema import AppointmentCreate, AppointmentFilter
import uuid

appointments_prefix = f"/api/v1/appointments"


def test_get_all_appointments(test_client,fake_repo,fake_session):
    response = test_client.get(
        url=f"{appointments_prefix}"
    )

    assert fake_repo.get_all_appointments_called_once()
    assert fake_repo.get_all_appointments_called_once_with(fake_session)


def test_create_appointment(test_client, fake_repo, fake_session):
    appointment_data = {
    "start_date": "2024-12-04T01:05:56.910Z",
    "duration": 0,
    "is_checked_in": True,
    "status": "PENDING",
    "reason_for_visit": "string",
    "location": "string",
    "is_virtual": True,
    "details": "string",
    "patient_uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "doctor_uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
    response = test_client.post(
        url=f"{appointments_prefix}",
        json=appointment_data
    )
    
    appointment_create_data = AppointmentCreate(**appointment_data)

    assert fake_repo.create_appointment_called_once()
    assert fake_repo.create_appointment_called_once_with(appointment_create_data, fake_session)


def test_get_appointment_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.get(f"{appointments_prefix}/{uid}")

    assert fake_repo.get_appointment_called_once()
    assert fake_repo.get_appointment_called_once_with(uid,fake_session)


def test_update_appointment_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.put(f"{appointments_prefix}/{uid}")

    assert fake_repo.get_appointment_called_once()
    assert fake_repo.get_appointment_called_once_with(uid,fake_session)

def test_delete_appointment_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.delete(f"{appointments_prefix}/{uid}")

    assert fake_repo.delete_appointment_called_once()
    assert fake_repo.delete_appointment_called_once_with(uid,fake_session)

def test_get_filtered_appointments(test_client, fake_repo, fake_session):
    appointment_filter = {
        "order_by" : "uid"
    }
    response = test_client.post(
        url=f"{appointments_prefix}",
        json=appointment_filter
    )
    
    appointment_filter_data = AppointmentFilter(**appointment_filter)

    assert fake_repo.filter_appointments_called_once()
    assert fake_repo.filter_appointments_called_once_with(appointment_filter_data, fake_session)