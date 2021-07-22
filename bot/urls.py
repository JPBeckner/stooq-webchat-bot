from rest_framework.routers import DefaultRouter

from .views import Command


router = DefaultRouter()
router.register(
    prefix='', viewset=Command, basename='command'
)
urlpatterns = router.urls
