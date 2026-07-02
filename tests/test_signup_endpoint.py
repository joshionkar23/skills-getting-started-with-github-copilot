from urllib.parse import quote

from src.app import activities


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    activity_path = quote(activity_name, safe="")
    email = "new.signup@mergington.edu"
    participants = activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in participants

    participants.remove(email)


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_path = quote("Nonexistent Club", safe="")
    email = "missing.activity@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_student_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    activity_path = quote(activity_name, safe="")
    email = "duplicate.signup@mergington.edu"
    participants = activities[activity_name]["participants"]
    if email not in participants:
        participants.append(email)

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert participants.count(email) == 1

    participants.remove(email)