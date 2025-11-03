#!/usr/bin/env python
"""
Automated test script for user data isolation.
Run with: python test_user_isolation.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    print("Make sure you're in the project directory and Django is installed.")
    sys.exit(1)

from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction
from decimal import Decimal


def test_user_isolation():
    """Test that user data is properly isolated"""
    print("=" * 60)
    print("Testing User Data Isolation")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        # Get or create test users
        print("\n1. Setting up test users...")
        user1, created = User.objects.get_or_create(
            username='testuser1',
            defaults={'email': 'testuser1@example.com'}
        )
        if created:
            user1.set_password('testpass123')
            user1.save()
            print("   ✅ Created testuser1")
        else:
            print("   ✅ Using existing testuser1")
        
        user2, created = User.objects.get_or_create(
            username='testuser2',
            defaults={'email': 'testuser2@example.com'}
        )
        if created:
            user2.set_password('testpass123')
            user2.save()
            print("   ✅ Created testuser2")
        else:
            print("   ✅ Using existing testuser2")
        
        # Clean up any existing test data
        print("\n2. Cleaning up old test data...")
        Product.objects.filter(sku__startswith='TEST').delete()
        Category.objects.filter(name__startswith='Test Category').delete()
        Supplier.objects.filter(name__startswith='Test Supplier').delete()
        
        # Create data for user1
        print("\n3. Creating test data for user1...")
        cat1 = Category.objects.create(
            name='Test Category 1',
            description='User1 category',
            created_by=user1
        )
        sup1 = Supplier.objects.create(
            name='Test Supplier 1',
            email='supplier1@test.com',
            created_by=user1
        )
        prod1 = Product.objects.create(
            name='Test Product 1',
            sku='TEST001',
            quantity=10,
            cost_price=Decimal('100.00'),
            selling_price=Decimal('150.00'),
            created_by=user1,
            category=cat1,
            supplier=sup1
        )
        print("   ✅ Created category, supplier, product for user1")
        
        # Create data for user2
        print("\n4. Creating test data for user2...")
        cat2 = Category.objects.create(
            name='Test Category 2',
            description='User2 category',
            created_by=user2
        )
        sup2 = Supplier.objects.create(
            name='Test Supplier 2',
            email='supplier2@test.com',
            created_by=user2
        )
        prod2 = Product.objects.create(
            name='Test Product 2',
            sku='TEST002',
            quantity=20,
            cost_price=Decimal('200.00'),
            selling_price=Decimal('300.00'),
            created_by=user2,
            category=cat2,
            supplier=sup2
        )
        print("   ✅ Created category, supplier, product for user2")
        
        # Test 1: Category isolation
        print("\n5. Testing category isolation...")
        user1_cats = Category.objects.filter(created_by=user1)
        user2_cats = Category.objects.filter(created_by=user2)
        
        if cat1 in user1_cats and cat2 not in user1_cats:
            print("   ✅ User1 sees only their categories")
            tests_passed += 1
        else:
            print("   ❌ User1 can see user2's categories!")
            tests_failed += 1
        
        if cat2 in user2_cats and cat1 not in user2_cats:
            print("   ✅ User2 sees only their categories")
            tests_passed += 1
        else:
            print("   ❌ User2 can see user1's categories!")
            tests_failed += 1
        
        # Test 2: Product isolation
        print("\n6. Testing product isolation...")
        user1_prods = Product.objects.filter(created_by=user1)
        user2_prods = Product.objects.filter(created_by=user2)
        
        if prod1 in user1_prods and prod2 not in user1_prods:
            print("   ✅ User1 sees only their products")
            tests_passed += 1
        else:
            print("   ❌ User1 can see user2's products!")
            tests_failed += 1
        
        if prod2 in user2_prods and prod1 not in user2_prods:
            print("   ✅ User2 sees only their products")
            tests_passed += 1
        else:
            print("   ❌ User2 can see user1's products!")
            tests_failed += 1
        
        # Test 3: Supplier isolation
        print("\n7. Testing supplier isolation...")
        user1_sups = Supplier.objects.filter(created_by=user1)
        user2_sups = Supplier.objects.filter(created_by=user2)
        
        if sup1 in user1_sups and sup2 not in user1_sups:
            print("   ✅ User1 sees only their suppliers")
            tests_passed += 1
        else:
            print("   ❌ User1 can see user2's suppliers!")
            tests_failed += 1
        
        # Test 4: Unique constraints per user
        print("\n8. Testing unique constraints per user...")
        
        # Same name, different users - should work
        try:
            cat3 = Category.objects.create(
                name='Test Category 1',  # Same name as cat1
                created_by=user2  # But different user
            )
            print("   ✅ Different users can have same category name")
            tests_passed += 1
            cat3.delete()
        except Exception as e:
            print(f"   ❌ Unique constraint too strict: {e}")
            tests_failed += 1
        
        # Same name, same user - should fail
        try:
            Category.objects.create(
                name='Test Category 1',  # Same name
                created_by=user1  # Same user
            )
            print("   ❌ Duplicate category name allowed for same user!")
            tests_failed += 1
        except Exception as e:
            print("   ✅ Duplicate category name correctly prevented")
            tests_passed += 1
        
        # Same SKU, different users - should work
        try:
            prod3 = Product.objects.create(
                name='Test Product 3',
                sku='TEST001',  # Same SKU as prod1
                quantity=5,
                created_by=user2  # But different user
            )
            print("   ✅ Different users can have same SKU")
            tests_passed += 1
            prod3.delete()
        except Exception as e:
            print(f"   ❌ Unique constraint too strict: {e}")
            tests_failed += 1
        
        # Same SKU, same user - should fail
        try:
            Product.objects.create(
                name='Test Product 4',
                sku='TEST001',  # Same SKU
                quantity=3,
                created_by=user1  # Same user
            )
            print("   ❌ Duplicate SKU allowed for same user!")
            tests_failed += 1
        except Exception as e:
            print("   ✅ Duplicate SKU correctly prevented")
            tests_passed += 1
        
        # Test 5: Check created_by is set
        print("\n9. Testing created_by fields...")
        all_cats = Category.objects.all()
        cats_with_user = Category.objects.exclude(created_by__isnull=True)
        
        if all_cats.count() == cats_with_user.count():
            print("   ✅ All categories have created_by")
            tests_passed += 1
        else:
            print(f"   ❌ Some categories missing created_by ({all_cats.count() - cats_with_user.count()})")
            tests_failed += 1
        
        # Cleanup
        print("\n10. Cleaning up test data...")
        Transaction.objects.filter(product__sku__startswith='TEST').delete()
        Product.objects.filter(sku__startswith='TEST').delete()
        Category.objects.filter(name__startswith='Test Category').delete()
        Supplier.objects.filter(name__startswith='Test Supplier').delete()
        print("   ✅ Cleanup complete")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 60)
    
    if tests_failed == 0:
        print("✅ All tests passed! User isolation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    exit_code = test_user_isolation()
    sys.exit(exit_code)

