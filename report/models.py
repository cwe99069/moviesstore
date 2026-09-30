from django.db import models
from django.contrib.auth.models import User
from movies.models import Review
# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - Review: ' + f'{self.review.id}'

    def delete(self, *args, **kwargs):
        self.review.reported=False
        self.review.save()
        super().delete(*args, **kwargs)