from django.urls import path
from . import views

app_name = "airports"
urlpatterns = [
    path("", views.airport_distance_views, name="airport_list"),
    path("calculate/", views.calculate_distance, name="calculate_distance"),
]
