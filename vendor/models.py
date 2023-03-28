from django.db import models
from account.models import User, UserProfile
from account.utils import send_notificationmail
from datetime import time, date, datetime
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name = 'user', on_delete = models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete = models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=100,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'account/email/admin_approval_mail.html'
                context = {
                        'user':self.user,
                        'is_approved':self.is_approved,
                        'to_email':self.user.email
                    }
                if self.is_approved == True:
                    #send email notification
                    mail_subject = 'Congratulations! Your restaurant has been approved'
                    send_notificationmail(mail_subject,mail_template,context)
                else:
                    #send email notification
                    mail_subject = 'We are sorry you are not eligible to publish your food menu on our marketplace'
                    send_notificationmail(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args, **kwargs)  #Super function allow you to access the save method of vendor class


DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()