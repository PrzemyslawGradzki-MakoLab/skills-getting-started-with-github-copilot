from fastapi import HTTPException


def get_activity_or_404(activity_name: str, activities: dict) -> dict:
    """Return an activity or raise a 404 error when it does not exist."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activities[activity_name]


def ensure_not_already_signed_up(email: str, activity: dict) -> None:
    """Validate that a participant is not already in the activity."""
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")


def add_participant(email: str, activity: dict) -> None:
    """Add a participant email to the activity list."""
    activity["participants"].append(email)


def remove_participant_or_404(email: str, activity: dict) -> None:
    """Remove a participant or raise a 404 error when missing."""
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    activity["participants"].remove(email)
