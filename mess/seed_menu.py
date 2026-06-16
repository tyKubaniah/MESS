import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess.settings')
django.setup()

from orders.models import MenuItem

# 10 Items per profile with realistic Mess pricing assignments
menu_profiles = {
    'BREAKFAST': [
        ("Tea and bread", 50.00), ("Mandazi and tea", 40.00), ("Chapati and tea", 60.00),
        ("Pancakes and milk", 90.00), ("Sausages and eggs", 120.00), ("Omelette and toast", 100.00),
        ("Sweet potatoes and tea", 70.00), ("Arrowroots (nduma) and tea", 80.00),
        ("Cereal with milk", 110.00), ("Fruit salad with yogurt", 130.00)
    ],
    'LUNCH': [
        ("Ugali and sukuma wiki", 60.00), ("Ugali and beef stew", 150.00), ("Rice and beans", 100.00),
        ("Pilau and kachumbari", 180.00), ("Chapati and beans", 110.00), ("Githeri", 80.00),
        ("Mukimo and beef stew", 170.00), ("Fish and ugali", 200.00), ("Chicken and rice", 220.00),
        ("Spaghetti and minced meat", 190.00)
    ],
    'DINNER': [
        ("Ugali and vegetables", 70.00), ("Rice and chicken stew", 200.00), ("Chapati and beef stew", 160.00),
        ("Fish and vegetables", 180.00), ("Mashed potatoes and beef", 190.00), ("Githeri", 80.00),
        ("Vegetable soup and bread", 90.00), ("Spaghetti and vegetable sauce", 130.00),
        ("Pilau and salad", 170.00), ("Beans and chapati", 110.00)
    ],
    'DRINK': [
        ("Orange juice", 70.00), ("Mango juice", 70.00), ("Passion juice", 70.00),
        ("Pineapple juice", 70.00), ("Lemonade", 60.00), ("Soda", 50.00),
        ("Mineral water", 40.00), ("Milkshake", 150.00), ("Iced tea", 80.00),
        ("Energy drink", 120.00)
    ]
}

print("Purging old items layout configuration data...")
MenuItem.objects.all().delete()

print("Synchronizing KDF Pricing Catalog Inventory Matrix...")
for category, items in menu_profiles.items():
    for name, price in items:
        MenuItem.objects.create(name=name, category=category, price=price)
print("Success! 40 structural food items mapped successfully with assigned item prices.")