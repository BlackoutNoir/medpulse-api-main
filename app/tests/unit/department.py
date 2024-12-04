from app.entities.department.schema import DepartmentCreate, DepartmentFilter
import uuid

departments_prefix = f"/api/v1/departments"


def test_get_all_departments(test_client,fake_repo,fake_session):
    response = test_client.get(
        url=f"{departments_prefix}"
    )

    assert fake_repo.get_all_departments_called_once()
    assert fake_repo.get_all_departments_called_once_with(fake_session)


def test_create_department(test_client, fake_repo, fake_session):
    department_data ={
    "name": "string",
    "description": "string",
    "default_appointment_time": 0
    }
    response = test_client.post(
        url=f"{departments_prefix}",
        json=department_data
    )
    
    department_create_data = DepartmentCreate(**department_data)

    assert fake_repo.create_department_called_once()
    assert fake_repo.create_department_called_once_with(department_create_data, fake_session)


def test_get_department_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.get(f"{departments_prefix}/{uid}")

    assert fake_repo.get_department_called_once()
    assert fake_repo.get_department_called_once_with(uid,fake_session)


def test_update_department_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.put(f"{departments_prefix}/{uid}")

    assert fake_repo.get_department_called_once()
    assert fake_repo.get_department_called_once_with(uid,fake_session)

def test_delete_department_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.delete(f"{departments_prefix}/{uid}")

    assert fake_repo.delete_department_called_once()
    assert fake_repo.delete_department_called_once_with(uid,fake_session)

def test_get_filtered_departments(test_client, fake_repo, fake_session):
    department_filter = {
        "order_by" : "uid"
    }
    response = test_client.post(
        url=f"{departments_prefix}",
        json=department_filter
    )
    
    department_filter_data = DepartmentFilter(**department_filter)

    assert fake_repo.filter_departments_called_once()
    assert fake_repo.filter_departments_called_once_with(department_filter_data, fake_session)