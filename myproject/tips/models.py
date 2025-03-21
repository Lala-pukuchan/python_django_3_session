from django.db import models
from django.contrib.auth.models import User


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvoters = models.ManyToManyField(User, related_name="upvoted_tips", blank=True)
    downvoters = models.ManyToManyField(User, related_name="downvoted_tips", blank=True)

    # create custome permission
    class Meta:
        permissions = [
            ("can_downvote_tip", "Can downvote tip"),
        ]

    def __str__(self):
        return f"{self.content[:20]} by {self.author}"

    def upvote_count(self):
        return self.upvoters.count()

    def downvote_count(self):
        return self.downvoters.count()
