from rest_framework_extensions.routers import ExtendedSimpleRouter
from . import views


router = ExtendedSimpleRouter()
(
    router.register(r'members', views.MemberViewSet, base_name='members')
          .register(r'promo',
                    views.PromoUrlViewSet,
                    base_name='member-promo',
                    parents_query_lookups=['member'])
)
(
    router.register(r'members', views.MemberViewSet, base_name='members')
          .register(r'certification',
                    views.CertificationViewSet,
                    base_name='member-certification',
                    parents_query_lookups=['member'])
)

router.register(r'certification', views.CertificationViewSet, base_name='certification')
