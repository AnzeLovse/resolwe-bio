# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-15 07:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resolwe_bio_kb", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                blank=True,
                default=[],
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="feature", name="name", field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name="feature",
            name="sub_type",
            field=models.CharField(
                choices=[
                    (b"protein-coding", b"Protein-coding"),
                    (b"pseudo", b"Pseudo"),
                    (b"rRNA", b"rRNA"),
                    (b"ncRNA", b"ncRNA"),
                    (b"snRNA", b"snRNA"),
                    (b"snoRNA", b"snoRNA"),
                    (b"tRNA", b"tRNA"),
                    (b"asRNA", b"asRNA"),
                    (b"other", b"Other"),
                    (b"unknown", b"Unknown"),
                ],
                max_length=20,
            ),
        ),
    ]
