from django.db import models, IntegrityError
import pyotp
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
import random
# Create your models here.


# user model
class Customer(models.Model):
    username = models.CharField(max_length=100)
    number = models.BigIntegerField(unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=500)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=50, null=True)
    date_joined = models.DateTimeField()
    otp_field = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Generate a referral code if it doesn't exist
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle the case where a non-unique code was generated
            self.referral_code = self.generate_referral_code()
            super().save(*args, **kwargs)

    def generate_referral_code(self):
        # Generate a random 5-character alphanumeric code
        return "".join(random.choices(string.ascii_letters + string.digits, k=5))


# generating otp
def generate_otp(user):
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    user1 = Customer.objects.get(id=user.id)
    user1.otp_field = otp
    user1.save()
    return otp


# Send OTP email
def send_otp_email(instance, otp_code):
    subject = "OTP Verification"
    message = f"Your OTP for verification is: {otp_code}"
    from_email = "muhammedmamu2906@gmail.com"  # Replace with your email
    send_mail(subject, message, from_email, [instance.email])


# signal to post save
@receiver(post_save, sender=Customer)
def generate_and_send_otp(sender, instance, created, **kwargs):
    if created:
        otp_code = generate_otp(instance)
        send_otp_email(instance, otp_code)
