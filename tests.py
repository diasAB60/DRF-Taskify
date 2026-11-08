import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_full_taskify_workflow():
    client = APIClient()

    user = User.objects.create_user(username="boss_user", email="boss@example.com", password="password123")

    client.force_authenticate(user=user)

    org_response = client.post('/api/organizations/', {
        "name": "Super Dev Team",
        "description": "Main development organization"
    }, format='json')

    assert org_response.status_code == status.HTTP_201_CREATED
    org_id = org_response.data['id']

    project_response = client.post('/api/projects/', {
        "name": "SaaS Backend",
        "organization": org_id,
        "description": "Backend API project"
    }, format='json')

    assert project_response.status_code == status.HTTP_201_CREATED
    project_id = project_response.data['id']

    task_response = client.post('/api/tasks/', {
        "title": "Setup pytest automation",
        "description": "Write comprehensive tests for multi-tenancy",
        "project": project_id,
        "status": "new",
        "priority": "low"
    }, format='json')

    assert task_response.status_code == status.HTTP_201_CREATED
    assert task_response.data['title'] == "Setup pytest automation"


@pytest.mark.django_db
def test_data_isolation_between_organizations():
    client = APIClient()

    user1 = User.objects.create_user(username="alice", email="alice@example.com", password="password123")
    user2 = User.objects.create_user(username="bob", email="bob@example.com", password="password123")

    client.force_authenticate(user=user1)

    org_response = client.post('/api/organizations/', {
        "name": "Alice Secret Org",
        "description": "Only Alice should access this organization"
    }, format='json')

    assert org_response.status_code == status.HTTP_201_CREATED
    org_id = org_response.data['id']

    project_response = client.post('/api/projects/', {
        "name": "Alice Confidential Project",
        "organization": org_id,
        "description": "Only Alice should access this project"
    }, format='json')

    assert project_response.status_code == status.HTTP_201_CREATED
    project_id = project_response.data['id']

    alice_projects_response = client.get('/api/projects/')

    assert alice_projects_response.status_code == status.HTTP_200_OK
    assert any(project['id'] == project_id for project in alice_projects_response.data)

    client.force_authenticate(user=user2)

    bob_projects_response = client.get('/api/projects/')

    assert bob_projects_response.status_code == status.HTTP_200_OK
    assert all(project['id'] != project_id for project in bob_projects_response.data)

    bob_project_detail_response = client.get(f'/api/projects/{project_id}/')

    assert bob_project_detail_response.status_code == status.HTTP_404_NOT_FOUND

    bob_create_project_response = client.post('/api/projects/', {
        "name": "Bob Should Not Create This",
        "organization": org_id,
        "description": "Bob is trying to create a project inside Alice's organization"
    }, format='json')

    assert bob_create_project_response.status_code in [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
    ]

    bob_create_task_response = client.post('/api/tasks/', {
        "title": "Bob Should Not Create This Task",
        "description": "Bob is trying to create a task inside Alice's project",
        "project": project_id,
        "status": "new",
        "priority": "low"
    }, format='json')

    assert bob_create_task_response.status_code in [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
    ]


