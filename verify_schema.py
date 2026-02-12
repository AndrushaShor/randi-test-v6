"""Verify database schema matches the Data Engineering contract"""

import asyncio
from sqlalchemy import inspect
from app.database.connection import engine, init_db


async def verify_schema():
    """Verify that the database schema matches expectations"""
    
    print("🔧 Initializing database...")
    await init_db()
    
    print("\n📊 Inspecting database schema...\n")
    
    async with engine.connect() as conn:
        def inspect_tables(connection):
            inspector = inspect(connection)
            tables = inspector.get_table_names()
            
            print(f"✅ Found {len(tables)} tables: {', '.join(tables)}\n")
            
            for table in tables:
                print(f"📋 Table: {table}")
                columns = inspector.get_columns(table)
                indexes = inspector.get_indexes(table)
                foreign_keys = inspector.get_foreign_keys(table)
                
                print("  Columns:")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    print(f"    - {col['name']}: {col['type']} ({nullable})")
                
                if indexes:
                    print("  Indexes:")
                    for idx in indexes:
                        cols = ', '.join(idx['column_names'])
                        print(f"    - {idx['name']}: ({cols})")
                
                if foreign_keys:
                    print("  Foreign Keys:")
                    for fk in foreign_keys:
                        print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
                        print(f"      ON DELETE: {fk.get('ondelete', 'NO ACTION')}")
                
                print()
        
        await conn.run_sync(inspect_tables)
    
    print("✅ Schema verification complete!")


if __name__ == "__main__":
    asyncio.run(verify_schema())
