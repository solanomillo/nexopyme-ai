from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

_USER_READONLY_FIELDS = tuple(
    field.name
    for field in User._meta.fields
    if field.name not in ("id", "password")
)
_GROUP_READONLY_FIELDS = tuple(
    field.name for field in Group._meta.fields if field.name != "id"
)
_USER_FIELDSETS = (
    (None, {"fields": ("username",)}),
    ("Información personal", {"fields": ("first_name", "last_name", "email")}),
    (
        "Permisos",
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        },
    ),
    ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
)


class ReadOnlyAdminMixin:
    """Impide crear, modificar o eliminar desde Django Admin (T-19)."""

    def has_add_permission(self, request: object, obj: object = None) -> bool:
        return False

    def has_change_permission(
        self,
        request: object,
        obj: object = None,
    ) -> bool:
        return False

    def has_delete_permission(
        self,
        request: object,
        obj: object = None,
    ) -> bool:
        return False


@admin.register(User)
class UserAdmin(ReadOnlyAdminMixin, BaseUserAdmin, ModelAdmin):
    fieldsets = _USER_FIELDSETS
    readonly_fields = _USER_READONLY_FIELDS


@admin.register(Group)
class GroupAdmin(ReadOnlyAdminMixin, BaseGroupAdmin, ModelAdmin):
    readonly_fields = _GROUP_READONLY_FIELDS

