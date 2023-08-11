from django.db import models


class Category(models.Model):
	title = models.CharField(max_length=50, null=False)
	image = models.ImageField(upload_to='category')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
