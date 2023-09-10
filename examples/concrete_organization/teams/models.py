from django.db import models

from organizations.models import Organization


class Department(Organization):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    notes = models.TextField(blank=True, default="")
