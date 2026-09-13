class ResumeUploadForm(forms.Form):

    file = forms.FileField(
        label="Resume"
    )

    job_title = forms.CharField(
        required=False,
        max_length=255
    )

    job_description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 10
            }
        )
    )

    def clean_file(self):

        f = self.cleaned_data.get('file')

        if not f:
            raise forms.ValidationError(
                "Please select a resume."
            )

        filename = f.name.lower()

        if not filename.endswith(
            ('.pdf', '.docx')
        ):
            raise forms.ValidationError(
                "Only PDF and DOCX files are supported."
            )

        # Keep below Vercel's request payload limit.
        if f.size > 4 * 1024 * 1024:
            raise forms.ValidationError(
                "Maximum resume size is 4 MB."
            )

        return f
