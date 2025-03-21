from django.db import models
from django.contrib.auth.models import User


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvoters = models.ManyToManyField(User, related_name="upvoted_tips", blank=True)
    downvoters = models.ManyToManyField(User, related_name="downvoted_tips", blank=True)

    def __str__(self):
        # 管理画面などで表示される文字列表現
        return f"{self.content[:20]} by {self.author}"

    def upvote_count(self):
        return self.upvoters.count()

    def downvote_count(self):
        return self.downvoters.count()
