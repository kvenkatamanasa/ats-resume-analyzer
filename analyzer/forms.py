from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Resume, BuiltResume


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(UserCreationForm):
    """
    User registration form.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email",
                "autocomplete": "email",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Choose a username",
                    "autocomplete": "username",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email


# =========================================================
# RESUME UPLOAD FORM
# =========================================================

class ResumeUploadForm(forms.ModelForm):
    """
    Upload a PDF or DOCX resume.

    Job Description is optional.
    """

    job_title = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: Data Analyst",
            }
        ),
    )

    job_description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": (
                    "Paste the target job description here "
                    "(optional)..."
                ),
                "rows": 8,
            }
        ),
    )

    class Meta:
        model = Resume

        fields = [
            "file",
        ]

        widgets = {
            "file": forms.ClearableFileInput(
                attrs={
                    "accept": ".pdf,.docx",
                }
            ),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if not uploaded_file:
            raise forms.ValidationError(
                "Please upload a resume."
            )

        filename = uploaded_file.name.lower()

        allowed_extensions = (
            ".pdf",
            ".docx",
        )

        if not filename.endswith(
            allowed_extensions
        ):
            raise forms.ValidationError(
                "Only PDF and DOCX files are supported."
            )

        # 5 MB maximum
        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "Resume file size must be 5 MB or less."
            )

        return uploaded_file


# =========================================================
# RESUME BUILDER FORM
# =========================================================

class ResumeBuilderForm(forms.ModelForm):
    """
    Form used to create an ATS-friendly resume.
    """

    class Meta:
        model = BuiltResume

        fields = [
            "full_name",
            "professional_title",
            "email",
            "phone",
            "location",
            "linkedin",
            "github",
            "summary",
            "skills",
            "experience",
            "projects",
            "education",
            "certifications",
            "achievements",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Your Full Name",
                }
            ),

            "professional_title": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Example: Data Analyst"
                    ),
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "your@email.com",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+91 XXXXX XXXXX",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": (
                        "City, State, Country"
                    ),
                }
            ),

            "linkedin": forms.URLInput(
                attrs={
                    "placeholder": (
                        "https://linkedin.com/in/yourname"
                    ),
                }
            ),

            "github": forms.URLInput(
                attrs={
                    "placeholder": (
                        "https://github.com/yourname"
                    ),
                }
            ),

            "summary": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Write a concise professional summary..."
                    ),
                    "rows": 6,
                }
            ),

            "skills": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Python, SQL, Excel, Power BI..."
                    ),
                    "rows": 5,
                }
            ),

            "experience": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Company - Role\n"
                        "Dates\n"
                        "• Achievement or responsibility\n"
                        "• Achievement or responsibility"
                    ),
                    "rows": 8,
                }
            ),

            "projects": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Project Name | Technologies\n"
                        "• Description and result"
                    ),
                    "rows": 8,
                }
            ),

            "education": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Degree - Institution - Year\n"
                        "CGPA: X.XX / 10"
                    ),
                    "rows": 5,
                }
            ),

            "certifications": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Certification - Provider"
                    ),
                    "rows": 5,
                }
            ),

            "achievements": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Awards, achievements, "
                        "competitions, leadership..."
                    ),
                    "rows": 5,
                }
            ),
        }

    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()

        if not value:
            raise forms.ValidationError(
                "Full name is required."
            )

        return value

    def clean_email(self):
        value = self.cleaned_data["email"].strip()

        if not value:
            raise forms.ValidationError(
                "Email is required."
            )

        return value