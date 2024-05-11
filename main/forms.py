from django import forms
from .models import CustomUser, Submission, File
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(required=True,
                              max_length=100,
                              label="Password",
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
    username = forms.CharField(required=True,
                              max_length=100,
                              label="Username",
                              widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    email = forms.CharField(required=True,
                              max_length=100,
                              label="Email",
                              widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'example@example.com'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    field_order = ['username', 'password','email']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))


# https://stackoverflow.com/questions/324477/in-a-django-form-how-do-i-make-a-field-readonly-or-disabled-so-that-it-cannot
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class':'form-control'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class SubmissionForm(forms.ModelForm):
    TAG_OPTIONS = [
        ('Cheating - Exam', 'Cheating - Exam'),
        ('Cheating - Coursework', 'Cheating - Coursework'),
        ('Lying', 'Lying'),
        ('Stealing - Physical Property', 'Stealing - Physical Property'),
        ('Stealing - Coursework', 'Stealing - Physical Property'),
        ('Plagiarism', 'Plagiarism'),
        ('Multiple Submission', 'Multiple Submission'),
        ('False Citation', 'False Citation'),
        ('False Data', 'False Data'),
        ('Discrimination', 'Discrimination'),
        ('Other', 'Other')
    ]
    subject = forms.CharField(required=True,
                              max_length=100,
                              label="Subject",
                              widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Subject'}))

    text = forms.CharField(required=True,
                           max_length=100,
                           label="Text",
                           widget=forms.Textarea(attrs={'class':'form-control','rows': '5', 'cols': '5','placeholder': 'Comment...'}))

    file = MultipleFileField(required=False,
                             label="Files")

    tag = forms.ChoiceField(required=True,
                            label="Tag",
                            choices=TAG_OPTIONS,
                            widget=forms.Select())

    class Meta:
        model = Submission
        exclude = ['status','admin_response','user']

    class Meta:
        model = File
        fields = ['file']

    BLACKLISTED_EXTENSIONS = ['.exe', '.bat', 'cmd']
    field_order = ['subject','text','tag','file']


# https://stackoverflow.com/questions/324477/in-a-django-form-how-do-i-make-a-field-readonly-or-disabled-so-that-it-cannot
class EditSubmissionForm(forms.ModelForm):
    admin_response = forms.CharField(max_length=500, required=True)

    class Meta:
        model = Submission
        fields = ['subject', 'text', 'tag', 'status', 'admin_response']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False
        self.fields['text'].required = False
        self.fields['status'].required = False
        self.fields['admin_response'].required = False
        self.fields['tag'].required = False
        for name, field in self.fields.items():
            if name not in ['status', 'admin_response', 'tag']:
                field.widget.attrs['readonly'] = True
