def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in activities


def test_get_activities_returns_activity_details(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert activities
    for activity in activities.values():
        assert required_fields.issubset(activity.keys())
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)