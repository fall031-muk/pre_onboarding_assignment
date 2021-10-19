from django.db import models
from django.db.models.deletion import CASCADE

class Post(models.Model):
    username       = models.CharField(max_length=45)
    title          = models.CharField(max_length=45)
    content        = models.TextField()
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"