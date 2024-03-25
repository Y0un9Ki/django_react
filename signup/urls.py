from django.urls import path, include
from .views import MyTokenObtainPairView, SignUpView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('signin/', MyTokenObtainPairView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
