from django.contrib import admin
from django.urls import path
from .views import PartyAPIView
from .views import FileAPIView
# from .views import PartyRegisterViewSets

urlpatterns = [
    path('party/', PartyAPIView.as_view()),
    path('upload/', FileAPIView.as_view()),
    #path('partyRegister/', PartyRegisterViewSets.as_view({'get': 'list'}))
]