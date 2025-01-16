from datetime import date, datetime, time
from enum import Enum
from typing import Dict, List, Optional


class HomeType(Enum):
    APARTMENT = "Appartement"
    HOUSE = "Maison"

class OccupantStatus(Enum):
    OWNER = "Propriétaire"
    TENANT = "Locataire"

class MaterialType(Enum):
    PVC = "PVC"
    WOOD = "Bois"
    ALUMINIUM = "Alu"

class Meet:
    def __init__(self, date_meet: date, hour_meet: time, date_works: date) -> None:
        self.date_meet = date_meet
        self.hour_meet = hour_meet
        self.date_works = date_works

        if self.date_meet < date.today():
            raise ValueError("La date de rendez-vous ne peut pas être dans le passé !")
        
    def __repr__(self) -> str:
        return f"La date de rendez-vous prévu est le {self.date_meet} à {self.hour_meet} et les travaux sont envisagés le {self.date_works}."

class Person:
    def __init__(self, name: str, firstname: str, email: str, address: str, tel: int, type_of_home: HomeType, status_occupant: OccupantStatus) -> None:
        self.name = name
        self.firstname = firstname
        self.email = email
        self.address = address
        self.tel = tel
        self.type_of_home = type_of_home
        self.status_occupant = status_occupant
    
    def __repr__(self) -> str:
        return f"Le contact est {self.firstname} {self.name}, habite au {self.address}, numéro de téléphone : {self.tel}, email: {self.email}, il est {self.status_occupant} et c'est un(e) {self.type_of_home}"

class WorksPlanned:
    def __init__(self, window: Optional[List[MaterialType]] = None, entrance_door: Optional[List[MaterialType]] = None) -> None:
        self.window = window
        self.entrance_door = entrance_door
    

class Contact:
    def __init__(self, meet: Meet, person: Person, works_planned: WorksPlanned) -> None:
        self.meet = meet
        self.person = person
        self.works_planned = works_planned

    def to_event_data(self) -> Dict:
        """
        Convertit la fiche contact en un format compatible avec Outlook Calendar
        """
        return {
            "subject": f"Rendez-vous avec {self.person.firstname} {self.person.name}",
            "start": {
                "dateTime": self.meet.date_meet.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Europe/Paris"
            },
            "end": {
                "dateTime": (datetime.combine(self.meet.date_meet, self.meet.hour_meet)
                            .strftime("%Y-%m-%dT%H:%M:%S")),
                "timeZone": "Europe/Paris"
            },
            "location": {
                "displayName": self.person.address
            },
            "attendees": [
                {
                    "emailAddress": {"address": self.person.email},
                    "type": "required"
                }
            ]
        }
