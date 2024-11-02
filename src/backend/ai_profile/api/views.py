"""User Profile API views."""

from __future__ import annotations

from typing import cast

from mhai_web.users.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ai_profile.api.serializers import (
    AIProfileBiographySerializer,
    AIProfileEmotionsSerializer,
    AIProfileGeneralInfoSerializer,
    AIProfileInterestsSerializer,
)
from ai_profile.models import AIProfile


class AIProfileGeneralInfoView(viewsets.ModelViewSet):
    """ViewSet for updating general information in the AIProfile model."""

    queryset = AIProfile.objects.all()
    serializer_class = AIProfileGeneralInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class AIProfileInterestsView(viewsets.ModelViewSet):
    """ViewSet for updating interests in the AIProfile model."""

    queryset = AIProfile.objects.all()
    serializer_class = AIProfileInterestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class AIProfileEmotionsView(viewsets.ModelViewSet):
    """ViewSet for updating the emotional profile in the AIProfile model."""

    queryset = AIProfile.objects.all()
    serializer_class = AIProfileEmotionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))


class AIProfileBiographyView(viewsets.ModelViewSet):
    """ViewSet for updating bio-related fields in the AIProfile model."""

    queryset = AIProfile.objects.all()
    serializer_class = AIProfileBiographySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=cast(User, self.request.user))
