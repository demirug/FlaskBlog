from flask_mail import Message

from application import celery, mail


@celery.task(bind=True)
def send_email_task(self, recipients: [], subject, body):
    try:
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
    except Exception as e:
        self.retry(exc=e, countdown=5)
