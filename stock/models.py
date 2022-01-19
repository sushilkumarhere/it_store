from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
import os

# Create your models here.

class YourBaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def validate_image(fieldfile_obj):
    
    filesize = fieldfile_obj.file.size
    kilobyte_limit = 300.0
    if filesize > kilobyte_limit*1024:
        raise ValidationError("Max file size that can be uploaded is %sKB" % str(kilobyte_limit))


def validate_file_size(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    kilobyte_limit = 1024*1024  #1024 byte X 1024 = 1MB
    if filesize > kilobyte_limit:
        raise ValidationError("Max file size that can be uploaded is %sKB" % str(kilobyte_limit))
    else:
        return fieldfile_obj


class ItemName(models.Model):
    item_name = models.CharField(max_length=100)
    item_image=models.ImageField(upload_to='item-pic',validators=[validate_image], 
    blank=True,help_text='Maximum file size allowed is 100KB')
    
    def __str__(self):
        return self.item_name

    def delete(self, using=None, keep_parents=False):
        #self.song.storage.delete(self.song.name)         #file delete
        self.item_image.storage.delete(self.item_image.name)  # image delete when delete items
        super().delete()

    class Meta:
        ordering = ["item_name"]

# Deletes old file from filesystem when corresponding `MediaFile` object is updated with new file. Model:ItemName
@receiver(models.signals.pre_save, sender=ItemName)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).item_image
    except sender.DoesNotExist:
        return False

    new_file = instance.item_image
    if old_file == "":
        pass
    else:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# Deletes file from filesystem when corresponding `MediaFile` object is deleted. Model:ItemName
@receiver(models.signals.post_delete, sender=ItemName)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.item_image:
        if os.path.isfile(instance.item_image.path):
            os.remove(instance.item_image.path)


class InstituteName(models.Model):
    Inst_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Inst_name

    class Meta:
        ordering = ["Inst_name"]


class ItemModel(models.Model):
    item_name = models.ForeignKey(ItemName, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name
        # return '%s %s' % (self.item_name, self.model_name)



class ac_block(models.Model):
    name = models.CharField(max_length=100)

    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
       



class RoomType(models.Model):
    room_type = models.CharField(max_length=100)

    def __str__(self):
        return self.room_type

    class Meta:
        ordering = ["room_type"]


class ItemDist(models.Model):
    item_name = models.ForeignKey(ItemName, on_delete=models.CASCADE)
    item_model = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    #item_sl = models.CharField(max_length=100)
    item_configuration = models.CharField("Items Specifications", max_length=100)
    purchase_date = models.DateField(null=True,blank=True)
    acblock = models.ForeignKey(ac_block, on_delete=models.CASCADE, verbose_name="Academic Block", null=True)
    room = models.CharField(max_length=100, verbose_name="Room No")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    inst = models.ForeignKey(InstituteName, on_delete=models.CASCADE, null=True, verbose_name="Institute Name")
    user = models.CharField(max_length=100, blank=True)
    item_qty = models.IntegerField()
    act = models.IntegerField(default=0,editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item Distribution"


class ItemPurchase(models.Model):
    item_purchase_date = models.DateField()
    item_name = models.ForeignKey(ItemName, on_delete=models.CASCADE )
    item_model = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    item_sl = models.CharField(max_length=100)
    item_configuration = models.CharField("Items Specifications", max_length=100)
    item_vendor = models.CharField("Vendor Name",max_length=100)
    item_invoice = models.CharField("Invoice No",max_length=100)
    item_invoice_file = models.FileField(upload_to='invoice', validators=[validate_file_size],
    blank=True,help_text='Maximum file size allowed is 300KB')
    item_price = models.CharField("Price",max_length=100)
    item_qty = models.IntegerField()

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Item Purchase"
    def delete(self, *args, **kwargs):
        self.item_invoice_file.delete()
        super().delete(*args, **kwargs)
        
# Deletes old file from filesystem when corresponding `MediaFile` object is updated with new file. Model:ItemPurchase
@receiver(models.signals.pre_save, sender=ItemPurchase)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).item_invoice_file
    except sender.DoesNotExist:
        return False

    new_file = instance.item_invoice_file
    if old_file == "":
        pass
    else:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# Deletes file from filesystem when corresponding `MediaFile` object is deleted. Model:ItemPurchase
@receiver(models.signals.post_delete, sender=ItemPurchase)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.item_invoice_file:
        if os.path.isfile(instance.item_invoice_file.path):
            os.remove(instance.item_invoice_file.path)


# Update user Profile 