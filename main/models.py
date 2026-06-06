from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    class RoleOfUsers(models.TextChoices):
        Guest = "G" , "Guest"
        Student = "S" , "Student"
        Teacher = "T" , "Teacher"
        Admin = "A" , "Admin"

    role = models.CharField(choices=RoleOfUsers.choices , default=RoleOfUsers.Guest, max_length=20)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return f"{self.role}  ->  {self.first_name} {self.last_name} "

