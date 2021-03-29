from django.contrib import admin
from login.models import Customer,RoomManager
from booking.models import Contact,Rooms,Booking
from django.core.mail import EmailMessage
from django.http import HttpResponse
import csv
from io import StringIO

email = EmailMessage('Booking Info', 'Hi, \nPlease find the attached csv for booking info.', 'from-email',
            ['jasil1689@gmail.com'])

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Rooms)
admin.site.register(RoomManager)


class BookingExportCsvMixin:
    def export_as_csv(self, request, queryset):
        Bookings = Booking.objects.all().only("room_no", "user_id", "start_day", "end_day", "amount", "booked_on"),
        filename = "Bookings_report.csv"
        filename = StringIO()
        formatted_field_names = ["room_no", "user_id", "start_day", "end_day", "amount", "booked_on"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Bookings_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)
        for booking in queryset:
            writer.writerow([booking.room_no,booking.user_id,booking.start_day,booking.end_day,booking.amount,booking.booked_on])

        email.attach('Bookings_report.csv', response.getvalue(), 'text/csv')
        email.send(fail_silently=False)
        success = True
        return response

class BookingList(admin.ModelAdmin, BookingExportCsvMixin):
        list_display = ('room_no', 'user_id', 'start_day', 'end_day', 'amount', 'booked_on')
        list_filter = ('room_no', 'user_id')
        search_fields = ('room_no', 'user_id')
        actions = ["export_as_csv"]

admin.site.register(Booking, BookingList)


