from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField


class Link(models.Model):
    short_url = models.URLField(max_length=7)
    long_url = models.URLField(max_length=150)
    user_id = models.ForeignKey(User, related_name="links", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class QRCode(models.Model):
    link_id = models.OneToOneField(
        Link, related_name="qr_code", on_delete=models.CASCADE
    )
    qr_image = CloudinaryField(
        "qr_image", folder="qr_codes/", resource_type="image", blank=True, null=True
    )
    public_id = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    size = models.IntegerField(default=300, help_text="QR code size in pixels")
    fill_color = models.CharField(max_length=20, default="black")
    back_color = models.CharField(max_length=20, default="white")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "QR Code"
        verbose_name_plural = "QR Codes"

    # def __str__(self):
    #     return f"QR Code for {self.link_id[:50]}..."
