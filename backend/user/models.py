import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, default='', unique=True)
    username = models.CharField(
        max_length=255, default='', blank=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['created_on', 'updated_on']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_pics = models.ImageField(
        default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Instructor(AbstractBaseUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, default='', unique=True)
    username = models.CharField(
        max_length=255, default='', blank=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=True)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['created_on', 'updated_on']

    def __str__(self):
        return self.email


class InstructorProfile(models.Model):
    user = models.ForeignKey(
        Instructor, on_delete=models.CASCADE)
    profile_pics = models.ImageField(
        default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Course(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255)
    what_you_learn = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    targeted_audience = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="courses")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_hours = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at', 'updated_at']

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Cartitems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.IntegerField(default=0)


class WatchList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)


class Watchitems(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user} reviewed {self.course}"


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
