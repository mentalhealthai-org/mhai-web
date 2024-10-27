"""User Profile API views."""

from __future__ import annotations

from typing import cast

from mhai_web.users.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from user_profile.api.serializers import (
    UserProfileBiographySerializer,
    UserProfileCriticalEventSerializer,
    UserProfileEmotionsSerializer,
    UserProfileGeneralInfoSerializer,
    UserProfileInterestsSerializer,
)
from user_profile.models import UserProfile, UserProfileCriticalEvent


class UserProfileGeneralInfoView(viewsets.ModelViewSet):
    """ViewSet for updating general information in the UserProfile model."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileGeneralInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class UserProfileInterestsView(viewsets.ModelViewSet):
    """ViewSet for updating interests in the UserProfile model."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileInterestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class UserProfileEmotionsView(viewsets.ModelViewSet):
    """ViewSet for updating the emotional profile in the UserProfile model."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileEmotionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class UserProfileBiographyView(viewsets.ModelViewSet):
    """ViewSet for updating bio-related fields in the UserProfile model."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileBiographySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class UserProfileCriticalEventView(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on the UserProfileCriticalEvent model."""

    queryset = UserProfileCriticalEvent.objects.all()
    serializer_class = UserProfileCriticalEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            profile__user=cast(User, self.request.user)
        )
