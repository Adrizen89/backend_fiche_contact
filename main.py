from datetime import date, time
from models.auth_model import Auth
from controllers.outlook_controller import OutlookCalendar
import os

from models.contact_model import Contact, HomeType, MaterialType, Meet, OccupantStatus, Person, WorksPlanned



CLIENT_ID = "fc8ed4e5-3328-4ee0-8ce4-e660c600dde7"
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
SCOPES = ["Calendars.ReadWrite"]
USER_EMAIL = "fbmenuiseriesadrien@outlook.fr"

auth = Auth(client_id=CLIENT_ID, scopes=SCOPES)

# Lancer le flux d’authentification
auth_flow = auth.initiate_auth_flow()
print(auth_flow["message"])
print(f"Connecte-toi ici : {auth_flow['verification_url']} et entre le code : {auth_flow['user_code']}")

input("Appuie sur Entrée une fois que tu as validé l’authentification...")

# Récupérer le token
access_token = auth.acquire_token()
print("Token d'accès obtenu avec succès !")

# Étape 2 : Instancier un contact
meet_info = Meet(
    date_meet=date(2025, 1, 17),  # Date du rendez-vous
    hour_meet=time(10, 0),  # Heure du rendez-vous
    date_works=date(2025, 3, 1)  # Date des travaux envisagés
)

person_info = Person(
    name="Dupont",
    firstname="Jean",
    email="jean.dupont@example.com",
    address="12 Rue des Lilas, Paris",
    tel=1234567890,
    type_of_home=HomeType.HOUSE,
    status_occupant=OccupantStatus.OWNER
)

works_planned = WorksPlanned(
    window=[MaterialType.PVC, MaterialType.ALUMINIUM],
    entrance_door=[MaterialType.WOOD]
)

contact = Contact(meet=meet_info, person=person_info, works_planned=works_planned)

# Étape 3 : Créer l'événement à partir du contact
calendar = OutlookCalendar(access_token)

try:
    event_response = calendar.create_event(contact.to_event_data(), USER_EMAIL)
    print(f"Événement créé avec succès : {event_response}")
except Exception as e:
    print(f"Erreur lors de la création de l'événement : {e}")