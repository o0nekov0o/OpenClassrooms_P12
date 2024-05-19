from Website_CRM import models
from rest_framework import serializers
from django.contrib.auth.models import Permission

url = serializers.HyperlinkedIdentityField(view_name="campaigns:promotion-detail", read_only=True)


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = []


class CrmUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CRM_User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'collaborator_type', 'url']


class FilterForCustomer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.CRM_User.objects.filter(collaborator_type=1)


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    commercial_contact = FilterForCustomer(many=False)

    class Meta:
        model = models.Customer
        fields = ['information', 'full_name', 'email', 'phone_number',
                  'enterprise_name', 'commercial_contact', 'url']


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contract
        fields = ['customer', 'commercial_contact', 'total_amount',
                  'unpaid_amount', 'contract_state', 'url']
        extra_kwargs = {'commercial_contact': {'read_only': True}, }


class FilterForEvent(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.CRM_User.objects.filter(collaborator_type=2)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    support_contact = FilterForEvent(many=False)

    class Meta:
        model = models.Event
        fields = ['contract', 'customer_name', 'customer_contact', 'event_start_date',
                  'event_end_date', 'support_contact', 'location', 'attendees', 'notes', 'url']
        extra_kwargs = {'customer_name': {'read_only': True}, 'customer_contact': {'read_only': True}, }

    """def to_representation(self, instance):
        rep = super(EventSerializer, self).to_representation(instance)
        rep['contract'] = instance.contract.customer.email
        return rep"""
