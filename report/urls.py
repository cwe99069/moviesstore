from django.urls import path
from . import views
urlpatterns = [
    path('<int:review_id>/report/index.html', views.repreview, name='report.review')
]