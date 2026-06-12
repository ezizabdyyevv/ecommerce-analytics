USE ecommerce_analytics;

-- ── Query 1: Total Customers ──────────────────────────
SELECT COUNT(*) AS total_customers
FROM customers;

-- ── Query 2: Orders by Status ─────────────────────────
SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status;

-- ── Query 3: Top 10 Best-Selling Products ─────────────
SELECT p.name, p.category, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_sold DESC
LIMIT 10;

-- ── Query 4: Revenue by Category ──────────────────────
SELECT p.category, ROUND(SUM(oi.quantity * p.price), 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'cancelled'
GROUP BY p.category
ORDER BY revenue DESC;

-- ── Query 5: Monthly Revenue Trend ────────────────────
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    ROUND(SUM(oi.quantity * p.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status != 'cancelled'
GROUP BY month
ORDER BY month;

-- ── Query 6: Customers Who Never Ordered ──────────────
SELECT c.customer_id, c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- ── Query 7: Average Order Value per Customer (Top 10) ─
SELECT 
    c.name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.quantity * p.price), 2) AS total_spent,
    ROUND(SUM(oi.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id, c.name
ORDER BY avg_order_value DESC
LIMIT 10;