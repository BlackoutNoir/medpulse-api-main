import pytest
import uuid
import importlib

entities = [
    "user",
    "log",
    "chat",
    "page",
    "department",
    "role",
    "staff",
    "doctor",
    "patient",
    "setting"
    ]


@pytest.mark.parametrize("entity", entities)
def test_get_all_entity(test_client,fake_repo,entity):
    response = test_client.get(
        url=f"/api/v1/{entity}s"
    )
    getattr(fake_repo, f"get_all_{entity}s").assert_called_once


@pytest.mark.parametrize("entity", entities)
def test_get_entity(test_client, fake_repo, entity):
    response = test_client.get(
        url=f"/api/v1/{entity}s/{str(uuid.uuid4())}"
    )
    
    repo_function = getattr(fake_repo, f"get_{entity}")
    repo_function.assert_called_once

@pytest.mark.parametrize("entity", entities)
def test_get_individual_entity(test_client, fake_repo, entity):
    response = test_client.get(
        url=f"/api/v1/{entity}s/{str(uuid.uuid4())}"
    )
    
    repo_function = getattr(fake_repo, f"get_{entity}")
    repo_function.assert_called_once



@pytest.mark.parametrize("entity", entities)
def test_create_entity(test_client, fake_repo, entity):
    response = test_client.post(
        url=f"/api/v1/{entity}s",
        json={}
    )    
    repo_function = getattr(fake_repo, f"create_{entity}")
    repo_function.assert_called_once()

