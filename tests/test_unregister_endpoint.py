from urllib.parse import quote

from src.app import activities


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Gym Class"
    activity_path = quote(activity_name, safe="")
    email = "remove.me@mergington.edu"
    email_path = quote(email, safe="")
    participants = activities[activity_name]["participants"]
    if email not in participants:
        participants.append(email)

    # Act
    response = client.delete(f"/activities/{activity_path}/participants/{email_path}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_path = quote("Nonexistent Club", safe="")
    email_path = quote("someone@mergington.edu", safe="")

    # Act
    response = client.delete(f"/activities/{activity_path}/participants/{email_path}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    activity_path = quote(activity_name, safe="")
    email = "not.registered@mergington.edu"
    email_path = quote(email, safe="")
    participants = activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    # Act
    response = client.delete(f"/activities/{activity_path}/participants/{email_path}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}
    assert email not in participants