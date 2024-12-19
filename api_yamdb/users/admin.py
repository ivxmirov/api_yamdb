from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role')
    search_fields = ('email',)
    ordering = ('email',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
