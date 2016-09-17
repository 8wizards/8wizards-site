from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'email', views.EmailAPIViewSet, base_name='email')

