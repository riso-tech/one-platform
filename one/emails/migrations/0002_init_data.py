from django.conf import settings
from django.db import migrations


def add_email_template_forward(apps, schema_editor):
    """Auto create Email template"""
    AllauthTemplate = apps.get_model("emails", "AllauthTemplate")

    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    group_ctt = ContentType.objects.get_for_model(AllauthTemplate)
    Permission.objects.create(
        name="can get list of email template",
        content_type=group_ctt,
        codename="list_allauthtemplate",
    )

    subjects = {
        "allauth_signup": "account/email/email_confirmation_signup",
        "allauth_reset": "account/email/password_reset_key",
        "allauth_confirm": "account/email/email_confirmation",
        "allauth_unknown": "account/email/unknown_account",
    }
    path = settings.TEMPLATES[0]["DIRS"][0]

    for language in settings.LANGUAGES:
        for subject in subjects:
            AllauthTemplate.objects.create(
                code=subject,
                language=language[0],
                is_protected=True,
                subject=open(
                    "{0}/{1}_subject.txt".format(path, subjects[subject]),
                    "r",
                    encoding="utf-8",
                ).read(),
                content=open(
                    "{0}/{1}_message.html".format(path, subjects[subject]),
                    "r",
                    encoding="utf-8",
                ).read(),
            )


def add_email_template_backward(apps, schema_editor):
    """Delete all Email template"""
    AllauthTemplate = apps.get_model("emails", "AllauthTemplate")
    AllauthTemplate.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("emails", "0001_initial")]

    operations = [
        migrations.RunPython(add_email_template_forward, add_email_template_backward)
    ]
