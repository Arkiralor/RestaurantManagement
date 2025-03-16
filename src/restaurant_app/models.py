import pandas as pd

from django.db import models
from django.contrib.postgres.fields import ArrayField


from core.boilerplate.model_template import TemplateModel
from employment_app.models import RestaurantEmployee
from restaurant_app.model_choices import RestaurantModelChoices, RestaurantBranchMenuItemChoices
from user_app.models import User

from restaurant_app import logger


class Address(TemplateModel):
    line_01 = models.CharField(max_length=128)
    line_02 = models.CharField(max_length=128, blank=True, null=True)
    city_town = models.CharField(max_length=128)
    district_county = models.CharField(max_length=128)
    state_province = models.CharField(max_length=128)
    country = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        self.district_county = self.district_county.title()
        self.state_province = self.state_province.title()
        self.country = self.country.title()

        super(self, Address).save(*args, **kwargs)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = (
            models.Index(fields=('id', )),
            models.Index(fields=('city_town', 'district_county',
                         'state_province', 'country', 'postal_code'))
        )


class Restaurant(TemplateModel):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    established = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.established:
            self.established = self.created.year
        super(self, Restaurant).save(*args, **kwargs)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('id', 'owner'))
        )


class RestaurantBranch(TemplateModel):
    name = models.CharField(max_length=64, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL)
    food_license_provider = models.CharField(
        max_length=32,
        choices=RestaurantModelChoices.FOOD_LICENSE_PROVIDER_CHOICES
    )
    food_license_number = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.food_license_number:
            self.food_license_number = self.food_license_number.upper()

        if not self.manager:
            # Need to set a point of contact for every single restaurant branch, even if there is no manager on record.
            self.manager = self.restaurant.owner

        self.find_branch_name()

        super(self, RestaurantBranch).save(*args, **kwargs)

    def find_branch_name(self):
        """
        Method to proceduraly generate a branch name if none is provided.
        """
        if (not self.name) and self.address:
            if self.address.line_01 and (not self.address.line_02):
                try:
                    self.name = self.address.line_01.replace(
                        " ", "").split(",")[-1]
                except Exception as ex:
                    logger.exception(f"{ex}")
            elif self.address.line_02:
                try:
                    self.name = self.address.line_02.replace(
                        " ", "").split(",")[-1]
                except Exception as ex:
                    logger.exception(f"{ex}")

            else:
                self.name = self.address.city_town
        else:
            pass

    class Meta:
        verbose_name = "Restaurant Branch"
        verbose_name_plural = "Restaurant Branches"
        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('restaurant', 'address'))
        )


class RestaurantBranchPhone(TemplateModel):
    restaurant_branch = models.ForeignKey(
        RestaurantBranch, on_delete=models.CASCADE)
    isd_code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        if not self.isd_code.startswith("+"):
            self.isd_code = f"+{self.isd_code}"

        super(self, RestaurantBranchPhone).save(*args, **kwargs)


class RestaurantBranchMenuSection(TemplateModel):
    name = models.CharField(max_length=64, blank=True, null=True)
    restaurant_branch = models.ForeignKey(
        RestaurantBranch, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "restaurant_branch")


class RestaurantBranchMenuItem(TemplateModel):
    section = models.ForeignKey(
        RestaurantBranchMenuSection, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=64)
    currency = models.CharField(
        max_length=8, choices=RestaurantBranchMenuItemChoices.CURRENCY_CHOICES)
    unit_price = models.DecimalField(decimal_places=2)
    discount = models.DecimalField(
        decimal_places=2, null=False, blank=False, default=0.00)

    class Meta:
        unique_together = ("section", "iten")
        indexes = (
            models.Index(fields=("id",)),
            models.Index(fields=("section", "item_name", "unit_price"))
        )

    @property
    def price(self):
        discount_amount = (self.unit_price*(self.discount/100))
        return self.unit_price - discount_amount


class RestaurantOrderItem(TemplateModel):
    item = models.ForeignKey(RestaurantBranchMenuItem, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField(default=1)
    total = models.DecimalField(decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.total or self.total == 0:
            self.total = self.item.price * self.quantity

        super(RestaurantOrderItem, self).save(*args, **kwargs)

    class Meta:
        indexes = (
            models.Index(fields=("id",)),
            models.Index(fields=("item",))
        )


class RestaurantOrder(TemplateModel):
    branch = models.ForeignKey(RestaurantBranch, on_delete=models.CASCADE) ## Yes, this breaks normalization, but we need it here for easier querrying.
    server = models.ForeignKey(RestaurantEmployee, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(RestaurantOrderItem)
    additional_discount_percentage = models.DecimalField(decimal_places=2)
    total = models.DecimalField(decimal_places=2)

    def save(self, *args, **kwargs):
        ##TODO: Make signal to log if server's log is not "SERVER"

        if self.branch != self.server.restaurant_branch:
            logger.exception(f"Cannot create this order as the server is not authorised to create orders for this restaurant.")
            return None
        
        if not self.total:
            no_discount_total = sum([item.total for item in self.items.all()])
            self.total = no_discount_total - (no_discount_total * (self.additional_discount_percentage/100))

        super(RestaurantOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Restaurant Order"
        verbose_name_plural = "Restaurant Orders"
        indexes = (
            models.Index(fields=("id",)),
            models.Index(fields=("branch", "server"))
        )
