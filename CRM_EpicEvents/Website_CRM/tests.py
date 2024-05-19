import phonenumbers
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
