from django.db import models
from django.contrib.postgres.fields import ArrayField

from core.boilerplate.model_template import TemplateModel
from employment_app.model_choices import RestaurantEmployeeChoices
from restaurant_app.models import RestaurantBranch
from user_app.models import User

class RestaurantEmployee(TemplateModel):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    restaurant_branch = models.ForeignKey(
        RestaurantBranch, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=16, choices=RestaurantEmployeeChoices.RESTAURANT_ROLE_CHOICES)
    shift_start = models.TimeField(blank=True, null=True)
    shift_end = models.TimeField(blank=True, null=True)
    shift_days = ArrayField(models.CharField(
        max_length=16, choices=RestaurantEmployeeChoices.DAY_CHOICES))

    def save(self, *args, **kwargs):
        if self.shift_days:
            self.shift_days = list(set(self.shift_days))

        super(RestaurantEmployee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Restaurant Branch Employee"
        verbose_name_plural = "Restaurant Branch Employees"
        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('employee',)),
            models.Index(fields=('restaurant_branch'))
        )





