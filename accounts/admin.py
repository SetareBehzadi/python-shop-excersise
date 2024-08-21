from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created_at']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "phone_number", "is_admin"]
    list_filter = ("is_admin",)
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["phone_number", "full_name"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_superuser", "last_login", "groups", "user_permissions",]}),
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number','email',  'full_name', 'password1', 'password2'),
        }),
    ]
    search_fields = ('full_name', 'email')
    ordering = ('full_name',)
    filter_horizontal = [
         'groups',"user_permissions",
    ]
    readonly_fields = ["last_login"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)



