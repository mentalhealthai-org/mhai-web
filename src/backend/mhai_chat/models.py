from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MhaiChat(models.Model):
    """
    Model representing a message within a chat room.
    """

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    user_input = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"MhaiChat ({self.user.name}): {self.timestamp} / #{self.id}"


class MhaiChatEvalMentBert(models.Model):
    """
    Store the scores from MentBert analysis from patient messsage.

    Ref: https://huggingface.co/reab5555/mentBERT
    """

    mhai_chat = models.ForeignKey(
        MhaiChat, null=True, on_delete=models.CASCADE
    )
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
        return f"MhaiChatEvalMentBert ({self.mhai_chat.user.name}) #{self.id}"


class MhaiChatEvalPsychBert(models.Model):
    """
    Store the scores from PsychBert analysis from patient messages.

    Ref: https://huggingface.co/mnaylor/psychbert-finetuned-multiclass
    """

    mhai_chat = models.ForeignKey(
        MhaiChat, null=True, on_delete=models.CASCADE
    )
    unrelated = models.FloatField()
    mental_illnesses = models.FloatField()
    anxiety = models.FloatField()
    depression = models.FloatField()
    social_anxiety = models.FloatField()
    loneliness = models.FloatField()

    def __str__(self):
        return f"MhaiChatEvalPsychBert ({self.mhai_chat.user.name}) #{self.id}"


class MhaiChatEvalEmotions(models.Model):
    """
    Store the scores from Emotion analysis from patient messages.

    Ref: j-hartmann/emotion-english-distilroberta-base
    """

    mhai_chat = models.ForeignKey(
        MhaiChat, null=True, on_delete=models.CASCADE
    )
    neutral = models.FloatField()
    joy = models.FloatField()
    disgust = models.FloatField()
    sadness = models.FloatField()
    anger = models.FloatField()
    surprise = models.FloatField()
    fear = models.FloatField()

    def __str__(self):
        return f"MhaiChatEvalEmotions ({self.mhai_chat.user.name}) #{self.id}"
