from django.db import models


class User(models.Model):
    uid = models.CharField(max_length=45)
    password = models.CharField(max_length=250)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    challenge_completed = models.IntegerField(default=0)
    accumulated_points = models.IntegerField(default=0)
    state = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "tb_user"


class ChallengeDetail(models.Model):
    challenge_description = models.CharField(max_length=255)
    shared_challenge_status = models.IntegerField()
    approved_shared_challenge = models.IntegerField()
    challenge_content = models.CharField(max_length=150)

    class Meta:
        db_table = "tb_detail_challenges"

    def __str__(self):
        return self.challenge_name


class Challenge(models.Model):
    challenge_detail = models.ForeignKey(
        ChallengeDetail, on_delete=models.CASCADE, null=True, blank=True
    )
    challenge_name = models.CharField(max_length=255)
    challenge_points = models.IntegerField()
    challenge_time = models.DateTimeField()
    challenge_type = models.CharField(max_length=100)
    state = models.IntegerField(default=1)

    class Meta:
        db_table = "tb_challenges"

    def __str__(self):
        return self.challenge_name


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_user_challenges"
        unique_together = [
            "user",
            "challenge",
        ]

    def __str__(self):
        return f"{self.user.username} - {self.challenge.challenge_name}"
