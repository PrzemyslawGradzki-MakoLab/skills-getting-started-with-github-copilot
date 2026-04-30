def test_get_activities_returns_data_and_no_store_header(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_adds_new_participant(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for Chess Club"
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={duplicate_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/Unknown Activity/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_missing_email_returns_422(client):
    # Arrange

    # Act
    response = client.post("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422


def test_unregister_removes_existing_participant(client):
    # Arrange
    email = "daniel@mergington.edu"

    # Act
    unregister_response = client.delete(f"/activities/Chess Club/participants?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from Chess Club"
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/Unknown Activity/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    email = "not.in.activity@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_missing_email_returns_422(client):
    # Arrange

    # Act
    response = client.delete("/activities/Chess Club/participants")

    # Assert
    assert response.status_code == 422
