from django import forms

class AssessmentForm(forms.Form):
    consent = forms.IntegerField(min_value=0, max_value=100)
    security = forms.IntegerField(min_value=0, max_value=100)
    breach = forms.IntegerField(min_value=0, max_value=100)
    children = forms.IntegerField(min_value=0, max_value=100)
    sdf = forms.IntegerField(min_value=0, max_value=100)

    breach_workflow = forms.BooleanField(required=False)
    children_data = forms.BooleanField(required=False)
    parental_consent = forms.BooleanField(required=False)
    is_sdf = forms.BooleanField(required=False)
    dpia_done = forms.BooleanField(required=False)