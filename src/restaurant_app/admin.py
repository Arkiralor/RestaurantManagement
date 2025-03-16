from django.contrib import admin

from restaurant_app.models import Address, Restaurant, RestaurantBranch, RestaurantBranchPhone, RestaurantBranchMenuSection, \
    RestaurantBranchMenuItem, RestaurantOrderItem, RestaurantOrder


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "city_town", "district_county", "state_province", "country", "postal_code")
    list_per_page = 10
    search_fields = (
        "id",
        "postal_code",
        "city_town",
        "district_county",
        "state_province",
        "country"
    )

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "established")
    search_fields = (
        "id",
        "name",
        "owner__email",
        "owner__username",
        "owner__slug"
    )
    raw_id_fields = ("owner",)

@admin.register(RestaurantBranch)
class RestaurantBranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "manager", "food_license_number")
    search_fields = (
        "id",
        "name",
        "restaurant__name",
        "restaurant__owner__email",
        "restaurant__owner__username",
        "restaurant__owner__slug",
        "manager__email",
        "food_license_number"
    )
    raw_id_fields = (
        "restaurant",
        "manager",
        "address"
    )