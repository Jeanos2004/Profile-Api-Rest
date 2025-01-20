from django.urls import path, include
from api.views import HelloApiView


urlpatterns = [
    path('', HelloApiView.as_view()),
]