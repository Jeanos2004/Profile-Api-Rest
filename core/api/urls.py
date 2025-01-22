from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import HelloApiView, HelloViewSet, UserProfileViewSet, UserLoginApiView, UserProfileFeedViewSet

router = DefaultRouter()
router.register('Hello-Viewset', HelloViewSet, basename='Hello-Viewset')
router.register('UserProfile', UserProfileViewSet)
router.register('feed', UserProfileFeedViewSet)
urlpatterns = [
    path('apiview', HelloApiView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('', include(router.urls)),
    
]