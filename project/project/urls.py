from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from users import viewsets as users


router = DefaultRouter()
router.register("users", users.UserViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/token/", users.ObtainTokenView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
