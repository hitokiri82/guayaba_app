from main.models import Firm

from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

# from main.models import UserProfile

admin.site.register(Firm)

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     exclude = ('ownSchedule',)
#     verbose_name_plural = 'profiles'


# # Define a new User admin
# class UserAdmin(UserAdmin):
#     inlines = (UserProfileInline, )


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
