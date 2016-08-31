from rest_framework_extensions.routers import ExtendedSimpleRouter
from . import views


router = ExtendedSimpleRouter()
(
    router.register(r'projects', views.ProjectViewSet, base_name='projects')
          .register(r'media',
                    views.MediaViewSet,
                    base_name='project-variations',
                    parents_query_lookups=['project'])

)
(
    router.register(r'categories', views.CategoryViewSet, base_name='categories')
          .register(r'projects',
                    views.ProjectViewSet,
                    base_name='category-projects',
                    parents_query_lookups=['category__slug'])
)
router.register(r'skills', views.SkillViewSet, base_name='skills')
router.register(r'technologies', views.SkillViewSet, base_name='technologies')