from flask_mail import Message

from extensions import celery, mail


@celery.task
def send_email_task(recipients: [], subject, body):
    for recipient in recipients:
        from worker import flask_app
        with flask_app.app_context():
            mail.send(
                Message(
                    recipients=[recipient],
                    subject=subject,
                    body=body
                )
            )
