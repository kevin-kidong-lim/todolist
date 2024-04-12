from django.urls import path, include
from rest_framework.routers import DefaultRouter
from member import views
from member.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'member'
router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path('',include(router.urls)),
    # path('register2/', views.register, name='register'),
    path('login', views.login, name='login'),

    path('detail/<str:pk>', views.DtailView.as_view()),

    path('register/', views.RegisterView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token2/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair2'),
    
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),

   
]