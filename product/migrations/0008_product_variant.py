# Generated by Django 4.1 on 2022-09-08 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0007_size_variants"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="variant",
            field=models.CharField(
                choices=[
                    ("Name", "Name"),
                    ("Size", "Size"),
                    ("Color", "Color"),
                    ("Size-Color", "Size-Color"),
                ],
                default="None",
                max_length=20,
            ),
        ),
    ]
