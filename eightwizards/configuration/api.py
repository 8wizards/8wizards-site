from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'config_params', views.ConfigParamViewSet, base_name='config_params')

