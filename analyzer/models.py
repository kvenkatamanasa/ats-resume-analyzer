from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes'
    )

    # Keep this field for compatibility with existing database migrations.
    # We will NOT depend on it for Vercel storage.
    file = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    original_filename = models.CharField(max_length=255)

    extracted_text = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename


class JobDescription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_descriptions'
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
        return self.title or 'Job Description'


class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='analyses'
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='analyses'
    )

    ats_score = models.FloatField(default=0)

    keyword_score = models.FloatField(default=0)

    skills_score = models.FloatField(default=0)

    section_score = models.FloatField(default=0)

    experience_score = models.FloatField(default=0)

    formatting_score = models.FloatField(default=0)

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

    jd_match_score = models.FloatField(default=0)

    matched_skills = models.JSONField(
        default=list,
        blank=True
    )

    missing_skills = models.JSONField(
        default=list,
        blank=True
    )

    priority_keywords = models.JSONField(
        default=list,
        blank=True
    )

    improvement_suggestions = models.JSONField(
        default=list,
        blank=True
    )

    before_score = models.FloatField(default=0)

    after_score = models.FloatField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Analysis - {self.resume.original_filename} - {self.ats_score}'


class BuiltResume(models.Model):

    TEMPLATE_CHOICES = [
        ('classic', 'Classic ATS'),
        ('modern', 'Modern ATS'),
        ('student', 'Student / Fresher ATS'),
        ('professional', 'Professional ATS'),
        ('executive', 'Executive ATS'),
        ('minimal', 'Minimal ATS'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='built_resumes'
    )

    template = models.CharField(
        max_length=20,
        choices=TEMPLATE_CHOICES,
        default='classic'
    )

    version_name = models.CharField(
        max_length=150,
        default='Resume'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='versions'
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
        return f'{self.full_name} - {self.version_name}'
