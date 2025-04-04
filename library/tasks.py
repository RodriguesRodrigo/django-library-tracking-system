from datetime import date

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Loan


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'''
                Hello {loan.member.user.username},\n\n
                You have successfully loaned "{book_title}".\n
                Please return it by the due date.''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    all_loans = Loan.objects.filter(is_returned=False, due_date__lt=date.today())

    for loan in all_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned overdue',
            message=f'''Hello {loan.member.user.username},\n\n Please return the "{book_title}".''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
