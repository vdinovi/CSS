from django import forms
from django.core.mail import send_mail
from css.models import CUser, Room, Course, SectionType, Schedule, Section, Availability
from django.http import HttpResponseRedirect
from settings import DEPARTMENT_SETTINGS, HOSTNAME
import re
from django.forms import ModelChoiceField

#  Login Form
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    #@TODO validate pass?
    @staticmethod
    def validate_password(password):
        if re.match(r'^(?=.*\d)(?=.*[A-Za-z])(?=.*[-._!@#$%^&*?+])[A-Za-z0-9-._!@#$%^&*?+]{8,32}$', password) is None:
            raise ValidationError("Attempted CUser creation with invalid password") 

#  Invite Form
class InviteUserForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def send_invite(self, usertype, request):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        name = first_name + ' ' + last_name
        email = self.cleaned_data['email']
        host = request.META['HTTP_HOST']
        if not re.search(r'http', host):
            host = 'http://' + host
        link = host + '/register?first_name=' + first_name +'&last_name=' + last_name +'&user_type='+ usertype + '&email=' + email
        send_mail('Invite to register for CSS', name + ", you have been invited to register for CSS. Please register using the following link:\n\n "
        + link, 'registration@inviso-css', [self.cleaned_data['email']])

# Registration Form
# @TODO on load, pull fields from query string -> show failure if field not able to be loaded:
#       Fields to pull: email, first_name, last_name, user_type
class RegisterUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_type = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        if kwargs.pop('request') is "GET":
            self.first_name = kwargs.pop('first_name')
            self.last_name = kwargs.pop('last_name')
            self.user_type = kwargs.pop('user_type')
            self.email = kwargs.pop('email')
            self.declared_fields['first_name'].initial = self.first_name
            self.declared_fields['last_name'].initial = self.last_name
            self.declared_fields['email'].initial = self.email
            self.declared_fields['user_type'].initial = self.user_type
            self.declared_fields['user_type'].disabled = True

        super(RegisterUserForm, self).__init__(*args,**kwargs)

    def save(self):
        user = CUser.create(email=self.cleaned_data['email'],
                            password=self.cleaned_data['password2'],
                            user_type=self.cleaned_data['user_type'],
                            first_name=self.cleaned_data['first_name'],
                            last_name=self.cleaned_data['last_name'])
        user.save()
        return user


# Edit User Form
class EditUserForm(forms.Form):
    user_email = forms.CharField(widget=forms.HiddenInput(), initial='a@a.com')
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()

    def save(self):
        user = CUser.get_user(email=self.cleaned_data['user_email'])
        user.set_first_name(self.cleaned_data['first_name'])
        user.set_last_name(self.cleaned_data['last_name'])
        user.set_password(self.cleaned_data['password'])

# Delete Form
class DeleteUserForm(forms.Form):
    email = forms.CharField(label='Confirm email')

    def delete_user(self):
        email = self.cleaned_data['email']
        CUser.get_user(user__username=self.cleaned_data['email']).delete()

class AddRoomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

    def save(self):
        room = Room.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], capacity=self.cleaned_data['capacity'], notes=self.cleaned_data['notes'], equipment=self.cleaned_data['equipment'])
        room.save()
        return room

class EditRoomForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput(), initial='defaultRoom')
    description = forms.CharField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

    def save(self):
        nameString = self.cleaned_data['name']
        room = Room.get_room(nameString)
        room.name = self.cleaned_data['name']
        room.description = self.cleaned_data['description']
        room.capacity = self.cleaned_data['capacity']
        room.notes = self.cleaned_data['notes']
        room.equipment = self.cleaned_data['equipment']
        room.save()

class DeleteRoomForm(forms.Form):
    roomName = forms.CharField(widget=forms.HiddenInput(), initial='defaultRoom')

    def deleteRoom(self):
        nameString=self.cleaned_data['roomName']
        Room.objects.filter(name=nameString).delete()

class EditCourseSectionTypeForm(forms.Form):
    work_units = forms.IntegerField()
    work_hours = forms.IntegerField()

    def save(self):
        name = self.cleaned_data['name']
        work_units = self.cleaned_data['work_units']
        work_hours = self.cleaned_data['work_hours']

class AddCourseSectionTypeForm(forms.Form):
    course = forms.CharField(widget=forms.HiddenInput(), initial='defaultCourse')
    name = forms. MultipleChoiceField(
        required = True,
        widget = forms.RadioSelect,
        choices = SectionType.get_all_section_types_list
    )
    work_units = forms.IntegerField()
    work_hours = forms.IntegerField()

class AddCourseForm(forms.Form):
    course_name = forms.CharField()
    description = forms.CharField()
    equipment_req = forms.CharField()

    def save(self):
        course = Course(name = self.cleaned_data['course_name'],
                      description = self.cleaned_data['description'],
                      equipment_req = self.cleaned_data['equipment_req'])
        course.save();

class DeleteCourseForm(forms.Form):
    course_name = forms.CharField(widget=forms.HiddenInput(), initial='defaultCourse')

    def save(self):
        course = Course.get_course(name=self.cleaned_data['course_name'])
        course.delete()
        return

# @TODO Fix naming -> EditCourseForm
class EditCourseForm(forms.Form):
    course_name = forms.CharField(widget=forms.HiddenInput(), initial='defaultcourse')
    equipment_req = forms.CharField()
    description = forms.CharField()

    def save(self):
        course = Course.get_course(name=self.cleaned_data['course_name'])
        course.set_equipment_req(self.cleaned_data['equipment_req'])
        course.set_description(self.cleaned_data['description'])

class AddSectionTypeForm(forms.Form):
    section_type_name = forms.CharField()

    def save(self):
        SectionType.create(name=self.cleaned_data['section_type_name'])


# Custom ModelChoiceField for faculty full names
class FacultyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

class AddSectionForm(forms.Form):
    academic_term = forms.ModelChoiceField(label='Term', queryset=Schedule.objects.values_list('academic_term', flat=True), empty_label="                    ")
    course = forms.ModelChoiceField(label='Course', queryset=Course.objects.values_list('name', flat=True), empty_label="                   ")
    start_time = forms.TimeField(label='Start Time', input_formats=('%I:%M %p'))
    end_time = forms.TimeField(label='End Time', input_formats=('%I:%M %p'))
    days = forms.CharField(label='Days')
    days = forms.ChoiceField(label='Days', choices=[('MWF', 'MWF'), ('TR', 'TR')])
    faculty = FacultyModelChoiceField(label='Faculty', queryset=CUser.objects.filter(user_type='faculty'))
    room = forms.ModelChoiceField(label='Room', queryset=Room.objects.values_list('name', flat=True), empty_label="                   ")
    capacity = forms.IntegerField()
    section_type = forms.ModelChoiceField(label='Section Type', queryset=SectionType.objects.values_list('name', flat=True), empty_label="                   ")

    def save(self):
        section = Section.create (schedule = Schedule.objects.get(academic_term=self.cleaned_data['academic_term']),
                                  course = Course.objects.get(course=self.cleaned_data['course']),
                                  start_time = self.cleaned_data['start_time'],
                                  end_time = self.cleaned_data['end_time'],
                                  days = self.cleaned_data['days'],
                                  faculty = CUser.get_cuser_by_full_name(self.cleaned_data['faculty']),
                                  room = Room.objects.get(name=self.cleaned_data['room']),
                                  capacity = self.cleaned_data['capacity'],
                                  students_enrolled = 0,
                                  students_waitlisted = 0,
                                  conflict = 'n',
                                  conflict_reason = null,
                                  fault = 'n',
                                  fault_reason = null)
        section.save()
        return

class AddAvailabilityForm(forms.Form):
    DAYS = ('Monday', 'Monday',),('Tuesday','Tuesday'),('Wednesday','Wednesday'), ('Thursday','Thursday',), ('Friday', 'Friday')
    day = forms.ChoiceField(label='Day', choices=DAYS)
    start_time = forms.TimeField(label='Start Time')
    end_time = forms.TimeField(label='End Time')
    level = forms.ChoiceField(label='Type', choices=[('Preferred', 'Preferred'), ('Unavailable','Unavailable')])

    def save(self, email):
        availability = Availability.create(email=email,
                                            day = self.cleaned_data['day'], 
                                            start_time = self.cleaned_data['start_time'],
                                            end_time = self.cleaned_data['end_time'],
                                            level = self.cleaned_data['level'])
        availability.save()

class AddScheduleForm(forms.Form):
    academic_term = forms.CharField(max_length=16)

    def save(self):
        Schedule.create(academic_term=self.cleaned_data['academic_term'],
                        state="active").save()


class UploadForm(forms.Form):
    file = forms.FileField()
