from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password, is_superuser=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if is_superuser:
            user = self.model(
                phone_number = phone_number,
            )
        else:
            if not email:
                raise ValueError('Пользователь должен иметь email-адрес')

            user = self.model(
                phone_number = phone_number,
                email=self.normalize_email(email),
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def change_password(self, user_id, password):
        user = MyUser.objects.get(pk=user_id)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number,
            "",
            password,
            is_superuser=True,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("Имя", max_length=50)

    last_name = models.CharField("Фамилия", max_length=50)

    patronymic = models.CharField("Отчество", max_length=50, default="Не указано")

    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=True, null=True)

    phone_number = models.CharField("Номер телефона", max_length=255, unique=True, blank=False, null=False)

    avatar = models.ImageField("Изображение", upload_to='avatars', null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.phone_number + " " + self.first_name

    def model_str(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
