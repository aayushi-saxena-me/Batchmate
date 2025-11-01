#!/usr/bin/env python
"""
Generate a secure Django SECRET_KEY for production use.
Run: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("GENERATED SECRET KEY (Copy this to your environment variables):")
    print("="*70)
    print(secret_key)
    print("="*70)
    print("\n⚠️  IMPORTANT: Never commit this key to git!")
    print("   Add it to your deployment platform's environment variables.")
    print("   Variable name: SECRET_KEY")
    print("="*70 + "\n")

