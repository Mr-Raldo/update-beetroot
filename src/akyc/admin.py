# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from django.contrib.admin import register
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from django.utils.safestring import mark_safe

# 
from django.contrib.auth.models import User
from .models import Profile, Subscription, Wallet, WalletTransaction
from business.models import Service
from unfold.decorators import action
from unfold.decorators import display
from dashboards.sites import dashboards_admin_site

from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericListFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
)

class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    INACTIVE = "INACTIVE", _("Inactive")
    CANCELLED = "CANCELLED", _("Cancelled")

class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


class CustomRangeNumericListFilter(RangeNumericListFilter):
    parameter_name = "items_count"
    title = "items"




class ServiceInline(admin.TabularInline):
    model = Service
    fields = ["name",
        "category",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending"]

    # optional: make the inline read-only
    readonly_fields = ["name",
        "category",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True
# Register your models here.


    # def get_queryset(self, request):
    #     return super().get_queryset().annotate(items_count=Count("item", distinct=True))

@admin.register(Subscription, site=dashboards_admin_site)
class SubscriptionAdmin(ModelAdmin):
    pass


@admin.register(Wallet, site=dashboards_admin_site)
class WalletAdmin(ModelAdmin):
    pass


@admin.register(WalletTransaction, site=dashboards_admin_site)
class WalletTransactionAdmin(ModelAdmin):
    pass

