
from .views import parent_list_view, add_parent_view, edit_parent_view, delete_parent_view
from .views import parent_profile_view,update_parent_profile
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet

router = DefaultRouter()
router.register(r"parents", ParentViewSet, basename="parent")
urlpatterns = [
    path("api/", include(router.urls)),
    path('', parent_list_view, name='parent_list'),
    path('add/', add_parent_view, name='add_parent'),
    path('edit/<int:pk>/', edit_parent_view, name='edit_parent'),
    path('delete/<int:pk>/', delete_parent_view, name='delete_parent'),
    path('profile/', parent_profile_view, name='parent_profile'),
    path('profile/update/', update_parent_profile, name='update_parent_profile'),
]
