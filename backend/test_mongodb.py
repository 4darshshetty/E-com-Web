import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_connection():
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017/")
        # Test connection
        await client.admin.command('ping')
        print("[OK] MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"[OK] Available databases: {db_list}")
        
        # Check ecommerce_db
        db = client["ecommerce_db"]
        collections = await db.list_collection_names()
        print(f"[OK] Collections in ecommerce_db: {collections}")
        
        # Count documents
        users_count = await db.users.count_documents({})
        products_count = await db.products.count_documents({})
        orders_count = await db.orders.count_documents({})
        
        print(f"[OK] Users: {users_count}")
        print(f"[OK] Products: {products_count}")
        print(f"[OK] Orders: {orders_count}")
        
        client.close()
        return True
    except Exception as e:
        print(f"[ERROR] MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    exit(0 if result else 1)

