from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf.urls.static import static
from django.core.exceptions import ValidationError
from django.dispatch import receiver
import os
from stock.models import InstituteName

def validate_image(fieldfile_obj):
    
    filesize = fieldfile_obj.file.size
    kilobyte_limit = 100.0
    if filesize > kilobyte_limit*1024:
        raise ValidationError("Max file size that can be uploaded is %sKB" % str(kilobyte_limit))

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True,
    validators=[validate_image], help_text='Maximum file size allowed is 100KB')
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        if not self.avatar:
            return static('AdminPanel/assets/img/avtar.png')
        return self.avatar.url

        #return self.avatar.url if self.avatar else static('AdminPanel/assets/img/avtar.png')

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)
        
# Deletes old file from filesystem when corresponding `MediaFile` object is updated with new file. Model:ItemPurchase
@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_file = instance.avatar
    if old_file == "":
        pass
    else:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# Deletes file from filesystem when corresponding `MediaFile` object is deleted. Model:Profile
@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
