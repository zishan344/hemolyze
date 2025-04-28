from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class DonatedFund(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=400, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.created_date}"

    class Meta:
        ordering = ['-created_date']
