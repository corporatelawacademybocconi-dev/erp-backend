from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, TagViewSet, ContactViewSet, InteractionViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = router.urls