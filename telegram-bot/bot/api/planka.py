import requests

def get_planka_token(api_url: str, email: str, password: str) -> str | None:
    """Authenticates with Planka and returns an access token."""
    try:
        auth_payload = {"emailOrUsername": email, "password": password}
        response = requests.post(f"{api_url}/access-tokens", json=auth_payload)

        if response.status_code == 200:
            token = response.json().get("item")
            return token
        return None
    except requests.RequestException:
        return None

def create_planka_user(api_url: str, token: str, user_data: dict) -> requests.Response:
    """Creates a new user in Planka."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.post(f"{api_url}/users", headers=headers, json=user_data)
