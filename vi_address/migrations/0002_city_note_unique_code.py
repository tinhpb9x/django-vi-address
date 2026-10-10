from django.db import migrations, models
from django.db.models import Count


def check_duplicate_codes(apps, schema_editor):
    """Fail early with an actionable message instead of a raw IntegrityError."""
    for model_name in ('City', 'Ward'):
        model = apps.get_model('vi_address', model_name)
        duplicates = (
            model.objects.values('code').annotate(n=Count('id')).filter(n__gt=1).values_list('code', flat=True)
        )
        duplicates = list(duplicates[:10])
        if duplicates:
            raise RuntimeError(
                f"vi_address: duplicate {model_name}.code values {duplicates} prevent adding a unique constraint. "
                "Remove the duplicated rows (or delete all City rows, which cascades to Ward), "
                "then run `migrate` and `insert_data` again."
            )


class Migration(migrations.Migration):

    dependencies = [
        ('vi_address', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(check_duplicate_codes, migrations.RunPython.noop),
        migrations.AddField(
            model_name='city',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='city',
            name='code',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='ward',
            name='code',
            field=models.IntegerField(unique=True),
        ),
    ]
