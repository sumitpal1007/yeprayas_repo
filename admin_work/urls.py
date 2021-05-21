from django.contrib import admin
from django.urls import path
from .views import AdminAPIView
from .views import DocumentAPIView
# from .views import PartyRegisterViewSets

urlpatterns = [
    path('admin/', AdminAPIView.as_view()),
    path('document/', DocumentAPIView.as_view()),
    # path('upload/', FileAPIView.as_view()),
    #path('partyRegister/', PartyRegisterViewSets.as_view({'get': 'list'}))
]