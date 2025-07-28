class SecretManagerError(Exception):
    "Class to handle errors for secret manager service."

    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        "Message detail error."
        return f"[Secret Manager Error] {self.message or 'No details.'}"
