from app.entities.user.schema import UserCreate, UserFilter
import uuid

users_prefix = f"/api/v1/users"


def test_get_all_users(test_client,fake_repo,fake_session):
    response = test_client.get(
        url=f"{users_prefix}"
    )

    assert fake_repo.get_all_users_called_once()
    assert fake_repo.get_all_users_called_once_with(fake_session)


def test_create_user(test_client, fake_repo, fake_session):
    user_data = {
        "username":"Test",
        "password" : "Test12223333",
        "email": "Test@mail.com",
        "firstname":"Test",
        "lastname": "Test",
        "user_type": "user",
        "gender": "male"
    }
    response = test_client.post(
        url=f"{users_prefix}",
        json=user_data
    )
    
    user_create_data = UserCreate(**user_data)

    assert fake_repo.create_user_called_once()
    assert fake_repo.create_user_called_once_with(user_create_data, fake_session)


def test_get_user_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.get(f"{users_prefix}/{uid}")

    assert fake_repo.get_user_called_once()
    assert fake_repo.get_user_called_once_with(uid,fake_session)


def test_update_user_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.put(f"{users_prefix}/{uid}")

    assert fake_repo.get_user_called_once()
    assert fake_repo.get_user_called_once_with(uid,fake_session)

def test_delete_user_by_uid(test_client, fake_repo, fake_session):
    uid = str(uuid.uuid4())
    response = test_client.delete(f"{users_prefix}/{uid}")

    assert fake_repo.delete_user_called_once()
    assert fake_repo.delete_user_called_once_with(uid,fake_session)

def test_get_filtered_users(test_client, fake_repo, fake_session):
    user_filter = {
        "username" : "test"
    }
    response = test_client.post(
        url=f"{users_prefix}",
        json=user_filter
    )
    
    user_filter_data = UserFilter(**user_filter)

    assert fake_repo.filter_users_called_once()
    assert fake_repo.filter_users_called_once_with(user_filter_data, fake_session)


