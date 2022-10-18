from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'links', views.LinkViewSet, basename='link')

urlpatterns = [
    path('link/', views.NewView.as_view()),
    path('locations/<str:url_code>/', views.LocationsView.as_view()),
    path('locations/', views.AllLocationsView.as_view()),
    path('info/', views.NumberOfViewsAndLinksView.as_view()),
] + router.urls