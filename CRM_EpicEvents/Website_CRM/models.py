from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


class CRM_User(AbstractUser):
    creator = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=False)
    COLLABORATOR_CHOICES = ((0, 'Management Collaborator'),
                            (1, 'Commercial Collaborator'),
                            (2, 'Support Collaborator'))
    collaborator_type = models.IntegerField(choices=COLLABORATOR_CHOICES, default=1, null=True, blank=False)


class Customer(models.Model):
    creator = models.ForeignKey(to=CRM_User, on_delete=models.CASCADE,
                                null=True, blank=False)
    information = models.TextField(max_length=2048, null=True, blank=True)
    full_name = models.CharField(max_length=128, null=False, blank=False)
    email = models.EmailField(max_length=128, null=False, blank=False)
    phone_number = PhoneNumberField(region="FR", null=False, blank=False)
    enterprise_name = models.CharField(max_length=128, null=False, blank=False, )
    creation_date = models.DateField("Date", auto_now_add=True)
    last_update = models.DateField("Date", auto_now=True)
    commercial_contact = models.ForeignKey(to=CRM_User, on_delete=models.CASCADE,
                                           related_name='customer_abstract_commercial')


class Contract(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                 related_name='contract_customer_all')
    commercial_contact = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                           related_name='contract_customer_contact',
                                           default='customer.commercial_contact')
    total_amount = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    unpaid_amount = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    creation_date = models.DateField("Date", auto_now_add=True)
    STATE_CHOICES = ((0, 'Not Signed'),
                     (1, 'Signed'),)
    contract_state = models.IntegerField(choices=STATE_CHOICES, default=0, null=False, blank=False)


class Event(models.Model):
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                      related_name='event_customer_name',
                                      default='contract.customer.full_name')
    customer_contact = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                         related_name='event_customer_contact',
                                         default='contract.customer.commercial_contact')
    event_start_date = models.DateTimeField(null=False, blank=False)
    event_end_date = models.DateTimeField(null=False, blank=False)
    support_contact = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                        related_name='event_contact', null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, null=False, blank=False)
    attendees = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=2048, null=True, blank=True)
