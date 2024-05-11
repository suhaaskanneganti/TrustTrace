from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.urls import reverse
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, SubmissionForm, EditSubmissionForm
from .models import Submission, File
from django.conf import settings
# Create your views here.

# https://stackoverflow.com/questions/604266/django-set-default-form-values
# https://stackoverflow.com/questions/33714485/prepopulating-django-form-request-files-and-instance
def reviewreports_view(request):
    if request.method == 'POST':
        forms = [EditSubmissionForm(request.POST, request.FILES, instance=submission, prefix=submission.id) for submission in Submission.objects.all().order_by('id')]
        for form in forms:
            initial_data = form.initial
            if form.is_valid() and form.cleaned_data != initial_data:
                form.save()
        return redirect('main:reviewreports_view')
    else:
        selected_tag = request.GET.get('tag')
        selected_status = request.GET.get('status')
        if selected_tag and selected_status:
            submissions = Submission.objects.filter(tag=selected_tag, status=selected_status).order_by('id')
        elif selected_tag and not selected_status:
            submissions = Submission.objects.filter(tag=selected_tag).order_by('id')
        elif not selected_tag and selected_status:
            submissions = Submission.objects.filter(status=selected_status).order_by('id')
        else:
            submissions = Submission.objects.all().order_by('id')
        forms = [EditSubmissionForm(instance=submission, prefix=submission.id) for submission in submissions]
    return render(request, "main/reviewreports.html", {'forms': forms, 'TAG_OPTIONS': TAG_OPTIONS, 'STATUS_OPTIONS': STATUS_OPTIONS})


def profile_view(request):
    submissions = Submission.objects.filter(user=request.user).order_by('id')
    return render(request, "main/profile.html", {'submissions': submissions})


def index(request):
    return render(request, "main/home.html",)


def success_view(request):
    image_link = request.GET.get('image_link')
    return render(request, "main/success.html", {'image_link': image_link})


def submission_view(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():

            text = form.cleaned_data['text']
            subject = form.cleaned_data['subject']
            if request.user.is_authenticated:
                submission = Submission.objects.create(user=request.user, text=text, subject=subject)
            else:
                submission = Submission.objects.create(user=None, text=text, subject=subject)
            submission.save()

            files = form.cleaned_data['file']
            for file in files:
                file_obj = File.objects.create(submission=submission, file=file)
                file_obj.save()

            success_url = reverse("main:success")

            return redirect(success_url)
    else:
        form = SubmissionForm()
    return render(request, 'main/submission.html', {'form': form})


def delete_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == 'POST':
        submission.delete()
        return render(request, 'main/deletesubmission.html')
    else:
        submissions = Submission.objects.filter(user=request.user)
        return render(request, 'main/profile.html', {'submissions': submissions})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('main:home'))
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('main:home'))


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})


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
    ('Other', 'Other'),
]

STATUS_OPTIONS = [('New', 'New'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ]

