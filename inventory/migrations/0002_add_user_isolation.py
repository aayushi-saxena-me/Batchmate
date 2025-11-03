# Generated migration for user data isolation
# This migration adds created_by fields and handles existing data

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_existing_data_to_default_user(apps, schema_editor):
    """
    Assign existing records without created_by to the first available user.
    If no users exist, this will need to be handled manually.
    """
    Category = apps.get_model('inventory', 'Category')
    Supplier = apps.get_model('inventory', 'Supplier')
    Product = apps.get_model('inventory', 'Product')
    Transaction = apps.get_model('inventory', 'Transaction')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    
    # Get first user (should be superuser if exists)
    default_user = User.objects.first()
    
    if default_user:
        # Assign existing records to default user
        Category.objects.filter(created_by__isnull=True).update(created_by=default_user)
        Supplier.objects.filter(created_by__isnull=True).update(created_by=default_user)
        Product.objects.filter(created_by__isnull=True).update(created_by=default_user)
        Transaction.objects.filter(created_by__isnull=True).update(created_by=default_user)
        print(f"Assigned existing records to user: {default_user.username}")
    else:
        # If no users exist, we can't assign - raise error
        raise ValueError(
            "No users found in database. Please create a user first:\n"
            "1. Run: python manage.py migrate auth\n"
            "2. Run: python manage.py createsuperuser\n"
            "3. Then run this migration again"
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        # Step 1: Add created_by to Category as nullable first
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='categories',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Step 2: Add created_by to Supplier as nullable first
        migrations.AddField(
            model_name='supplier',
            name='created_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='suppliers',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Step 3: Change Product.created_by from SET_NULL to CASCADE (but keep nullable for now)
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='products',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Step 4: Change Transaction.created_by from SET_NULL to CASCADE (but keep nullable for now)
        migrations.AlterField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Step 5: Assign existing data to default user
        migrations.RunPython(assign_existing_data_to_default_user, migrations.RunPython.noop),
        
        # Step 6: Remove unique constraint from Category.name (will add per-user constraint)
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        
        # Step 7: Remove unique constraint from Product.sku (will add per-user constraint)
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(help_text='Stock Keeping Unit', max_length=50),
        ),
        
        # Step 8: Now make created_by required (NOT NULL)
        migrations.AlterField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='categories',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        migrations.AlterField(
            model_name='supplier',
            name='created_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='suppliers',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='products',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        migrations.AlterField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        
        # Step 9: Add per-user unique constraints
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'created_by')},
        ),
        
        migrations.AlterUniqueTogether(
            name='supplier',
            unique_together={('name', 'created_by')},
        ),
        
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('sku', 'created_by')},
        ),
        
        # Step 10: Add index on created_by for performance
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_by'], name='inventory_p_created__idx'),
        ),
    ]

