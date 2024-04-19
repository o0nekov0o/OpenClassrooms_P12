from Website_CRM import models
from rest_framework import serializers
from django.contrib.auth.models import Permission

url = serializers.HyperlinkedIdentityField(view_name="campaigns:promotion-detail", read_only=True)


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = []


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Customer
        exclude = ['information', 'full_name', 'email', 'phone_number',
                   'enterprise_name', 'commercial_contact', 'url']


class CrmUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CRM_User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'collaborator_type', 'url']


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contract
        fields = ['customer', 'commercial_contact', 'total_amount',
                  'unpaid_amount', 'creation_date', 'contract_state', 'url']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Event
        fields = ['contract', 'customer_name', 'customer_contact', 'event_start_date',
                  'event_end_date', 'support_contact', 'location', 'attendees', 'notes', 'url']
