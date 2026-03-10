import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

all_products = [
    {
        "name": 'Temple Gold Choker',
        "price": 85000.0,
        "price_display": '₹85,000',
        "oldPrice": 95000.0,
        "oldPrice_display": '₹95,000',
        "discount": '10%',
        "category": 'Neckpiece',
        "section": 'Women',
        "description": 'Exquisitely crafted 22K gold choker featuring traditional temple motifs and high-grade rubies.',
        "details": ['Material: 22K Yellow Gold', 'Weight: 45.5g', 'BIS Hallmarked'],
        "images": [
            'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1515562141207-7a18b5ce7142?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1611085583191-a3b1a308c1db?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?auto=format&fit=crop&q=80&w=800'
        ]
    },
    {
        "name": 'Heritage Nakshi Bangle',
        "price": 42500.0,
        "price_display": '₹42,500',
        "category": 'Bangles',
        "section": 'Women',
        "description": 'Hand-carved Nakshi work bangle with intricate floral patterns.',
        "details": ['Material: 22K Gold', 'Weight: 24g', 'Traditional Handcraft'],
        "images": [
            'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&q=80&w=800'
        ]
    },
    {
        "name": 'Antique Jhumka Set',
        "price": 28900.0,
        "price_display": '₹28,900',
        "oldPrice": 34000.0,
        "oldPrice_display": '₹34,000',
        "discount": '15%',
        "category": 'Earrings',
        "section": 'Women',
        "description": 'Classic antique finish Jhumkas with pearl droppings.',
        "details": ['Material: Gold Polished', 'Type: Antique', 'Stone: Pearl'],
        "images": [
            'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1515562141207-7a18b5ce7142?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1611085583191-a3b1a308c1db?auto=format&fit=crop&q=80&w=800'
        ]
    },
    {
        "name": 'Mens Urban Bracelet',
        "price": 18500.0,
        "price_display": '₹18,500',
        "category": 'Bracelets',
        "section": 'Men',
        "description": 'Bold and masculine 18K gold bracelet with a modern link design.',
        "details": ['Material: 18K Gold', 'Length: 8.5 inch', 'Design: Urban Links'],
        "images": [
            'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1598560937024-c7f863289652?auto=format&fit=crop&q=80&w=800',
            'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&q=80&w=800'
        ]
    }
]

async def seed():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    # Categories to seed
    categories = [
        {
            "name": "Women", 
            "slug": "women", 
            "subcategories": [
                "Anklets", "Hip Chain", "Adjustable Bangle", "Jumkhas",
                "Diamond Replica", "Bangles", "Bracelet", "Chains",
                "Earrings", "Neckpiece", "Hindu God Chains",
                "Hindu Thali chains", "Rings", "Toe Ring", "Traditional"
            ]
        },
        {
            "name": "Men", 
            "slug": "men", 
            "subcategories": ["Bracelets", "Chains", "Hindu God Chains", "Cross Chains"]
        },
        {
            "name": "Kids", 
            "slug": "kids", 
            "subcategories": ["Earrings", "Neckpiece", "Bracelets", "Chains"]
        }
    ]
    
    # Clear existing
    await db["products"].delete_many({})
    await db["categories"].delete_many({})
    
    # Insert new
    await db["products"].insert_many(all_products)
    await db["categories"].insert_many(categories)
    
    print(f"Seeded {len(all_products)} products and {len(categories)} categories.")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
