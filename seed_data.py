import os
import django
from django.conf import settings

# Configure Django settings (only if running as a standalone script)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from items.models import Product
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

def create_sample_products():
    if Product.objects.exists():
        print("Products already exist. Skipping seeding.")
        return

    products_data = [
        {
            "name": "Stylish T-Shirt",
            "description": "Comfortable and trendy cotton t-shirt, perfect for everyday wear.",
            "price": 25.99,
            "stock": 100,
            "image_url": "https://via.placeholder.com/300x200/FF5733/FFFFFF?text=T-Shirt"
        },
        {
            "name": "Designer Jeans",
            "description": "High-quality denim jeans with a modern fit, designed for durability.",
            "price": 69.99,
            "stock": 50,
            "image_url": "https://via.placeholder.com/300x200/3366FF/FFFFFF?text=Jeans"
        },
        {
            "name": "Leather Wallet",
            "description": "Genuine leather wallet with multiple card slots and a coin pocket.",
            "price": 35.00,
            "stock": 75,
            "image_url": "https://via.placeholder.com/300x200/33FF99/FFFFFF?text=Wallet"
        },
        {
            "name": "Smartwatch Pro",
            "description": "Feature-rich smartwatch with health tracking, notifications, and long battery life.",
            "price": 199.50,
            "stock": 30,
            "image_url": "https://via.placeholder.com/300x200/FFC300/FFFFFF?text=Smartwatch"
        },
        {
            "name": "Wireless Headphones",
            "description": "Over-ear headphones with superior sound quality and noise cancellation.",
            "price": 120.00,
            "stock": 40,
            "image_url": "https://via.placeholder.com/300x200/C70039/FFFFFF?text=Headphones"
        },
    ]

    for data in products_data:
        product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"]
        )
        
        # Download image and save to model
        if data.get("image_url"):
            response = requests.get(data["image_url"], stream=True)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                # Use a proper filename, e.g., from the URL or generated
                filename = os.path.basename(data["image_url"].split("?")[0]) # Basic attempt to get filename
                if not filename or '.' not in filename: # Fallback if URL doesn't give good filename
                    filename = f"{data['name'].replace(' ', '_').lower()}.png"
                product.image.save(filename, File(img_temp), save=False)
        
        product.save()
        print(f"Created product: {product.name}")

if __name__ == '__main__':
    print("Seeding sample products...")
    create_sample_products()
    print("Seeding complete.")