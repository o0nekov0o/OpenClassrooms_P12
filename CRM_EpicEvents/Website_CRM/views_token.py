from django.db.models import Q
from Website_CRM import models, serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password
from rest_framework import authentication, permissions, views, response, status
from rest_framework.decorators import authentication_classes, permission_classes


class NonExistantUser(permissions.BasePermission):
    """
    Just make sure nobody can access PermissionView.
    """

    def has_permission(self, request, view):
        if request.user.pk == -1:
            return True
        return False


class IsSuperUserOrCollaborator(permissions.BasePermission):
    """
    Ensure only admins and the management team can perform certain actions.
    Then Views that use this permission class can reduce authorizations.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']:
            if request.user.is_superuser:
                return True
            if request.user.collaborator_type in [0, 1, 2]:
                return True
            return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.collaborator_type == 0 and obj.collaborator_type in [0, 1, 2]:
            return True
        if request.user.collaborator_type == 1 and obj.collaborator_type == 1:
            return True
        if request.user.collaborator_type == 2 and obj.collaborator_type == 2:
            return True
        if request.user.collaborator_type in [0, 1] and hasattr(obj, 'enterprise_name'):
            return True
        if request.user.collaborator_type in [0, 1] and hasattr(obj, 'contract_state'):
            return True
        if request.user.collaborator_type in [0, 1, 2] and hasattr(obj, 'event_start_date'):
            return True
        return False


class PermissionView(views.APIView):
    """
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    permission_classes = [NonExistantUser]


@permission_classes([IsSuperUserOrCollaborator])
@authentication_classes([authentication.TokenAuthentication])
class CustomerView(views.APIView):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    queryset = models.Customer.objects.all().order_by('-pk')
    serializer_class = serializers.CustomerSerializer
    permission_classes = [IsSuperUserOrCollaborator]

    def get_object(self, customer_id):
        return get_object_or_404(self.queryset, id=customer_id)

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs
        if customer_id:
            serializer_context = {'request': request}
            serializer = serializers.CustomerSerializer(
                self.get_object(customer_id['pk']), context=serializer_context)
        else:
            serializer_context = {'request': request}
            serializer = serializers.CustomerSerializer(
                models.Customer.objects.order_by('-pk'), context=serializer_context, many=True)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(self.kwargs['pk'])
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or instance.creator == request.user:
            instance.__class__.objects.get(pk=instance.pk).delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(self.kwargs['pk'])
        serializer = serializers.CustomerSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        changed_customer = serializer.validated_data
        information, full_name, email, phone_number, enterprise_name, commercial_contact = \
            changed_customer['information'], changed_customer['full_name'], \
            changed_customer['email'], changed_customer['phone_number'], \
            changed_customer['enterprise_name'], changed_customer['commercial_contact']
        if information == '' or full_name == '' or email == '' or phone_number == '' \
                or enterprise_name == '' or commercial_contact == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not email == instance.email:
            if models.Customer.objects.filter(Q(email=email)):
                return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not phone_number == instance.phone_number:
            if models.Customer.objects.filter(Q(phone_number=phone_number)):
                return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or instance.creator == request.user:
            serializer.save()
            return response.Response(status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomerSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        new_customer = serializer.validated_data
        information, full_name, email, phone_number, enterprise_name, commercial_contact = \
            new_customer['information'], new_customer['full_name'], \
            new_customer['email'], new_customer['phone_number'], \
            new_customer['enterprise_name'], new_customer['commercial_contact']
        if information == '' or full_name == '' or email == '' or phone_number == '' \
                or enterprise_name == '' or commercial_contact == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if models.Customer.objects.filter(Q(email=email) | Q(phone_number=phone_number)):
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type in [0, 1]:
            models.Customer.objects.create(information=information, full_name=full_name, email=email,
                                           phone_number=phone_number, enterprise_name=enterprise_name,
                                           commercial_contact=commercial_contact, creator=request.user)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsSuperUserOrCollaborator])
@authentication_classes([authentication.TokenAuthentication])
class CrmUserView(views.APIView):
    """
    API endpoint that allows crm_users to be viewed or edited.
    """
    queryset = models.CRM_User.objects.all().order_by('-pk')
    serializer_class = serializers.CrmUserSerializer
    permission_classes = [IsSuperUserOrCollaborator]

    def get_object(self, user_id):
        return get_object_or_404(self.queryset, id=user_id)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs
        if user_id:
            serializer_context = {'request': request}
            serializer = serializers.CrmUserSerializer(
                self.get_object(user_id['pk']), context=serializer_context)
        else:
            serializer_context = {'request': request}
            serializer = serializers.CrmUserSerializer(
                models.CRM_User.objects.order_by('-pk'), context=serializer_context, many=True)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(self.kwargs['pk'])
        if instance.is_superuser and not request.user.is_superuser:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or instance.creator == request.user \
                or instance == request.user and request.user.collaborator_type == 0 \
                or instance.collaborator_type in [1, 2] and request.user.collaborator_type == 0:
            instance.__class__.objects.get(pk=instance.pk).delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(self.kwargs['pk'])
        serializer = serializers.CrmUserSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.is_superuser and not request.user.is_superuser:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        changed_crm_user = serializer.validated_data
        username, password, first_name, last_name, email, collaborator_type = \
            changed_crm_user['username'], changed_crm_user['password'], changed_crm_user['first_name'], \
            changed_crm_user['last_name'], changed_crm_user['email'], changed_crm_user['collaborator_type']
        if username == '' or password == '' or first_name == '' \
                or last_name == '' or email == '' or collaborator_type is None:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not username == instance.username:
            if models.CRM_User.objects.filter(Q(username=username)):
                return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not email == instance.email:
            if models.CRM_User.objects.filter(Q(email=email)):
                return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or instance.creator == request.user \
                or instance == request.user and request.user.collaborator_type == 0 \
                or instance.collaborator_type in [1, 2] and request.user.collaborator_type == 0:
            password = serializer.validated_data['password']
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return response.Response(status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CrmUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        new_crm_user = serializer.validated_data
        username, password, first_name, last_name, email, collaborator_type = \
            new_crm_user['username'], new_crm_user['password'], new_crm_user['first_name'], \
            new_crm_user['last_name'], new_crm_user['email'], new_crm_user['collaborator_type']
        if username == '' or password == '' or first_name == '' \
                or last_name == '' or email == '' or collaborator_type is None:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if models.CRM_User.objects.filter(Q(username=username) | Q(email=email)):
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0:
            models.CRM_User.objects.create(username=username, password=make_password(password),
                                           first_name=first_name, last_name=last_name, creator=request.user,
                                           email=email, collaborator_type=collaborator_type)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsSuperUserOrCollaborator])
@authentication_classes([authentication.TokenAuthentication])
class ContractView(views.APIView):
    """
    API endpoint that allows contracts to be viewed or edited.
    """
    queryset = models.Contract.objects.all().order_by('-pk')
    serializer_class = serializers.ContractSerializer
    permission_classes = [IsSuperUserOrCollaborator]

    def get_object(self, contract_id):
        return get_object_or_404(self.queryset, id=contract_id)

    def get(self, request, *args, **kwargs):
        contract_id = self.kwargs
        if contract_id:
            serializer_context = {'request': request}
            serializer = serializers.ContractSerializer(
                self.get_object(contract_id['pk']), context=serializer_context)
        else:
            serializer_context = {'request': request}
            serializer = serializers.ContractSerializer(
                models.Contract.objects.order_by('-pk'), context=serializer_context, many=True)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(self.kwargs['pk'])
        if request.user.is_superuser or request.user.collaborator_type == 0:
            instance.__class__.objects.get(pk=instance.pk).delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(self.kwargs['pk'])
        serializer = serializers.ContractSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        changed_contract = serializer.validated_data
        customer, total_amount, unpaid_amount, contract_state = \
            changed_contract['customer'], changed_contract['total_amount'], \
            changed_contract['unpaid_amount'], changed_contract['contract_state']
        if customer == '' or total_amount == '' or unpaid_amount == '' or contract_state == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or instance.customer.creator == request.user:
            serializer.save()
            return response.Response(status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        serializer = serializers.ContractSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        new_contract = serializer.validated_data
        customer, total_amount, unpaid_amount, contract_state = \
            new_contract['customer'], new_contract['total_amount'], \
            new_contract['unpaid_amount'], new_contract['contract_state']
        if customer == '' or total_amount == '' or unpaid_amount == '' or contract_state == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0:
            models.Contract.objects.create(customer=customer, total_amount=total_amount,
                                           unpaid_amount=unpaid_amount, contract_state=contract_state)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsSuperUserOrCollaborator])
@authentication_classes([authentication.TokenAuthentication])
class EventView(views.APIView):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = models.Event.objects.all().order_by('-pk')
    serializer_class = serializers.EventSerializer
    permission_classes = [IsSuperUserOrCollaborator]

    def get_object(self, event_id):
        return get_object_or_404(self.queryset, id=event_id)

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs
        if event_id:
            serializer_context = {'request': request}
            serializer = serializers.EventSerializer(
                self.get_object(event_id['pk']), context=serializer_context)
        else:
            serializer_context = {'request': request}
            serializer = serializers.EventSerializer(
                models.Event.objects.order_by('-pk'), context=serializer_context, many=True)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(self.kwargs['pk'])
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or instance.contract.customer.creator == request.user:
            instance.__class__.objects.get(pk=instance.pk).delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(self.kwargs['pk'])
        serializer = serializers.EventSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        changed_event = serializer.validated_data
        contract, event_start_date, event_end_date, support_contact, location, attendees, notes = \
            changed_event['contract'], changed_event['event_start_date'], \
            changed_event['event_end_date'], changed_event['support_contact'], \
            changed_event['location'], changed_event['attendees'], changed_event['notes']
        if contract == '' or event_start_date == '' or event_end_date == '' \
                or support_contact == '' or location == '' or attendees == '' or notes == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or instance.contract.customer.creator == request.user \
                or instance.support_contact == request.user:
            serializer.save()
            return response.Response(status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        serializer = serializers.EventSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        new_event = serializer.validated_data
        contract, event_start_date, event_end_date, support_contact, location, attendees, notes = \
            new_event['contract'], new_event['event_start_date'], \
            new_event['event_end_date'], new_event['support_contact'], \
            new_event['location'], new_event['attendees'], new_event['notes']
        if contract == '' or event_start_date == '' or event_end_date == '' \
                or support_contact == '' or location == '' or attendees == '' or notes == '':
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.collaborator_type == 0 \
                or request.user.collaborator_type == 1 and contract.contract_state == 1 \
                and contract.customer.creator == request.user:
            models.Event.objects.create(contract=contract, event_start_date=event_start_date,
                                        event_end_date=event_end_date, support_contact=support_contact,
                                        location=location, attendees=attendees, notes=notes)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
