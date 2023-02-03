from flask import render_template
from tasks import send_email_task


def send_group_email(recipients, subject, body):
    send_email_task.delay(recipients, subject, body)


def send_group_template_email(recipients, subject, template, **kwargs):
    send_group_email(recipients, subject, render_template(template, **kwargs))


def send_email(recipient, subject, body):
    send_group_email([recipient], subject, body)


def send_template_email(recipient, subject, template, **kwargs):
    send_group_email([recipient], subject, render_template(template, **kwargs))
