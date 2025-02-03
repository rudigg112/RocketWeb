from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from RocketWebMain.models import DiscordUser


class DiscordUserAdmin(UserAdmin):
    # Поля для отображения в списке пользователей
    list_display = ('discord_id', 'username', 'email', 'get_statuses_display', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('discord_id', 'username', 'email')
    ordering = ('discord_id',)

    # Поля для отображения и редактирования на странице пользователя
    fieldsets = (
        (None, {
            'fields': ('discord_id', 'username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Additional Info', {
            'fields': ('statuses', 'roles', 'avatar_url'),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('discord_id', 'username', 'email', 'password1', 'password2', 'statuses'),
        }),
    )

    def get_statuses_display(self, obj):
        """Возвращает статусы пользователя для отображения в списке."""
        # Если поле `statuses` — ManyToManyField
        return ", ".join([status.name for status in obj.statuses.all()])

        # Если поле `statuses` — JSONField
        # return ", ".join(obj.statuses)

    get_statuses_display.short_description = 'Statuses'


# Регистрируем модель в админке
admin.site.register(DiscordUser, DiscordUserAdmin)
