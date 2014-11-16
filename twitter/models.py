from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.text
