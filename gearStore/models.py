import string
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
import random

WHATSAPP = 'logo-whatsapp'
PHONE = 'call-outline'
EMAIL = 'mail-outline'

CONTACT_CHOICES = (
    (WHATSAPP, 'WhatsApp'),
    (PHONE, 'Phone Number'),
    (EMAIL, 'Email'),
)


# define a method to generate a random id not in use
def id_generator():
    ID_LENGTH = 6
    # define a string to hold the id
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=ID_LENGTH))
    try:
        booking = Booking.objects.get(id=id)
        print("Booking ID already exists. Creating new ID.")
        return id_generator()
    except Booking.DoesNotExist:
        print("Booking ID is valid.")
        return id


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to="category_images", default="category_images/default.png")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adminStatus = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, default="Jane")
    last_name = models.CharField(max_length=30, default="Doe")
    picture = models.ImageField(upload_to='profile_images', default="profile_images/default.jpeg")

    def __str__(self):
        return self.user.username


class Gear(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to="gear_images", default="gear_images/default.png")
    size = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Gear"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Gear, self).save(*args, **kwargs)


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)


class Booking(models.Model):
    id = models.TextField(max_length=6, primary_key=True, default=id_generator)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    gearItem = models.ForeignKey(Gear, on_delete=models.CASCADE)
    dateBorrowed = models.DateField(auto_now_add=True)
    dateToReturn = models.DateField(default=return_date_time)

    def __str__(self):
        return f"{self.user.user.username} booking of {self.gearItem.name}"

    def is_current(self):
        if self.dateToReturn >= timezone.now().date():
            return True
        return False


class AdminPassword(models.Model):
    password = models.CharField(max_length=64, default="password123")

    def __str__(self):
        return self.password


class PageContents(models.Model):
    background_image = models.ImageField(upload_to="site_images", default="site_images/default_background.jpg")
    logo_image = models.ImageField(upload_to="site_images", default="site_images/default_logo.png")
    home_contents = models.TextField()
    about_contents = models.TextField()
    contact_contents = models.TextField()
    contact = models.CharField(max_length=128)
    contact_option = models.CharField(max_length=128, choices=CONTACT_CHOICES, default=PHONE)
    title = models.TextField(default="Gear Store")
