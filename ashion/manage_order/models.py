from django.db import models
from logintohome.models import Customer
from manage_product.models import Variant
from user_profile.models import Address
from django.utils import timezone
from manage_coupen.models import Coupons
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )
    payment_method = models.CharField(max_length=10)
    order_date = models.DateTimeField(auto_now_add=True)
    coupon_id = models.ForeignKey(
        Coupons, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.user}'s Order {self.id}"


class OrderedProducts(models.Model):
    STATUS_CHOICES = (
        ("Order confirmed", "Order confirmed"),
        ("Shipped", "Shipped"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned"),
    )

    order_id = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        Variant, on_delete=models.SET_NULL, null=True, blank=True
    )
    size = models.CharField(max_length=5)
    quantity = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )
    status = models.CharField(choices=STATUS_CHOICES)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_date = models.DateField(null=True)

    def set_expected_delivery_date(self):
        # Set expected delivery date based on the current date and time
        if self.order_id and self.order_id.order_date:
            # Calculate expected delivery date (assuming 7 days)
            expected_delivery_date = self.order_id.order_date + timezone.timedelta(
                days=7
            )
            self.delivery_date = expected_delivery_date.date()

    def save(self, *args, **kwargs):
        if self.delivery_date is None:
            self.set_expected_delivery_date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order ID =  {self.id}"


class CancelledOrder(models.Model):
    order_id = models.ForeignKey(OrderedProducts, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    cancel_reason = models.TextField(null=True, blank=True)
    cancel_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled order item: {self.order_id.product} in order {self.order_id.order_id}"


class OrderReturns(models.Model):
    order_id = models.ForeignKey(OrderedProducts, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(null=True, blank=True)
    request_date = models.DateField(auto_now_add=True, null=True)
    pickup_date = models.DateField(null=True, blank=True)

    def set_pick_up_date(self):
        # Set expected delivery date based on the current date and time
        if self.request_date:
            # Calculate expected delivery date (assuming 2 days)
            set_pick_up_date = self.request_date + timezone.timedelta(days=2)
            self.pickup_date = set_pick_up_date

    def save(self, *args, **kwargs):
        self.set_pick_up_date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f" Order_id = {self.order.id} , return status = {self.order.status} "
