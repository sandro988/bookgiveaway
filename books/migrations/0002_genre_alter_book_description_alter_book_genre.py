# Generated by Django 4.0.10 on 2023-09-28 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("genre_name", models.CharField(max_length=100, unique=True)),
                ("genre_description", models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name="book",
            name="description",
            field=models.TextField(blank=True, default="No description"),
        ),
        migrations.AlterField(
            model_name="book",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.genre"
            ),
        ),
    ]
