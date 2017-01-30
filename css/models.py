from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 