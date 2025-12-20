import requests
from typing import Dict, Any

API_BASE_URL = "http://localhost:5000"

'''
Docstring for login

:param username: The username of the user
:type username: str
:param email: The email of the user
:type email: str
:param password: The password of the user
:type password: str
:return: Description
:rtype: Dict[str, Any]
'''
def login(identifier: str, password: str) -> Dict[str, Any]:
    """
    Send login request to server.
    Returns response JSON or error dict
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"identifier": identifier, "password": password},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return {"error": str(e)}

'''
Docstring for login

:param username: The username of the user
:type username: str
:param email: The email of the user
:type email: str
:param password: The password of the user
:type password: str
:return: Description
:rtype: Dict[str, Any]
''' 
def signup(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Send signup request to server.
    Returns response JSON or error dict.
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/signup",
            json={"username": username, "password": password, "email": email},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Signup failed: {e}")
        return {"error": str(e)}