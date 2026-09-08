from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home",
    ),


    # =====================================================
    # USER REGISTRATION
    # =====================================================

    path(
        "accounts/register/",
        views.register,
        name="register",
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),


    # =====================================================
    # ATS RESUME TEMPLATES
    # =====================================================

    path(
        "templates/",
        views.resume_templates,
        name="resume_templates",
    ),


    # =====================================================
    # RESUME BUILDER
    # =====================================================

    path(
        "builder/<str:template>/",
        views.resume_builder,
        name="resume_builder",
    ),


    # =====================================================
    # RESUME BUILDER PREVIEW
    # =====================================================

    path(
        "builder/preview/<int:resume_id>/",
        views.resume_builder_preview,
        name="resume_builder_preview",
    ),


    # =====================================================
    # DOWNLOAD PDF
    # =====================================================

    path(
        "builder/download/pdf/<int:resume_id>/",
        views.download_resume_pdf,
        name="download_resume_pdf",
    ),


    # =====================================================
    # DOWNLOAD DOCX
    # =====================================================

    path(
        "builder/download/docx/<int:resume_id>/",
        views.download_resume_docx,
        name="download_resume_docx",
    ),


    # =====================================================
    # RESUME UPLOAD / ATS ANALYSIS
    # =====================================================

    path(
        "upload/",
        views.upload_resume,
        name="upload_resume",
    ),


    # =====================================================
    # LATEST RESULT FOR A RESUME
    # =====================================================

    path(
        "result/<int:resume_id>/",
        views.resume_result,
        name="resume_result",
    ),


    # =====================================================
    # SPECIFIC HISTORICAL ANALYSIS
    # =====================================================

    path(
        "analysis/<int:analysis_id>/",
        views.analysis_detail,
        name="analysis_detail",
    ),
]