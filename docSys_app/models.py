from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Members"))
    user_type=models.IntegerField(default=1,choices=user_type_data)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Houses(models.Model):
    id=models.AutoField(primary_key=True)
    house_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Voices(models.Model):
    id=models.AutoField(primary_key=True)
    voice_name=models.CharField(max_length=255, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.voice_name

class Members(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    address=models.TextField()
    house_id=models.ForeignKey(Houses, on_delete=models.SET_NULL, null=True, blank=True)
    voice_id=models.ForeignKey(Voices, on_delete=models.SET_NULL, null=True, blank=True)
    session_start_year=models.DateField()
    has_staff_privileges = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.username

    def get_profile_pic(self):
        """Return uploaded profile pic or default placeholder"""
        if self.profile_pic:
            return self.profile_pic.url
        return "/static/dist/img/default_profile.jpg"   # change to the chosen default
    
    def grant_staff_privileges(self):
        """Grant staff privileges to this member"""
        self.has_staff_privileges = True
        self.save()

    def revoke_staff_privileges(self):
        """Revoke staff privileges from this member"""
        self.has_staff_privileges = False
        self.save()

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    voice_id=models.ForeignKey(Voices,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    member_id=models.ForeignKey(Members,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

"""
class LeaveReportMember(models.Model):
    id=models.AutoField(primary_key=True)
    member_id=models.ForeignKey(Members,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    
    """

class FeedBackMember(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationMember(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")  # stored under MEDIA_ROOT/documents/
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # points to CustomUser
        on_delete=models.CASCADE,
        related_name="uploaded_documents"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)

        elif instance.user_type == 2:
            Staffs.objects.create(admin=instance, address="")

        elif instance.user_type == 3:
            # Safely get default house and voice
            default_house = Houses.objects.first()
            default_voice = Voices.objects.first()

            Members.objects.create(
                admin=instance,
                house_id=default_house if default_house else None,
                voice_id=default_voice if default_voice else None,
                session_start_year="2020-01-01",  # keep if you want only start year
                address="",
                profile_pic="",
                gender=""
            )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    elif instance.user_type == 2:
        instance.staffs.save()
    elif instance.user_type == 3:
        instance.members.save()
