# Generated manually to remove SKU unique constraint per user
# This allows multiple products with the same SKU for the same user

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_rename_inventory_p_created__idx_inventory_p_created_00cd94_idx'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set(),  # Remove the unique constraint on (sku, created_by)
        ),
    ]

