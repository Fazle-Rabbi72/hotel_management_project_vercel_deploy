from decimal import Decimal
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price']

    # Override save_model to check balance when confirming booking
    def save_model(self, request, obj, form, change):
        # Get the original booking status before saving
        original_status = Booking.objects.get(pk=obj.pk).status if obj.pk else None
        
        # Save the booking
        obj.save()

        # If the status is changed to "Confirmed" and balance hasn't been deducted
        if original_status != "Confirmed" and obj.status == "Confirmed":
            # Use obj.total_price for the balance deduction
            if obj.user.balance >= Decimal(obj.total_price):
                # Deduct the balance and save the user
                obj.user.balance -= Decimal(obj.total_price)
                obj.user.save()
                # Send email confirmation for booking completion
                email_subject = "Booking Completed"
                email_body = render_to_string('booking_confirm_mail.html', {
                    'first_name': obj.user.first_name,
                    'last_name': obj.user.last_name,
                    'hotel_name': obj.room.hotel.name,
                    'booking_date': obj.created_at.strftime('%Y-%m-%d'),
                    'check_in_date': obj.check_in_date.strftime('%Y-%m-%d') if obj.check_in_date else "N/A",
                    'check_out_date': obj.check_out_date.strftime('%Y-%m-%d') if obj.check_out_date else "N/A",
                })
                
                # Send the email
                email = EmailMultiAlternatives(email_subject, '', to=[obj.user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            else:
                # If balance is insufficient, raise a validation error
                raise ValidationError("Insufficient balance to complete the booking.") 

# Register the admin model
admin.site.register(Booking, BookingAdmin)
