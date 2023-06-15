from django.contrib.auth.models import BaseUserManager, Group


class UserManager(BaseUserManager):
    """
    This class is used to customize the fields that will be
    required for authorized users and for staff users
    """

    def create_user(
        self,
        identification_number=None,
        first_name=None,
        last_name=None,
        password=None,
    ):
        if not first_name:
            raise ValueError("Debes ingresar tu nombre")
        if not identification_number:
            raise ValueError("Debes ingresar tu rut")

        user = self.model(
            identification_number=identification_number,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        identification_number=None,
        first_name=None,
        last_name=None,
        password=None,
    ):
        user = self.create_user(identification_number, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        user_groups = Group.objects.get(name="admin")
        user.groups.add(user_groups)
        return user
