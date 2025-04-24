from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

class BibleVerse(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.PositiveSmallIntegerField()
    chapter = models.PositiveSmallIntegerField()
    verse = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        db_table = 'bible_verses_kjv'
        managed = False
        ordering = ['book', 'chapter', 'verse']

    def __str__(self):
        return f"{self.book}:{self.chapter}:{self.verse}"

class Highlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    verse = models.ForeignKey(BibleVerse, on_delete=models.CASCADE)  # <-- ADD THIS LINE
    text = models.TextField()
    book = models.CharField(max_length=50)
    chapter = models.IntegerField()
    verse_number = models.IntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20, default='yellow')  # <-- Also needed if you're passing 'color'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    verse = models.ForeignKey(BibleVerse, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)  # Add group field
    created_at = models.DateTimeField(auto_now_add=True)
