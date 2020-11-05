from django.db import models

# Create your models here.
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    # title = models.TextField(null=True, blank=True)
    # cover = models.ImageField(upload_to='images/', null=True, blank=True)
    bucket_url = models.TextField()
    cathegory = models.CharField(null=True, blank=True, max_length=50)
    # created = models.DateField(auto_now_add=True)
    # modified = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.image_id)
