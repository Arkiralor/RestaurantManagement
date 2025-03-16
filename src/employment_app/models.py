from django.db import models
from core.boilerplate.model_template import TemplateModel
from user_app.models import User

class Company(TemplateModel):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    established = models.IntegerField()
    registration_number = models.CharField(max_length=64)
    registration_authority = models.CharField(max_length=64)
    registration_date = models.DateField()
    registration_expiry = models.DateField()
    registration_proof = models.FileField(upload_to='company/registration_proof')

    def save(self, *args, **kwargs):
        if not self.established:
            self.established = self.created.year
        super(self, Company).save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('id', 'owner'))
        )





