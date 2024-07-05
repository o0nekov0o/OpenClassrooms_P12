from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class CRM_User(AbstractUser):
    creator = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=False)
    COLLABORATOR_CHOICES = ((0, 'Management Collaborator'),
                            (1, 'Commercial Collaborator'),
                            (2, 'Support Collaborator'))
    collaborator_type = models.IntegerField(choices=COLLABORATOR_CHOICES, default=1, null=True, blank=False)


class Customer(models.Model):
    creator = models.ForeignKey(to=CRM_User, on_delete=models.CASCADE, null=True, blank=False)
    information = models.TextField(max_length=2048, null=True, blank=True)
    full_name = models.CharField(max_length=128, null=False, blank=False)
    email = models.EmailField(max_length=128, null=False, blank=False, unique=True)
    phone_number = models.CharField(null=False, blank=False, max_length=12)
    enterprise_name = models.CharField(max_length=128, null=False, blank=False, )
    creation_date = models.DateField("Date", auto_now_add=True)
    last_update = models.DateField("Date", auto_now=True)
    commercial_contact = models.ForeignKey(to=CRM_User, on_delete=models.CASCADE,
                                           related_name='customer_commercial_contact')

    def __str__(self):
        return "|| name : " + str(self.full_name) + " ||  mail : " + str(self.email) + " ||"


class Contract(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    commercial_contact = models.CharField(max_length=128, null=False, blank=True)
    email = models.EmailField(max_length=128, null=False, blank=True)
    total_amount = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    unpaid_amount = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField("Date", auto_now_add=True)
    STATE_CHOICES = ((0, 'Not Signed'),
                     (1, 'Signed'),)
    contract_state = models.IntegerField(choices=STATE_CHOICES, default=0, null=False, blank=False)

    def __str__(self):
        return "|| created on : " + str(self.creation_date) + " || for user : " + str(self.email) + " ||"


@receiver(post_save, sender=Contract)
def auto_create_commercial_contact(instance, **kwargs):
    """
    Anytime a Contract object is created, associate customer data thanks to customer
    """
    if kwargs.get('created', False):
        if instance.customer:
            instance.commercial_contact = instance.customer.commercial_contact.username
            instance.email = instance.customer.email
            instance.save(update_fields=['commercial_contact', 'email'])


class Event(models.Model):
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=128, null=False, blank=True)
    customer_contact = models.CharField(max_length=128, null=False, blank=True)
    event_start_date = models.DateTimeField(null=False, blank=False)
    event_end_date = models.DateTimeField(null=False, blank=False)
    support_contact = models.ForeignKey(to=CRM_User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(null=False, blank=False, max_length=12)
    attendees = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=2048, null=True, blank=True)


@receiver(post_save, sender=Event)
def auto_create_customer_data(instance, **kwargs):
    """
    Anytime an Event object is created, associate customer data thanks to customer
    """
    if kwargs.get('created', False):
        if instance.contract:
            instance.customer_name = instance.contract.customer.full_name
            instance.customer_contact = instance.contract.customer.commercial_contact.username
            instance.save(update_fields=['customer_name', 'customer_contact'])
