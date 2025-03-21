from django.db import models
from django.conf import settings


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvoted_tips", blank=True)
    downvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvoted_tips", blank=True)

    # create custome permission
    class Meta:
        permissions = [
            ("can_downvote_tip", "Can downvote tip"),
        ]

    def __str__(self):
        return f"{self.content[:20]} by {self.author}"

    @property
    def upvote_count(self):
        return self.upvoters.count()

    @property
    def downvote_count(self):
        return self.downvoters.count()
