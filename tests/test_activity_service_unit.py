import pytest
from fastapi import HTTPException

from src.activity_service import (
    add_participant,
    ensure_not_already_signed_up,
    get_activity_or_404,
    remove_participant_or_404,
)


@pytest.fixture
def sample_activities():
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        }
    }


def test_get_activity_or_404_returns_activity(sample_activities):
    # Arrange

    # Act
    activity = get_activity_or_404("Chess Club", sample_activities)

    # Assert
    assert activity["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_get_activity_or_404_raises_for_missing_activity(sample_activities):
    # Arrange

    # Act
    with pytest.raises(HTTPException) as exc:
        get_activity_or_404("Unknown Activity", sample_activities)

    # Assert
    assert exc.value.status_code == 404
    assert exc.value.detail == "Activity not found"


def test_ensure_not_already_signed_up_allows_new_email(sample_activities):
    # Arrange
    activity = sample_activities["Chess Club"]

    # Act
    ensure_not_already_signed_up("new@mergington.edu", activity)

    # Assert
    assert True


def test_ensure_not_already_signed_up_raises_for_duplicate_email(sample_activities):
    # Arrange
    activity = sample_activities["Chess Club"]

    # Act
    with pytest.raises(HTTPException) as exc:
        ensure_not_already_signed_up("michael@mergington.edu", activity)

    # Assert
    assert exc.value.status_code == 400
    assert exc.value.detail == "Student already signed up for this activity"


def test_add_participant_appends_email(sample_activities):
    # Arrange
    activity = sample_activities["Chess Club"]
    email = "new@mergington.edu"

    # Act
    add_participant(email, activity)

    # Assert
    assert email in activity["participants"]


def test_remove_participant_or_404_removes_existing_email(sample_activities):
    # Arrange
    activity = sample_activities["Chess Club"]
    email = "daniel@mergington.edu"

    # Act
    remove_participant_or_404(email, activity)

    # Assert
    assert email not in activity["participants"]


def test_remove_participant_or_404_raises_for_missing_email(sample_activities):
    # Arrange
    activity = sample_activities["Chess Club"]

    # Act
    with pytest.raises(HTTPException) as exc:
        remove_participant_or_404("missing@mergington.edu", activity)

    # Assert
    assert exc.value.status_code == 404
    assert exc.value.detail == "Participant not found in this activity"
