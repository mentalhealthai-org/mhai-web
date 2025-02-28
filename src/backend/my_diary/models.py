from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MyDiary(models.Model):
    """
    Model representing a message within a chat room.
    """

    class StatusChoices(models.TextChoices):
        STARTED = "started", "Started"
        IN_PROGRESS = "in-progress", "In Progress"
        COMPLETED = "completed", "Completed"
        ERROR = "error", "Error"

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    prompt = models.TextField()
    prompt_timestamp = models.DateTimeField(auto_now_add=True)
    response = models.TextField()
    response_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.STARTED,
    )

    class Meta:
        ordering = ["-prompt_timestamp"]

    def __str__(self):
        return f"MyDiary ({self.user}): {self.prompt_timestamp} / #{self.id}"


class MhaiDiaryEvalMentBert(models.Model):
    """
    Store the scores from MentBert analysis from patient messsage.

    Ref: https://huggingface.co/reab5555/mentBERT
    """

    my_diary = models.ForeignKey(MyDiary, null=False, on_delete=models.CASCADE)
    borderline = models.FloatField()
    anxiety = models.FloatField()
    depression = models.FloatField()
    bipolar = models.FloatField()
    ocd = models.FloatField()
    adhd = models.FloatField()
    schizophrenia = models.FloatField()
    asperger = models.FloatField()
    ptsd = models.FloatField()

    def __str__(self):
        return f"MhaiDiaryEvalMentBert ({self.my_diary.user}) #{self.id}"


class MhaiDiaryEvalPsychBert(models.Model):
    """
    Store the scores from PsychBert analysis from patient messages.

    Ref: https://huggingface.co/mnaylor/psychbert-finetuned-multiclass
    """

    my_diary = models.ForeignKey(MyDiary, null=False, on_delete=models.CASCADE)
    unrelated = models.FloatField()
    mental_illnesses = models.FloatField()
    anxiety = models.FloatField()
    depression = models.FloatField()
    social_anxiety = models.FloatField()
    loneliness = models.FloatField()

    def __str__(self):
        return f"MhaiDiaryEvalPsychBert ({self.my_diary.user}) #{self.id}"


class MhaiDiaryEvalEmotions(models.Model):
    """
    Store the scores from Emotion analysis from patient messages.

    Ref: j-hartmann/emotion-english-distilroberta-base
    """

    my_diary = models.ForeignKey(MyDiary, null=False, on_delete=models.CASCADE)
    neutral = models.FloatField()
    joy = models.FloatField()
    disgust = models.FloatField()
    sadness = models.FloatField()
    anger = models.FloatField()
    surprise = models.FloatField()
    fear = models.FloatField()

    def __str__(self):
        return f"MhaiDiaryEvalEmotions ({self.my_diary.user}) #{self.id}"
