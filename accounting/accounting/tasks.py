from app.celery import app

from accounting.models import Account, AuditLog, Balance


@app.task
def pay_salary():
    for account in Account.objects.all():
        if account.balance > 0:
            # send_mail
            #
            # from django.core.mail import
            # send_mail(
            #     "Salary",
            #     f"Great! Your salary is :{account.balance}!",
            #     "asyn-task-tracker@test.com",
            #     [user.public_id],  # should be email
            #     fail_silently=False,
            # )

            Balance.objects.create(account=account, debit=account.balance)
            AuditLog.objects.create(
                user=account.user,
                description=f"Salary for {account.public_id} account was paid",
            )
            AuditLog.objects.create(
                user=account.user,
                description=f"Balance for {account.public_id} account was set to 0$",
            )
