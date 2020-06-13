from django.db import models


# Create your models here.
class User(models.Model):
    name_field = models.CharField(max_length=25)
    hash_field = models.CharField(max_length=61)

    def __str__(self):
        return self.name_field


class Category(models.Model):
    title_field = models.CharField(max_length=128)


class Challenge(models.Model):
    category_field = models.ForeignKey(Category, on_delete=models.CASCADE)
    title_field = models.CharField(max_length=128)
    file_field = models.CharField(max_length=1024)
    score_field = models.IntegerField(default=0)

    def __str__(self):
        return self.title_field


class Score(models.Model):
    user_field = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge_field = models.ForeignKey(Challenge, on_delete=models.CASCADE)
