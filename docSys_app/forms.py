from django import forms
from docSys_app.models import Houses, Voices, Document


class DateInput(forms.DateInput):
    input_type = "date"

class AddMemberForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_start=forms.DateField(label="Session Start",widget=DateInput(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)

    # Add house field in __init__ to ensure fresh data each time
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)

        # Houses dropdown
        houses = Houses.objects.all()
        house_list = [(house.id, house.house_name) for house in houses]
        self.fields['house'] = forms.ChoiceField(
            label="House", 
            choices=house_list, 
            widget=forms.Select(attrs={"class":"form-control"})
        )

        # Voices dropdown
        voices = Voices.objects.all()
        voice_list = [(voice.id, voice.voice_name) for voice in voices]
        self.fields['voice'] = forms.ChoiceField(
            label="Voice", 
            choices=voice_list, 
            widget=forms.Select(attrs={"class":"form-control"})
        )

class EditMemberForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_start=forms.DateField(label="Session Start",widget=DateInput(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)

    # Similarly for EditMemberForm
    def __init__(self, *args, **kwargs):
        super(EditMemberForm, self).__init__(*args, **kwargs)
        houses = Houses.objects.all()
        self.fields['house'] = forms.ChoiceField(
            label="House",
            choices=[(house.id, house.house_name) for house in houses],
            widget=forms.Select(attrs={"class":"form-control"})
        )
        voices = Voices.objects.all()
        self.fields['voice'] = forms.ChoiceField(
            label="Voice",
            choices=[(voice.id, voice.voice_name) for voice in voices],
            widget=forms.Select(attrs={"class":"form-control"})
        )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "file"]

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and not file.name.endswith(".pdf"):
            raise forms.ValidationError("Only PDF files are allowed.")
        return file
    