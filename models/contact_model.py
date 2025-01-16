from datetime import date, datetime, time
import enum
from typing import Dict, List, Optional
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Date, Time
from database.connexion import get_engine

# Création de Base et Engine
Base = declarative_base()
engine = get_engine()

# Définition des Enum
class HomeType(enum.Enum):
    APARTMENT = "Appartement"
    HOUSE = "Maison"

class OccupantStatus(enum.Enum):
    OWNER = "Propriétaire"
    TENANT = "Locataire"

class MaterialType(enum.Enum):  # Correction : uniformisation avec enum.Enum
    PVC = "PVC"
    WOOD = "Bois"
    ALUMINIUM = "Aluminium"

# Modèle Meet
class Meet(Base):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True, index=True)
    date_meet = Column(Date, nullable=False)
    hour_meet = Column(Time, nullable=False)
    date_works = Column(Date, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))

    person = relationship("Person", back_populates="meet")

    def __init__(self, date_meet: date, hour_meet: time, date_works: date) -> None:
        if date_meet < date.today():
            raise ValueError("La date de rendez-vous ne peut pas être dans le passé !")

        self.date_meet = date_meet
        self.hour_meet = hour_meet
        self.date_works = date_works

    def __repr__(self) -> str:
        return f"Meet scheduled on {self.date_meet} at {self.hour_meet}, work planned for {self.date_works}."

# Modèle Person
class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    type_of_home = Column(Enum(HomeType, native_enum=False), nullable=True)
    status_occupant = Column(Enum(OccupantStatus, native_enum=False), nullable=True)

    meet = relationship("Meet", back_populates="person")
    works_planned = relationship("WorksPlanned", back_populates="person")
    contacts = relationship("Contact", back_populates="person")

    def __init__(self, name: str, firstname: str, email: str, address: str, tel: str, type_of_home: str, status_occupant: str) -> None:
        self.name = name
        self.firstname = firstname
        self.email = email
        self.address = address
        self.tel = tel

        # Conversion de string vers Enum pour éviter les erreurs
        self.type_of_home = HomeType(type_of_home) if isinstance(type_of_home, str) else type_of_home
        self.status_occupant = OccupantStatus(status_occupant) if isinstance(status_occupant, str) else status_occupant

    def __repr__(self) -> str:
        return f"Person {self.firstname} {self.name}, lives at {self.address}, phone: {self.tel}, email: {self.email}, is {self.status_occupant}, home type: {self.type_of_home}"

# Modèle WorksPlanned
class WorksPlanned(Base):
    __tablename__ = 'works_planned'

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    window = Column(String, nullable=True)
    entrance_door = Column(String, nullable=True)

    person = relationship("Person", back_populates="works_planned")

    def __init__(self, window: Optional[MaterialType] = None, entrance_door: Optional[MaterialType] = None) -> None:
        self.window = window.value if window else None 
        self.entrance_door = entrance_door.value if entrance_door else None

# Modèle Contact
class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    meet_id = Column(Integer, ForeignKey("meets.id"), nullable=False)
    works_id = Column(Integer, ForeignKey("works_planned.id"), nullable=False)

    person = relationship("Person", back_populates="contacts")
    meet = relationship("Meet")
    works_planned = relationship("WorksPlanned")

    def __init__(self, meet: Meet, person: Person, works_planned: WorksPlanned) -> None:
        self.person_id = person.id
        self.meet_id = meet.id
        self.works_id = works_planned.id

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
    
    def __repr__(self):
        return f"Contact {self.person.name} {self.person.firstname} inscrite !"

# Création des tables dans la base de données
Base.metadata.create_all(engine)
print("Base de données et tables créées avec succès !")
