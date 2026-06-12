import mysql.connector
from faker import Faker
import random

fake = Faker()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="passwd1234",
    database="ecommerce_analytics"
)

cursor = conn.cursor()
cursor.execute("USE ecommerce_analytics")

# ── Clear old data ─────────────────────────────────────
print("Clearing old data...")
cursor.execute("DELETE FROM order_items")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")
cursor.execute("ALTER TABLE customers AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE orders AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE order_items AUTO_INCREMENT = 1")
conn.commit()

# ── 1. Generate Customers ──────────────────────────────
print("Inserting customers...")
for _ in range(500):
    cursor.execute("""
        INSERT INTO customers (name, email, city, signup_date)
        VALUES (%s, %s, %s, %s)
    """, (
        fake.name(),
        fake.unique.email(),
        fake.city(),
        fake.date_between(start_date="-2y", end_date="today")
    ))
conn.commit()

# ── 2. Generate Products ───────────────────────────────
print("Inserting products...")
categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys']
for _ in range(100):
    cursor.execute("""
        INSERT INTO products (name, category, price)
        VALUES (%s, %s, %s)
    """, (
        fake.catch_phrase(),
        random.choice(categories),
        round(random.uniform(5.0, 500.0), 2)
    ))
conn.commit()

# ── 3. Generate Orders ─────────────────────────────────
print("Inserting orders...")

# Fetch real customer IDs from the database
cursor.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

statuses = ['pending', 'shipped', 'delivered', 'cancelled']
for _ in range(2000):
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (%s, %s, %s)
    """, (
        random.choice(customer_ids),
        fake.date_between(start_date='-1y', end_date='today'),
        random.choice(statuses)
    ))
conn.commit()

# ── 4. Generate Order Items ────────────────────────────
print("Inserting order items...")

# Fetch real order and product IDs from the database
cursor.execute("SELECT order_id FROM orders")
order_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

for order_id in order_ids:
    for _ in range(random.randint(1, 4)):
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (
            order_id,
            random.choice(product_ids),
            random.randint(1, 5)
        ))
conn.commit()

cursor.close()
conn.close()
print("✅ Done! Database populated successfully.")