from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Group

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'role',
        'favorite_group'
    )
    search_fields = ('last_name',)
    list_filter = ('favorite_group',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
