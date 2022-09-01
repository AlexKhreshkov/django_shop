from model_utils import Choices
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_by_category', args=[self.slug])


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField()
    description = RichTextField()
    image = models.ImageField()
    mark = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_item', args=[self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profiles_images/",
                                    default="profiles_images/ava.png")

    def __str__(self):
        return f"User {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Order(models.Model):
    allowed_statuses = Choices('formed', 'approved', 'done')
    allowed_issue_points = Choices('Kiev, str. Peremohi 12', 'Kharkiv, str. Klochkovskay 123')
    status = models.CharField(max_length=15, choices=allowed_statuses, default=allowed_statuses.formed)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    issue_point = models.CharField(max_length=50, choices=allowed_issue_points, blank=True)
    delivery_address = models.CharField(max_length=50, blank=True)
    total_cost = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return f"Order №{self.id}"


class RatingMark(models.Model):
    mark = models.SmallIntegerField()

    def __str__(self):
        return f"{self.mark}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    mark = models.ForeignKey(RatingMark, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment on: {self.item} by {self.user}"
