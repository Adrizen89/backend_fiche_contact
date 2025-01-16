from datetime import date, time
from unittest.mock import Base
from models.auth_model import Auth
from controllers.outlook_controller import OutlookCalendar
from database.connexion import get_engine, get_session
from models.contact_model import Contact, HomeType, MaterialType, Meet, OccupantStatus, Person, WorksPlanned



CLIENT_ID = "fc8ed4e5-3328-4ee0-8ce4-e660c600dde7"
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
SCOPES = ["Calendars.ReadWrite"]
USER_EMAIL = "fbmenuiseriesadrien@outlook.fr"

session = get_session()

# Création et insertion d'une personne
person = Person(
    name="Dupont",
    firstname="Jean",
    email="jean.dupont@f.com",
    address="12 Rue des Lilas, Paris",
    tel="1234567890",
    type_of_home="Maison",
    status_occupant="Locataire"
)
session.add(person)
session.commit()
session.refresh(person)

meet = Meet(
    date_meet=date(2025, 1, 17),
    hour_meet=time(10,0),
    date_works=date(2025, 1, 18),
)

session.add(meet)
session.commit()
session.refresh(meet)

works_planned = WorksPlanned(
    window= MaterialType.PVC,
    entrance_door= MaterialType.WOOD
)
session.add(works_planned)
session.commit()
session.refresh(works_planned)

contact = Contact(person=person, meet=meet, works_planned=works_planned)
session.add(contact)
session.commit()
session.refresh(contact)


print(person)
print(meet)
print(contact)
