from django.db import models
from organizations.models import Organization


class Team(Organization):
    sport = models.CharField(max_length=100, blank=True, null=True)
