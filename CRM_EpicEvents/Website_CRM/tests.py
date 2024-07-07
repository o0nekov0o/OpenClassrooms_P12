import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from django.test import TestCase
from rest_framework import status
from Website_CRM import models, serializers


class TestCaseCrmUser(TestCase):

    def setUp(self):
        self.new_user_1_data = {
            'username': 'o0nekov0o',
            'password': 'test_123',
            'first_name': 'admin',
            'last_name': 'webmaster',
            'email': 'admin@gmail.com',
            'collaborator_type': 0,
        }
        self.new_user_1_test = models.CRM_User.objects.create_user(**self.new_user_1_data)

    def test_crm_user_model(self):
        self.new_user_2_data = {
            'creator': self.new_user_1_test,
            'username': 'new_user',
            'password': 'new_password',
            'first_name': 'donald',
            'last_name': 'mitchell',
            'email': 'mitch@gmail.com',
            'collaborator_type': 0,
        }
        self.new_user_2_test = models.CRM_User.objects.create_user(**self.new_user_2_data)
        self.assertEqual(self.new_user_1_test, self.new_user_2_test.creator)
        self.assertNotEqual(self.new_user_1_test, self.new_user_2_test)

    def test_crm_user_serializer(self):
        self.new_user_1_data['username'] = 'o0nekov0o_1'
        self.crm_user_serializer = serializers.CrmUserSerializer(data=self.new_user_1_data)
        self.assertTrue(self.crm_user_serializer.is_valid())

    def test_crm_user_view(self):
        self.client.login(username=self.new_user_1_data['username'],
                          password=self.new_user_1_data['password'])
        self.new_user_1_data['username'] = 'o0nekov0o_2'
        self.new_user_1_data['email'] = 'admin@gmail.com'
        response = self.client.post('/crm_users/', self.new_user_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.new_user_1_data['username'] = 'o0nekov0o'
        self.new_user_1_data['email'] = 'admin_2@gmail.com'
        response = self.client.post('/crm_users/', self.new_user_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.new_user_1_data['username'] = 'o0nekov0o_2'
        self.new_user_1_data['email'] = 'admin_2@gmail.com'
        response = self.client.post('/crm_users/', self.new_user_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseCustomer(TestCase):

    def setUp(self):
        self.new_user_1_data = {
            'username': 'o0nekov0o',
            'password': 'test_123',
            'first_name': 'admin',
            'last_name': 'webmaster',
            'email': 'admin@gmail.com',
            'collaborator_type': 1,
        }
        self.new_user_1_test = models.CRM_User.objects.create_user(**self.new_user_1_data)
        self.new_customer_1_data = {
            'information': 'New Customer Unlocked',
            'full_name': 'John Doe the One',
            'email': 'johndoe_theone@gmail.com',
            'phone_number': '+33701020304',
            'enterprise_name': 'Anonymous Enterprise',
            'commercial_contact': self.new_user_1_test
        }
        self.new_customer_1_test = models.Customer.objects.create(**self.new_customer_1_data)

    def test_customer_model(self):
        self.new_customer_2_data = {
            'information': 'Another Customer Unlocked',
            'full_name': 'John Doe the Second',
            'email': 'johndoe_numbertwo@gmail.com',
            'phone_number': '+33702030405',
            'enterprise_name': 'Anonymous Enterprise',
            'commercial_contact': self.new_user_1_test
        }
        self.new_customer_2_test = models.Customer.objects.create(**self.new_customer_2_data)
        self.assertEqual(self.new_customer_1_test.commercial_contact,
                         self.new_customer_2_test.commercial_contact)
        self.assertNotEqual(self.new_customer_1_test, self.new_customer_2_test)

    def test_customer_serializer(self):
        self.new_customer_1_data['email'] = 'johndoe_number3@gmail.com'
        self.new_customer_1_data['phone_number'] = '+33733457295'
        self.new_customer_1_data['commercial_contact'] = \
            models.CRM_User.objects.get(username='o0nekov0o').id
        self.customer_serializer = serializers.CustomerSerializer(data=self.new_customer_1_data)
        self.assertTrue(self.customer_serializer.is_valid())

    def test_customer_view(self):
        self.client.login(username=self.new_user_1_data['username'],
                          password=self.new_user_1_data['password'])
        self.new_customer_1_data['email'] = 'johndoe_number4@gmail.com'
        self.new_customer_1_data['phone_number'] = '+33701020304'
        self.new_customer_1_data['commercial_contact'] = \
            models.CRM_User.objects.get(username='o0nekov0o').id
        response = self.client.post('/customers/', self.new_customer_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.new_customer_1_data['email'] = 'johndoe_theone@gmail.com'
        self.new_customer_1_data['phone_number'] = '+33733457296'
        self.new_customer_1_data['commercial_contact'] = \
            models.CRM_User.objects.get(username='o0nekov0o').id
        response = self.client.post('/customers/', self.new_customer_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.new_customer_1_data['email'] = 'johndoe_number4@gmail.com'
        self.new_customer_1_data['phone_number'] = '+33733457296'
        self.new_customer_1_data['commercial_contact'] = \
            models.CRM_User.objects.get(username='o0nekov0o').id
        response = self.client.post('/customers/', self.new_customer_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseContract(TestCase):

    def setUp(self):
        self.new_user_1_data = {
            'username': 'o0nekov0o',
            'password': 'test_123',
            'first_name': 'admin',
            'last_name': 'webmaster',
            'email': 'admin@gmail.com',
            'collaborator_type': 0,
        }
        self.new_user_1_test = models.CRM_User.objects.create_user(**self.new_user_1_data)
        self.new_customer_1_data = {
            'information': 'New Customer Unlocked',
            'full_name': 'John Doe the One',
            'email': 'johndoe_theone@gmail.com',
            'phone_number': '+33701020304',
            'enterprise_name': 'Anonymous Enterprise',
            'commercial_contact': self.new_user_1_test
        }
        self.new_customer_1_test = models.Customer.objects.create(**self.new_customer_1_data)
        self.new_contract_1_data = {
            'customer': self.new_customer_1_test,
            'total_amount': 500,
            'unpaid_amount': 250,
            'contract_state': 1,
        }
        self.new_contract_1_test = models.Contract.objects.create(**self.new_contract_1_data)

    def test_contract_model(self):
        self.new_contract_2_data = {
            'customer': self.new_customer_1_test,
            'total_amount': 500,
            'unpaid_amount': 250,
            'contract_state': 1,
        }
        self.new_contract_2_test = models.Contract.objects.create(**self.new_contract_2_data)
        self.assertEqual(self.new_contract_1_test.commercial_contact,
                         self.new_contract_2_test.commercial_contact)
        self.assertNotEqual(self.new_contract_1_test, self.new_contract_2_test)

    def test_contract_serializer(self):
        self.new_contract_1_data['customer'] = models.Customer.objects.last().id
        self.contract_serializer = serializers.ContractSerializer(data=self.new_contract_1_data)
        self.assertTrue(self.contract_serializer.is_valid())

    def test_contract_view(self):
        self.client.login(username=self.new_user_1_data['username'],
                          password=self.new_user_1_data['password'])
        self.new_contract_1_data['customer'] = models.Customer.objects.last().id
        response = self.client.post('/contracts/', self.new_contract_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCaseEvent(TestCase):

    def setUp(self):
        self.new_user_1_data = {
            'username': 'o0nekov0o',
            'password': 'test_123',
            'first_name': 'admin',
            'last_name': 'webmaster',
            'email': 'admin@gmail.com',
            'collaborator_type': 0,
        }
        self.new_user_1_test = models.CRM_User.objects.create_user(**self.new_user_1_data)
        self.new_user_2_data = {
            'creator': self.new_user_1_test,
            'username': 'new_user',
            'password': 'new_password',
            'first_name': 'donald',
            'last_name': 'mitchell',
            'email': 'mitch@gmail.com',
            'collaborator_type': 2,
        }
        self.new_user_2_test = models.CRM_User.objects.create_user(**self.new_user_2_data)
        self.new_customer_1_data = {
            'information': 'New Customer Unlocked',
            'full_name': 'John Doe the One',
            'email': 'johndoe_theone@gmail.com',
            'phone_number': '+33701020304',
            'enterprise_name': 'Anonymous Enterprise',
            'commercial_contact': self.new_user_1_test
        }
        self.new_customer_1_test = models.Customer.objects.create(**self.new_customer_1_data)
        self.new_contract_1_data = {
            'customer': self.new_customer_1_test,
            'total_amount': 500,
            'unpaid_amount': 250,
            'contract_state': 1,
        }
        self.new_contract_1_test = models.Contract.objects.create(**self.new_contract_1_data)
        self.new_event_1_data = {
            'contract': self.new_contract_1_test,
            'event_start_date': '2025-04-23T18:25:43.511Z',
            'event_end_date': '2025-04-24T18:25:43.511Z',
            'support_contact': self.new_user_2_test,
            'location': 'Paris',
            'attendees': 500,
            'notes': '500 attendees',
        }
        self.new_event_1_test = models.Event.objects.create(**self.new_event_1_data)

    def test_event_model(self):
        self.new_event_2_data = {
            'contract': self.new_contract_1_test,
            'event_start_date': '2025-04-23T18:25:43.511Z',
            'event_end_date': '2025-04-24T18:25:43.511Z',
            'support_contact': self.new_user_2_test,
            'location': 'Paris',
            'attendees': 500,
            'notes': '500 attendees',
        }
        self.new_event_2_test = models.Event.objects.create(**self.new_event_2_data)
        self.assertEqual(self.new_event_1_test.support_contact,
                         self.new_event_2_test.support_contact)
        self.assertNotEqual(self.new_event_1_test, self.new_event_2_test)

    def test_event_serializer(self):
        self.new_event_1_data['contract'] = models.Contract.objects.last().id
        self.new_event_1_data['support_contact'] = models.CRM_User.objects.last().id
        self.event_serializer = serializers.EventSerializer(data=self.new_event_1_data)
        self.assertTrue(self.event_serializer.is_valid())

    def test_contract_view(self):
        self.client.login(username=self.new_user_1_data['username'],
                          password=self.new_user_1_data['password'])
        self.new_event_1_data['contract'] = models.Contract.objects.last().id
        self.new_event_1_data['support_contact'] = models.CRM_User.objects.last().id
        response = self.client.post('/events/', self.new_event_1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
