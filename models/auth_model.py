from msal import PublicClientApplication



class Auth:
    def __init__(self, client_id: str, scopes: list):
        self.client_id = client_id
        self.scopes = scopes
        self.device_code = None 
        self.access_token = None

    def initiate_auth_flow(self) -> dict:
        app = PublicClientApplication(
            self.client_id,
            authority="https://login.microsoftonline.com/common",
        )
        flow = app.initiate_device_flow(scopes=self.scopes)

        if not flow or "user_code" not in flow:
            raise Exception("Erreur lors de l'initialisation du flux d'authentification.")

        # Stocke le device_code côté backend
        self.device_code = flow["device_code"]

        # Ne renvoie que les données nécessaires au frontend
        return {
            "user_code": flow["user_code"],
            "verification_url": flow["verification_uri"],
            "message": flow["message"],
        }

    def acquire_token(self) -> str:
        if not self.device_code:
            raise Exception("Le device_code n'a pas été initialisé. Veuillez lancer 'initiate_auth_flow' d'abord.")

        app = PublicClientApplication(
            self.client_id,
            authority="https://login.microsoftonline.com/common",
        )
        result = app.acquire_token_by_device_flow({"device_code": self.device_code})

        if "access_token" in result:
            self.access_token = result["access_token"]
            return self.access_token
        else:
            raise Exception(f"Erreur MSAL : {result.get('error_description', 'Erreur inconnue')}")

