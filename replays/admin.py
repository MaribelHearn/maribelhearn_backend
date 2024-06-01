from django.contrib import admin
from django.contrib.admin.decorators import register

from django.contrib.admin import ModelAdmin

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
# from django.contrib.auth.models import User, Group

# from unfold.admin import ModelAdmin

from .models import Category, Game, ShotType, Replay


# admin.site.unregister(User)
# admin.site.unregister(Group)
#
#
# @register(User)
# class UserAdmin(BaseUserAdmin, ModelAdmin):
#     pass
#
#
# @register(Group)
# class GroupAdmin(BaseGroupAdmin, ModelAdmin):
#     pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["shot__game__short_name", "difficulty", "type", "shot__name"]
    exclude = ["id"]


@register(Game)
class GameAdmin(ModelAdmin):
    search_fields = ["short_name"]
    list_display = ["id", "short_name", "full_name", "number"]
    exclude = ["id"]


@register(ShotType)
class ShotTypeAdmin(ModelAdmin):
    list_select_related = True
    search_fields = ["game__short_name", "name"]
    exclude = ["id"]


@register(Replay)
class ReplayAdmin(ModelAdmin):
    # list_select_related = ["category"]
    list_display = [
        "id",
        "category",
        "player",
        "score",
        "date",
        "video",
        "verified",
    ]
    # raw_id_fields = ["category"]
    search_fields = ["player", "category__shot__game__short_name"]
    autocomplete_fields = ["category"]
    list_filter = [
        ("verified", admin.BooleanFieldListFilter),
        ("category__type", admin.ChoicesFieldListFilter),
        ("category__difficulty", admin.ChoicesFieldListFilter),
        ("category__region", admin.ChoicesFieldListFilter),
    ]
    list_editable = [
        "score",
        "verified",
        "player",
        "date",
        "video",
        "category",
    ]
    exclude = ["id"]
