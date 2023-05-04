from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('user must have an email address.')
        if not username:
            raise ValueError('user must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField('email', unique=True)
    portfolio = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class TodoListModel(models.Model):

    STATUS_CHOICE = [
        ('C', 'Created'), ('P', 'In progress'), ('D', 'Done')
    ]

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE, default='C', max_length=100)
    deadline = models.DateTimeField(null=True, blank=True, default='')
    owner = models.ForeignKey('UserModel', related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', 'status', 'owner')

    def __str__(self):
        return self.title
