from rest_framework import serializers
from .models import ChallengeDetail, User, Challenge


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "password",
            "challenge_completed",
            "accumulated_points",
            "email",
            "fullname",
            "state",
            "date_created",
        ]


class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeDetail
        fields = [
            "challenge_description",
            "shared_challenge_status",
            "approved_shared_challenge",
            "challenge_content",
        ]


class ChallengeSerializer(serializers.ModelSerializer):
    challenge_description = serializers.CharField(
        source="challenge_detail.challenge_description", read_only=True
    )
    shared_challenge_status = serializers.IntegerField(
        source="challenge_detail.shared_challenge_status", read_only=True
    )
    approved_shared_challenge = serializers.IntegerField(
        source="challenge_detail.approved_shared_challenge", read_only=True
    )
    challenge_content = serializers.CharField(
        source="challenge_detail.challenge_content", read_only=True
    )

    class Meta:
        model = Challenge
        fields = [
            "id",
            "challenge_name",
            "challenge_points",
            "challenge_time",
            "challenge_type",
            "state",
            "challenge_description",
            "shared_challenge_status",
            "approved_shared_challenge",
            "challenge_content",
        ]
