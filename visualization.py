import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connecting to MySQL 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="passwd1234",
    database="ecommerce_analytics"
)

# Revenue by Category 
query1 = """
    SELECT p.category, ROUND(SUM(oi.quantity * p.price), 2) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY p.category
    ORDER BY revenue DESC;
"""
df1 = pd.read_sql(query1, conn)

plt.figure(figsize=(10, 6))
plt.bar(df1['category'], df1['revenue'], color='steelblue')
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('revenue_by_category.png')
plt.show()
print(" Chart 1 saved!")

# Monthly Revenue Trend 
query2 = """
    SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
           ROUND(SUM(oi.quantity * p.price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status != 'cancelled'
    GROUP BY month
    ORDER BY month;
"""
df2 = pd.read_sql(query2, conn)

plt.figure(figsize=(12, 6))
plt.plot(df2['month'], df2['revenue'], marker='o', color='steelblue', linewidth=2)
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_revenue.png')
plt.show()
print(" Chart 2 saved!")

# Top 10 Customers by Spend 
query3 = """
    SELECT c.name,
           ROUND(SUM(oi.quantity * p.price), 2) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status != 'cancelled'
    GROUP BY c.customer_id, c.name
    ORDER BY total_spent DESC
    LIMIT 10;
"""
df3 = pd.read_sql(query3, conn)

plt.figure(figsize=(12, 6))
plt.barh(df3['name'], df3['total_spent'], color='steelblue')
plt.title('Top 10 Customers by Total Spend')
plt.xlabel('Total Spent ($)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_customers.png')
plt.show()
print("Chart 3 saved!")

conn.close()
print("\n All charts saved successfully!")
