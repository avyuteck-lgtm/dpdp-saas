from django.db import models
from accounts.models import Tenant


class Assessment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    consent_score = models.FloatField(default=0)
    security_score = models.FloatField(default=0)
    breach_score = models.FloatField(default=0)
    children_score = models.FloatField(default=0)
    sdf_score = models.FloatField(default=0)

    total_score = models.FloatField(default=0)
    penalty_exposure = models.FloatField(default=0)
    risk_level = models.CharField(max_length=50)

    # ✅ NEW: Section-wise Legal Status (Added Only)
    section_8_5_status = models.CharField(max_length=50, blank=True, null=True)
    section_8_6_status = models.CharField(max_length=50, blank=True, null=True)
    section_9_status = models.CharField(max_length=50, blank=True, null=True)
    section_10_status = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.total_score}%"