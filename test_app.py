import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import MagicMock, patch
from app import app, get_slack_client, gen_results, grade, launch_task

# Create a TestClient for testing FastAPI
client = TestClient(app)

async def test_production_status_help():
    """Test the /productions endpoint with empty command for help message."""

    # Mock the get_slack_client function
    with patch('get_slack_client', return_value=MagicMock()) as mock_slack_client:
        response = await client.post("/productions", data={"command": "/campy"})
        
        # Assert that the help message is in the response
        assert response.status_code == 200
        assert "Campy is a bot that manages production cycle" in response.text

async def test_production_status_notify():
    """Test the /productions endpoint with the notify subcommand."""

    # Mock the slack client and its methods
    with patch('get_slack_client', return_value=MagicMock()) as mock_slack_client:
        mock_slack_client_instance = mock_slack_client.return_value
        mock_slack_client_instance.chat_postMessage = MagicMock()

        response = await client.post(
            "/productions", 
            data={"command": "/campy", "text": "notify"}
        )

        # Assert that the status code is 200 OK
        assert response.status_code == 200
        # Ensure the notify function was called
        mock_slack_client_instance.chat_postMessage.assert_called_with(
            channel='#campy',
            text=ANY
        )

async def test_production_status_grade():
    """Test the /productions endpoint with the grade subcommand."""

    with patch('get_slack_client', return_value=MagicMock()) as mock_slack_client:
        mock_slack_client_instance = mock_slack_client.return_value
        mock_slack_client_instance.chat_postMessage = MagicMock()

        response = await client.post(
            "/productions", 
            data={"command": "/campy", "text": "grade"}
        )

        assert response.status_code == 200
        mock_slack_client_instance.chat_postMessage.assert_called_with(
            channel='#campy',
            text="Your request is being processed. You will receive a response shortly."
        )


