from django.urls import path
from .views import create_assessment, generate_pdf

urlpatterns = [
    path("new/", create_assessment, name="create_assessment"),
    path("report/<int:assessment_id>/", generate_pdf, name="generate_pdf"),
    path("executive/", executive_summary, name="executive_summary"),
]
