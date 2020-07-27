from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin


class UserManager(BaseUserManager):
    """Provides helper functiosn for creating a user"""

    def create_user(self, email, password=None, **extra_fields):
        """create and save a new user"""

        if not email:
            raise ValueError('Users must have an email address')

        # We can access the model that the manager is for through the
        # self.model call. self.normalize_email comes with BaseUserManager
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password comes with AbstractBaseUser
        user.set_password(password)

        # This allows us to use any db
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign UserManager
    objects = UserManager()

    USERNAME_FIELD = 'email'
