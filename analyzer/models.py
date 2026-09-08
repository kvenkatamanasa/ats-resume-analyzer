from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    file = models.FileField(
        upload_to="resumes/"
    )

    original_filename = models.CharField(
        max_length=255
    )

    extracted_text = models.TextField(
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.original_filename


class JobDescription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_descriptions"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title or "Job Description"


class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="analyses"
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="analyses",
        null=True,
        blank=True
    )

    ats_score = models.FloatField(
        default=0
    )

    keyword_score = models.FloatField(
        default=0
    )

    skills_score = models.FloatField(
        default=0
    )

    section_score = models.FloatField(
        default=0
    )

    experience_score = models.FloatField(
        default=0
    )

    formatting_score = models.FloatField(
        default=0
    )

    skills = models.JSONField(
        default=list,
        blank=True
    )

    sections = models.JSONField(
        default=dict,
        blank=True
    )

    matched_keywords = models.JSONField(
        default=list,
        blank=True
    )

    missing_keywords = models.JSONField(
        default=list,
        blank=True
    )

    recommendations = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Analysis - "
            f"{self.resume.original_filename} - "
            f"{self.ats_score}"
        )


class BuiltResume(models.Model):

    TEMPLATE_CHOICES = [
        ("classic", "Classic ATS"),
        ("modern", "Modern ATS"),
        ("student", "Student / Fresher ATS"),
        ("professional", "Professional ATS"),
        ("executive", "Executive ATS"),
        ("minimal", "Minimal ATS"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="built_resumes"
    )

    template = models.CharField(
        max_length=20,
        choices=TEMPLATE_CHOICES,
        default="classic"
    )

    full_name = models.CharField(
        max_length=150
    )

    professional_title = models.CharField(
        max_length=150,
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    summary = models.TextField(
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    experience = models.TextField(
        blank=True
    )

    projects = models.TextField(
        blank=True
    )

    education = models.TextField(
        blank=True
    )

    certifications = models.TextField(
        blank=True
    )

    achievements = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.full_name} - "
            f"{self.get_template_display()}"
        )