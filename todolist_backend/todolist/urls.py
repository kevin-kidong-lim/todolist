from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'todolist'
router = DefaultRouter(trailing_slash=False)
router.register('',views.CreateView)

urlpatterns = [ 
    path('list/<str:user_id>', views.DetailListView.as_view(),name='mymodel-list-create'),
    path('detail/<int:pk>', views.DetailView.as_view(),name='mymodel-detail'),
    # path('create', views.CreateView),
    path('',include(router.urls)),

]