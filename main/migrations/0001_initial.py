# Generated by Django 4.2.11 on 2024-04-27 22:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Courses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "course_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
            ],
            options={
                "verbose_name": "Course",
                "verbose_name_plural": "Courses",
            },
        ),
        migrations.CreateModel(
            name="Groups",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "group_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("group_link", models.CharField(max_length=100)),
                (
                    "group_member_count",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
            ],
            options={
                "verbose_name": "Group",
                "verbose_name_plural": "Groups",
            },
        ),
        migrations.CreateModel(
            name="Clients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("client_name", models.CharField(max_length=100)),
                (
                    "client_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("client_telegram_id", models.CharField(max_length=100)),
                (
                    "client_username",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("client_status", models.BooleanField(default=False)),
                ("client_check_time", models.TimeField(auto_now_add=True, null=True)),
                (
                    "client_check_photo",
                    models.ImageField(blank=True, null=True, upload_to="check_photo/"),
                ),
                ("activation_end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "client_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.courses",
                    ),
                ),
                (
                    "client_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.groups",
                    ),
                ),
            ],
            options={
                "verbose_name": "Client",
                "verbose_name_plural": "Clients",
            },
        ),
    ]
