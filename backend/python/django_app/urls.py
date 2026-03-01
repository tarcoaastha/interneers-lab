from django.urls import path
from .views import greeting_view
urlpatterns = [
    path('hello/', greeting_view),
]