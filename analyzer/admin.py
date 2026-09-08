from django.contrib import admin
from .models import Resume, JobDescription, ResumeAnalysis


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "original_filename",
        "user",
        "uploaded_at",
    )

    search_fields = (
        "original_filename",
        "user__username",
    )

    list_filter = (
        "uploaded_at",
    )


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "user__username",
    )

    list_filter = (
        "created_at",
    )


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "resume",
        "job_description",
        "ats_score",
        "created_at",
    )

    search_fields = (
        "resume__original_filename",
        "job_description__title",
    )

    list_filter = (
        "created_at",
    )