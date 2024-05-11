from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# https://stackoverflow.com/questions/57446355/custom-user-model-error-attributeerror-customuser-object-has-no-attribute-i
# https://stackoverflow.com/questions/53172431/customising-django-user-model-is-failing
# ChatGPT - how to fix has_module_perms error in Django
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class CustomUser(AbstractBaseUser):
    objects = CustomUserManager()

    username = models.CharField("Username", max_length=100, unique=True)
    password = models.CharField("Password", max_length=100)
    email = models.EmailField("Email")
    site_admin = models.BooleanField("Admin User", default=False)
    is_staff = models.BooleanField("Staff Status", default=False)
    is_superuser = models.BooleanField("Superuser Status", default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email', 'site_admin']

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.username


class Submission(models.Model):
    STATUS_OPTIONS = [('New', 'New'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ]
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
    subject = models.CharField(max_length=500, default="N/A")
    text = models.CharField(max_length=500, default="N/A")
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='New')
    tag = models.CharField(max_length=40, choices=TAG_OPTIONS, default='Other')
    admin_response = models.CharField(max_length=500, default="N/A")
    user = models.ForeignKey(CustomUser, default=None, blank=True, null=True, on_delete=models.CASCADE)


class File(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
