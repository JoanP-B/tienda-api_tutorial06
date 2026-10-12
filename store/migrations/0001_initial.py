from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Producto",
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
                ("nombre", models.CharField(max_length=150, unique=True)),
                ("descripcion", models.TextField(blank=True)),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Compra",
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
                ("cantidad", models.PositiveIntegerField()),
                ("total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("creada_en", models.DateTimeField(auto_now_add=True)),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="compras",
                        to="store.producto",
                    ),
                ),
            ],
            options={"ordering": ["-creada_en"]},
        ),
    ]
