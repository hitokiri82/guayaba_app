# from django.contrib.auth.forms import UserCreationForm
# from main.models import Schedule

# class UserForm(UserCreationForm):
#     firm = forms.CharField(required=True)

#     def save(self, commit=False):
#         user = super(UserForm, self).save(commit=False)
#         user.save()

#         try:
#             profile = user.get_profile()
#         except:
#             profile = UserProfile(user=user)

#         schedule = Schedule()
#         schedule.save()

#         profile.firm = self.cleaned_data['firm']

#         profile.ownSchedule = schedule
#         profile.save()

#         return user
