from django.urls import path
from . import views

urlpatterns = [
    path("metrics/top-products/", views.top_products),
    path("metrics/total-by-user/", views.total_by_user_type),
    path("metrics/last-5min/", views.money_last_5_minutes),

    path("audit/resources/", views.list_datalake_files),
    path("audit/version/", views.get_file_version),
    path("audit/access-log/", views.access_log),

    path("fulltext_search/<str:text>/", views.fulltext_search),

]
