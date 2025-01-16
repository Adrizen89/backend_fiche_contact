from typing import Optional
import requests


class OutlookCalendar:
    def __init__(self, access_token: Optional[str]):
        if not access_token:
            raise ValueError("Un jeton d'accès est requis pour initialiser Outlook Calendar ! ")
        self.access_token = access_token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }


    def create_event(self, event_data: dict, user_email: str) -> dict:
        response = requests.post(
            f"{self.base_url}/users/{user_email}/events",
            headers=self.headers,
            json= event_data
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la création de l'événement : {response.text}")

        