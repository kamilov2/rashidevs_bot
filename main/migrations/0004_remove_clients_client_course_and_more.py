# Generated by Django 4.2.11 on 2024-05-02 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_clients_client_course_tarif_groups_group_tarif"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clients",
            name="client_course",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="client_group",
        ),
        migrations.DeleteModel(
            name="Courses",
        ),
        migrations.DeleteModel(
            name="Groups",
        ),
    ]