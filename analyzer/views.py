from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    ResumeUploadForm,
    RegisterForm,
    ResumeBuilderForm,
)

from .models import (
    Resume,
    ResumeAnalysis,
    JobDescription,
    BuiltResume,
)

from ai.parser import extract_resume_text
from ai.analyzer import analyze_resume

from .documents import (
    create_pdf_response,
    create_docx_response,
)


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "analyzer/home.html",
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def dashboard(request):

    analyses = (
        ResumeAnalysis.objects
        .filter(
            resume__user=request.user
        )
        .select_related(
            "resume",
            "job_description",
        )
        .order_by("-created_at")
    )

    total_analyses = analyses.count()

    latest_analysis = analyses.first()

    average_score = 0

    if total_analyses:

        total_score = sum(
            float(analysis.ats_score)
            for analysis in analyses
        )

        average_score = round(
            total_score / total_analyses,
            2,
        )

    built_resumes = (
        BuiltResume.objects
        .filter(user=request.user)
        .order_by("-updated_at")
    )

    return render(
        request,
        "analyzer/dashboard.html",
        {
            "analyses": analyses,
            "total_analyses": total_analyses,
            "latest_analysis": latest_analysis,
            "average_score": average_score,
            "built_resumes": built_resumes,
        },
    )


@login_required
def upload_resume(request):

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            resume = form.save(commit=False)

            resume.user = request.user

            uploaded_file = request.FILES.get("file")

            if uploaded_file:

                resume.original_filename = uploaded_file.name

            job_description = None

            try:

                extracted_text = extract_resume_text(
                    resume.file.path
                )

                if not extracted_text.strip():

                    raise ValueError(
                        "No readable text was found in the "
                        "uploaded resume."
                    )

                resume.extracted_text = extracted_text

                resume.save()

                job_title = (
                    form.cleaned_data.get(
                        "job_title",
                        "",
                    ) or ""
                )

                job_description_text = (
                    form.cleaned_data.get(
                        "job_description",
                        "",
                    ) or ""
                )

                if job_description_text.strip():

                    job_description = JobDescription.objects.create(
                        user=request.user,
                        title=job_title.strip(),
                        description=job_description_text.strip(),
                    )

                result = analyze_resume(
                    extracted_text,
                    job_description_text,
                )

                ResumeAnalysis.objects.create(
                    resume=resume,
                    job_description=job_description,
                    ats_score=result.get("ats_score", 0),
                    keyword_score=result.get("keyword_score", 0),
                    skills_score=result.get("skills_score", 0),
                    section_score=result.get("section_score", 0),
                    experience_score=result.get(
                        "experience_score",
                        0,
                    ),
                    formatting_score=result.get(
                        "formatting_score",
                        0,
                    ),
                    skills=result.get(
                        "skills",
                        [],
                    ),
                    sections=result.get(
                        "sections",
                        {},
                    ),
                    matched_keywords=result.get(
                        "matched_keywords",
                        [],
                    ),
                    missing_keywords=result.get(
                        "missing_keywords",
                        [],
                    ),
                    recommendations=result.get(
                        "recommendations",
                        [],
                    ),
                )

            except Exception as error:

                resume.delete()

                if job_description:
                    job_description.delete()

                form.add_error(
                    "file",
                    f"Could not analyze the resume: {error}",
                )

            else:

                return redirect(
                    "resume_result",
                    resume_id=resume.id,
                )

    else:

        form = ResumeUploadForm()

    return render(
        request,
        "analyzer/upload.html",
        {
            "form": form,
        },
    )


@login_required
def resume_result(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user,
    )

    analysis = (
        ResumeAnalysis.objects
        .filter(resume=resume)
        .select_related("job_description")
        .order_by("-created_at")
        .first()
    )

    return render(
        request,
        "analyzer/result.html",
        {
            "resume": resume,
            "analysis": analysis,
        },
    )


@login_required
def latest_result(request):

    analysis = (
        ResumeAnalysis.objects
        .filter(
            resume__user=request.user
        )
        .select_related("resume")
        .order_by("-created_at")
        .first()
    )

    if not analysis:
        return redirect("upload_resume")

    return redirect(
        "resume_result",
        resume_id=analysis.resume.id,
    )


@login_required
def analysis_detail(request, analysis_id):

    analysis = get_object_or_404(
        ResumeAnalysis.objects.select_related(
            "resume",
            "job_description",
        ),
        id=analysis_id,
        resume__user=request.user,
    )

    return render(
        request,
        "analyzer/result.html",
        {
            "resume": analysis.resume,
            "analysis": analysis,
        },
    )


@login_required
def resume_templates(request):

    templates = [
        {
            "slug": "classic",
            "name": "Classic ATS",
            "description": (
                "Traditional single-column ATS-friendly format."
            ),
            "best_for": "Most professional roles",
        },
        {
            "slug": "modern",
            "name": "Modern ATS",
            "description": (
                "Clean modern layout with strong hierarchy."
            ),
            "best_for": "Technology and business roles",
        },
        {
            "slug": "student",
            "name": "Student / Fresher ATS",
            "description": (
                "Designed for students and fresh graduates."
            ),
            "best_for": "Students and freshers",
        },
        {
            "slug": "professional",
            "name": "Professional ATS",
            "description": (
                "Professional format focused on experience."
            ),
            "best_for": "Professional applications",
        },
        {
            "slug": "executive",
            "name": "Executive ATS",
            "description": (
                "Strong format for leadership applications."
            ),
            "best_for": "Leadership roles",
        },
        {
            "slug": "minimal",
            "name": "Minimal ATS",
            "description": (
                "Simple and highly readable ATS format."
            ),
            "best_for": "General applications",
        },
    ]

    return render(
        request,
        "analyzer/templates.html",
        {
            "templates": templates,
        },
    )


@login_required
def builder_home(request):
    return redirect("resume_templates")


@login_required
def resume_builder(request, template):

    valid_templates = {
        "classic": "Classic ATS",
        "modern": "Modern ATS",
        "student": "Student / Fresher ATS",
        "professional": "Professional ATS",
        "executive": "Executive ATS",
        "minimal": "Minimal ATS",
    }

    if template not in valid_templates:
        return redirect("resume_templates")

    template_name = valid_templates[template]

    if request.method == "POST":

        form = ResumeBuilderForm(request.POST)

        if form.is_valid():

            built_resume = form.save(
                commit=False
            )

            built_resume.user = request.user

            built_resume.template = template

            built_resume.save()

            return redirect(
                "resume_builder_preview",
                resume_id=built_resume.id,
            )

    else:

        form = ResumeBuilderForm()

    return render(
        request,
        "analyzer/builder.html",
        {
            "form": form,
            "template": template,
            "template_name": template_name,
        },
    )


@login_required
def resume_builder_preview(request, resume_id):

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return render(
        request,
        "analyzer/builder_preview.html",
        {
            "resume": resume,
        },
    )


@login_required
def latest_built_resume(request):

    resume = (
        BuiltResume.objects
        .filter(user=request.user)
        .order_by("-created_at")
        .first()
    )

    if not resume:
        return redirect("resume_templates")

    return redirect(
        "resume_builder_preview",
        resume_id=resume.id,
    )


@login_required
def download_resume_pdf(request, resume_id):

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return create_pdf_response(resume)


@login_required
def download_resume_docx(request, resume_id):

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return create_docx_response(resume)