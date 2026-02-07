"""Basic API checks for the RAG assistant."""

import requests

BASE_URL = "http://localhost:7860"

def test_healthcheck():
    """Verify the root endpoint returns HTTP 200."""
    try:
        response = requests.get(BASE_URL + "/")
        assert response.status_code == 200
        print("Test / (healthcheck) OK")
    except Exception as e:
        print(f"Test / failed: {e}")

def test_ask_endpoint():
    """Verify /ask returns a response payload."""
    try:
        payload = {"question": "What events are happening in August?"}
        response = requests.post(BASE_URL + "/ask", json=payload)
        assert response.status_code == 200
        json_data = response.json()
        assert "response" in json_data
        print("Test /ask OK")
    except Exception as e:
        print(f"Test /ask failed: {e}")

if __name__ == "__main__":
    test_healthcheck()
    test_ask_endpoint()
