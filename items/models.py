from django.db import models
from accounts.models import User

university_list = [
    ("AASTU", "Addis Ababa Science and Technology Univesity"),
]

# Create your models here.
class ItemPost(models.Model):
    UNIVERSITY_CHOICES = university_list
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=100)
    description = models.TextField()
    location_text = models.CharField(max_length=255)
    date_of_event = models.DateField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.telegram_username})"
    
class ContactRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    item = models.ForeignKey(ItemPost, on_delete=models.CASCADE, related_name="contact_requests")

    def __str__(self):
        return f"Request from {self.from_user.telegram_username} to {self.to_user.telegram_username} for {self.item.title}"