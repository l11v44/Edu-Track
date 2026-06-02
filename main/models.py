from django.db import models

# Create your models here.
class User(models.Model):
    class RoleOfUsers(models.TextChoices):
        Guest = "G" , "Guest"
        Student = "S" , "Student"
        Teacher = "T" , "Teacher"
        Admin = "A" , "Admin"

    role = models.CharField(choices=RoleOfUsers.choices , default=RoleOfUsers.Guest, max_length=1)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.role}  ->  {self.first_name} {self.last_name} "

