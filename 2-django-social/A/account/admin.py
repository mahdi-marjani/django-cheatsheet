from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
