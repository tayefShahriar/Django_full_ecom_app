# Generated by Django 4.1 on 2022-08-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EcomApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
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
                ("name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=40)),
                ("subject", models.CharField(blank=True, max_length=200)),
                ("message", models.CharField(blank=True, max_length=500)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Read", "Read"),
                            ("Closed", "Closed"),
                        ],
                        default="New",
                        max_length=40,
                    ),
                ),
                ("ip", models.CharField(blank=True, max_length=100)),
                ("Note", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
