from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookAPIView, BorrowRequestAPIView

urlpatterns = [
    path('books/', BookAPIView.as_view(), name='books'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('borrow_requests/', BorrowRequestAPIView.as_view(), name='borrow_requests'),
]