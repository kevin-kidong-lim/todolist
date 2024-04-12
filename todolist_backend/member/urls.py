from django.urls import path, include
from rest_framework.routers import DefaultRouter
from member import views
app_name = 'member'
router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path('',include(router.urls)),
    path('detail/<str:pk>', views.DtailView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair2'),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
]