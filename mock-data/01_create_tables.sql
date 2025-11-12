-- ============================================================================
-- Mock Data for Databricks Genie MCP Showcase
-- Creates e-commerce dataset for analytics demonstrations
-- ============================================================================

-- Create catalog and schema
CREATE CATALOG IF NOT EXISTS demo_retail;
CREATE SCHEMA IF NOT EXISTS demo_retail.ecommerce;
USE CATALOG demo_retail;
USE SCHEMA ecommerce;

-- ============================================================================
-- Table 1: Customers
-- ============================================================================
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    customer_name STRING,
    email STRING,
    country STRING,
    segment STRING,
    signup_date DATE,
    lifetime_value DECIMAL(10,2)
) COMMENT 'Customer master data with demographics and value metrics. Use for customer segmentation and lifetime value analysis.';

INSERT INTO customers VALUES
    (1, 'Acme Corporation', 'contact@acme.com', 'USA', 'Enterprise', '2023-01-15', 450000.00),
    (2, 'TechStart Inc', 'sales@techstart.io', 'USA', 'SMB', '2023-02-20', 180000.00),
    (3, 'Global Systems Ltd', 'info@globalsys.uk', 'UK', 'Enterprise', '2023-01-10', 380000.00),
    (4, 'DataWorks GmbH', 'contact@dataworks.de', 'Germany', 'Mid-Market', '2023-02-05', 220000.00),
    (5, 'CloudFirst SAS', 'hello@cloudfirst.fr', 'France', 'SMB', '2023-03-15', 120000.00),
    (6, 'Innovation Labs', 'team@innovationlabs.com', 'Canada', 'Enterprise', '2022-11-20', 520000.00),
    (7, 'Digital Dynamics', 'info@digitaldyn.com', 'Australia', 'Mid-Market', '2023-04-01', 195000.00),
    (8, 'Smart Solutions', 'contact@smartsol.com', 'USA', 'SMB', '2023-05-10', 85000.00),
    (9, 'NextGen Tech', 'sales@nextgentech.com', 'Singapore', 'Enterprise', '2022-12-05', 410000.00),
    (10, 'Infinity Systems', 'hello@infinitysys.com', 'India', 'Mid-Market', '2023-06-20', 165000.00),
    (11, 'Quantum Analytics', 'info@quantum.com', 'USA', 'Mid-Market', '2023-07-15', 175000.00),
    (12, 'Pixel Perfect Inc', 'hello@pixelperfect.com', 'UK', 'SMB', '2023-08-01', 95000.00),
    (13, 'Data Forge Ltd', 'sales@dataforge.com', 'Germany', 'Enterprise', '2023-01-20', 390000.00),
    (14, 'Cloud Native Co', 'team@cloudnative.com', 'USA', 'Mid-Market', '2023-09-10', 145000.00),
    (15, 'AI Ventures', 'contact@aiventures.com', 'Canada', 'SMB', '2023-10-05', 78000.00);

-- Add column comments
ALTER TABLE customers ALTER COLUMN customer_id COMMENT 'Unique customer identifier';
ALTER TABLE customers ALTER COLUMN segment COMMENT 'Customer segment: Enterprise (>$300K LTV), Mid-Market ($100-300K), SMB (<$100K)';
ALTER TABLE customers ALTER COLUMN lifetime_value COMMENT 'Total revenue from customer since signup (updated monthly)';
ALTER TABLE customers ALTER COLUMN country COMMENT 'Customer primary country location';

-- ============================================================================
-- Table 2: Products
-- ============================================================================
CREATE OR REPLACE TABLE products (
    product_id INT,
    product_name STRING,
    category STRING,
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    stock_quantity INT,
    margin_percent DECIMAL(5,2)
) COMMENT 'Product catalog with pricing and inventory. Use for revenue and margin analysis.';

INSERT INTO products VALUES
    (101, 'Data Platform Pro', 'Software', 5000.00, 1200.00, 999, 76.00),
    (102, 'Analytics Suite Enterprise', 'Software', 8000.00, 2000.00, 999, 75.00),
    (103, 'ML Toolkit Advanced', 'Software', 3500.00, 800.00, 999, 77.14),
    (104, 'Professional Services - 10 Days', 'Services', 15000.00, 8000.00, 50, 46.67),
    (105, 'Training Package - 5 Days', 'Training', 2500.00, 500.00, 100, 80.00),
    (106, 'Data Integration Module', 'Software', 2000.00, 400.00, 999, 80.00),
    (107, 'Security Add-on', 'Software', 1500.00, 300.00, 999, 80.00),
    (108, 'Premium Support Annual', 'Support', 10000.00, 3000.00, 200, 70.00),
    (109, 'API Access Tier 1', 'Software', 1000.00, 200.00, 999, 80.00),
    (110, 'Cloud Storage - 1TB', 'Infrastructure', 500.00, 150.00, 999, 70.00);

ALTER TABLE products ALTER COLUMN category COMMENT 'Product category: Software, Services, Training, Support, Infrastructure';
ALTER TABLE products ALTER COLUMN margin_percent COMMENT 'Gross margin percentage calculated as (price-cost)/price*100';
ALTER TABLE products ALTER COLUMN stock_quantity COMMENT 'Available inventory (999 = unlimited for digital products)';

-- ============================================================================
-- Table 3: Orders
-- ============================================================================
CREATE OR REPLACE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status STRING,
    quarter STRING,
    year INT
) COMMENT 'Order transactions with status and period information. Use for time-series revenue analysis and trends.';

INSERT INTO orders VALUES
    -- Q1 2024
    (1001, 1, '2024-01-15', 25000.00, 'Completed', 'Q1', 2024),
    (1002, 2, '2024-01-20', 8500.00, 'Completed', 'Q1', 2024),
    (1003, 3, '2024-02-05', 23000.00, 'Completed', 'Q1', 2024),
    (1004, 4, '2024-02-12', 12000.00, 'Completed', 'Q1', 2024),
    (1005, 5, '2024-03-08', 5500.00, 'Completed', 'Q1', 2024),
    (1006, 6, '2024-03-20', 32000.00, 'Completed', 'Q1', 2024),
    -- Q2 2024
    (1007, 1, '2024-04-10', 35000.00, 'Completed', 'Q2', 2024),
    (1008, 7, '2024-04-15', 18000.00, 'Completed', 'Q2', 2024),
    (1009, 2, '2024-05-20', 15000.00, 'Completed', 'Q2', 2024),
    (1010, 8, '2024-05-25', 8500.00, 'Completed', 'Q2', 2024),
    (1011, 3, '2024-06-10', 28000.00, 'Completed', 'Q2', 2024),
    (1012, 9, '2024-06-18', 38000.00, 'Completed', 'Q2', 2024),
    -- Q3 2024
    (1013, 4, '2024-07-05', 19000.00, 'Completed', 'Q3', 2024),
    (1014, 10, '2024-07-15', 14500.00, 'Completed', 'Q3', 2024),
    (1015, 1, '2024-08-20', 45000.00, 'Completed', 'Q3', 2024),
    (1016, 11, '2024-08-25', 17500.00, 'Completed', 'Q3', 2024),
    (1017, 6, '2024-09-10', 42000.00, 'Completed', 'Q3', 2024),
    (1018, 12, '2024-09-22', 9500.00, 'Completed', 'Q3', 2024),
    -- Q4 2024
    (1019, 3, '2024-10-05', 31000.00, 'Completed', 'Q4', 2024),
    (1020, 13, '2024-10-12', 39000.00, 'Completed', 'Q4', 2024),
    (1021, 7, '2024-11-08', 21000.00, 'Completed', 'Q4', 2024),
    (1022, 9, '2024-11-15', 41000.00, 'Completed', 'Q4', 2024),
    (1023, 14, '2024-11-20', 15500.00, 'Processing', 'Q4', 2024),
    (1024, 15, '2024-11-25', 7800.00, 'Processing', 'Q4', 2024);

ALTER TABLE orders ALTER COLUMN quarter COMMENT 'Fiscal quarter: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec)';
ALTER TABLE orders ALTER COLUMN status COMMENT 'Order status: Completed, Processing, Cancelled';
ALTER TABLE orders ALTER COLUMN total_amount COMMENT 'Total order value in USD including all line items';

-- ============================================================================
-- Table 4: Order Items (detail)
-- ============================================================================
CREATE OR REPLACE TABLE order_items (
    order_item_id INT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    line_total DECIMAL(10,2)
) COMMENT 'Line items for each order. Join with products table for product performance analysis.';

INSERT INTO order_items VALUES
    -- Order 1001
    (1, 1001, 101, 5, 5000.00, 25000.00),
    -- Order 1002
    (2, 1002, 103, 2, 3500.00, 7000.00),
    (3, 1002, 106, 1, 2000.00, 2000.00),
    -- Order 1003
    (4, 1003, 102, 2, 8000.00, 16000.00),
    (5, 1003, 107, 3, 1500.00, 4500.00),
    (6, 1003, 109, 2, 1000.00, 2000.00),
    -- Order 1004
    (7, 1004, 104, 1, 15000.00, 15000.00),
    -- Order 1005
    (8, 1005, 105, 2, 2500.00, 5000.00),
    (9, 1005, 109, 1, 1000.00, 1000.00),
    -- Order 1006
    (10, 1006, 102, 4, 8000.00, 32000.00),
    -- Order 1007
    (11, 1007, 101, 7, 5000.00, 35000.00),
    -- Order 1008
    (12, 1008, 104, 1, 15000.00, 15000.00),
    (13, 1008, 105, 1, 2500.00, 2500.00),
    -- Order 1009
    (14, 1009, 102, 1, 8000.00, 8000.00),
    (15, 1009, 103, 2, 3500.00, 7000.00),
    -- Order 1010
    (16, 1010, 101, 1, 5000.00, 5000.00),
    (17, 1010, 106, 1, 2000.00, 2000.00),
    (18, 1010, 107, 1, 1500.00, 1500.00),
    -- Order 1011
    (19, 1011, 102, 3, 8000.00, 24000.00),
    (20, 1011, 108, 1, 10000.00, 10000.00),
    -- Continue pattern for remaining orders...
    (21, 1012, 101, 5, 5000.00, 25000.00),
    (22, 1012, 102, 1, 8000.00, 8000.00),
    (23, 1012, 108, 1, 10000.00, 10000.00),
    (24, 1013, 104, 1, 15000.00, 15000.00),
    (25, 1013, 106, 2, 2000.00, 4000.00),
    (26, 1014, 101, 2, 5000.00, 10000.00),
    (27, 1014, 105, 1, 2500.00, 2500.00),
    (28, 1014, 109, 2, 1000.00, 2000.00),
    (29, 1015, 102, 5, 8000.00, 40000.00),
    (30, 1015, 108, 1, 10000.00, 10000.00),
    (31, 1016, 101, 3, 5000.00, 15000.00),
    (32, 1016, 109, 2, 1000.00, 2000.00),
    (33, 1017, 102, 5, 8000.00, 40000.00),
    (34, 1017, 109, 2, 1000.00, 2000.00),
    (35, 1018, 103, 2, 3500.00, 7000.00),
    (36, 1018, 106, 1, 2000.00, 2000.00),
    (37, 1019, 102, 3, 8000.00, 24000.00),
    (38, 1019, 107, 4, 1500.00, 6000.00),
    (39, 1019, 109, 1, 1000.00, 1000.00),
    (40, 1020, 101, 6, 5000.00, 30000.00),
    (41, 1020, 108, 1, 10000.00, 10000.00),
    (42, 1021, 104, 1, 15000.00, 15000.00),
    (43, 1021, 106, 3, 2000.00, 6000.00),
    (44, 1022, 102, 4, 8000.00, 32000.00),
    (45, 1022, 108, 1, 10000.00, 10000.00),
    (46, 1023, 101, 3, 5000.00, 15000.00),
    (47, 1024, 105, 3, 2500.00, 7500.00),
    (48, 1024, 109, 1, 1000.00, 1000.00);

ALTER TABLE order_items ALTER COLUMN line_total COMMENT 'Calculated as quantity * unit_price';

-- ============================================================================
-- Create useful views for Genie
-- ============================================================================

CREATE OR REPLACE VIEW revenue_by_quarter AS
SELECT 
    year,
    quarter,
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE status = 'Completed'
GROUP BY year, quarter
ORDER BY year, quarter;

CREATE OR REPLACE VIEW customer_performance AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed' OR o.status IS NULL
GROUP BY c.customer_id, c.customer_name, c.segment, c.country
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.margin_percent,
    COUNT(oi.order_item_id) as times_sold,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.line_total) as total_revenue,
    SUM(oi.quantity * p.cost) as total_cost,
    SUM(oi.line_total) - SUM(oi.quantity * p.cost) as total_profit
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category, p.price, p.margin_percent
ORDER BY total_revenue DESC;

-- ============================================================================
-- Grant permissions (adjust as needed)
-- ============================================================================
-- GRANT SELECT ON TABLE customers TO `your-user-group`;
-- GRANT SELECT ON TABLE products TO `your-user-group`;
-- GRANT SELECT ON TABLE orders TO `your-user-group`;
-- GRANT SELECT ON TABLE order_items TO `your-user-group`;

-- ============================================================================
-- Validation queries
-- ============================================================================
SELECT 'Total customers: ' || COUNT(*) FROM customers;
SELECT 'Total products: ' || COUNT(*) FROM products;
SELECT 'Total orders: ' || COUNT(*) FROM orders;
SELECT 'Total order items: ' || COUNT(*) FROM order_items;
SELECT 'Total revenue (completed): $' || CAST(SUM(total_amount) AS STRING) FROM orders WHERE status = 'Completed';

-- Success message
SELECT '✅ Mock data created successfully!' as status,
       'Catalog: demo_retail | Schema: ecommerce' as location,
       '4 tables + 3 views created' as summary;

