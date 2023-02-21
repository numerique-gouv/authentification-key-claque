from django.core.validators import URLValidator
from django.db import models


class Client(models.Model):
    """OIDC Client"""

    name = models.CharField("Nom", max_length=200)
    client_id = models.CharField("Identifiant", max_length=100, unique=True)
    client_secret = models.CharField("Secret", max_length=100)


class RedirectUri(models.Model):
    """Redirect URI allowed for a given client"""

    name = models.CharField("Nom", max_length=255)
    uri = models.CharField(
        "Uri",
        max_length=1000,
        validators=[URLValidator(schemes=("http", "https", "ftp", "ftps"))],
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
