from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy


class GenderChoices(models.TextChoices):
    MALE = "M", gettext_lazy("Male")
    FEMALE = "F", gettext_lazy("Female")
    NON_BINARY = "NB", gettext_lazy("Non-Binary")
    OTHER = "O", gettext_lazy("Other")
    CUSTOM = "C", gettext_lazy("Custom")


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    age = models.IntegerField()

    gender = models.CharField(
        max_length=2,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
    )
    gender_custom = models.CharField(max_length=50, blank=True)

    interests = models.TextField(max_length=1000)
    emotional_profile = models.TextField(max_length=1000)
    bio_life = models.TextField(max_length=4000)
    bio_education = models.TextField(max_length=4000)
    bio_work = models.TextField(max_length=4000)
    bio_family = models.TextField(max_length=4000)
    bio_friends = models.TextField(max_length=4000)
    bio_pets = models.TextField(max_length=4000)
    bio_health = models.TextField(max_length=4000)

    def __str__(self):
        return self.user.name


class UserProfileCriticalEvent(models.Model):
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="critical_events"
    )
    date = models.DateField()
    description = models.TextField()
    impact = models.TextField()
    resolved = models.BooleanField(default=False)
    treated = models.BooleanField(default=False)

    def __str__(self):
        return f"Event on {self.date}: {self.description[:30]}..."
