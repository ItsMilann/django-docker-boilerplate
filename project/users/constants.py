from django.db.models import TextChoices

class Roles(TextChoices):
    SUPERUSER = "superuser", "superuser"
    CDADMIN = "cd_admin", "cd_admin"
    RESOURCE_PERSON = "resource_person", "resource_person"
    PARTICIPANT = "participant", "participant"
