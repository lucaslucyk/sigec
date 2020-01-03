from django.db import models
from django.urls import reverse

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from colorful.fields import RGBColorField

class Perfil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_title_font = models.CharField("Fuente de títulos", max_length=30, blank=True, default="Segoe UI Black")
    report_subtitle_font = models.CharField("Fuente de subtítulos", max_length=30, blank=True, default="Segoe UI Black")
    report_body_font = models.CharField("Fuente de cuerpo", max_length=30, blank=True, default="Segoe UI")

    report_color_title = RGBColorField("Color de títulos", default="#2B2B2B")
    report_bg_title = RGBColorField("Color de fondo de títuos", default="#008080")

    # birthdate = models.DateField(null=True, blank=True)
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile-update')#, kwargs={})

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()
