from django import forms


class SubmitDownloadForm(forms.Form):
    url = forms.URLField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "eg: https://www.youtube.com/watch?v=ROOeGPrC1Do",
            }
        )
    )
