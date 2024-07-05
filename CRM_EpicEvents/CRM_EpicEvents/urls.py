"""
URL configuration for CRM_EpicEvents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import include, path
from Website_CRM import views, views_token
from rest_framework.authtoken import views as login_token

router = routers.DefaultRouter()
router.register(r'permission', views.PermissionViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'crm_users', views.CrmUserViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'events', views.EventsViewSet)


def trigger_error(request):
    division_by_zero = 1 / 0


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
    path('api-token-auth/', login_token.obtain_auth_token),
    path('token_crm_users/<int:pk>/', views_token.CrmUserView.as_view()),
    path('token_crm_users/', views_token.CrmUserView.as_view()),
    path('token_customers/<int:pk>/', views_token.CustomerView.as_view()),
    path('token_customers/', views_token.CustomerView.as_view()),
    path('token_contracts/<int:pk>/', views_token.ContractView.as_view()),
    path('token_contracts/', views_token.ContractView.as_view()),
    path('token_events/<int:pk>/', views_token.EventView.as_view()),
    path('token_events/', views_token.EventView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
