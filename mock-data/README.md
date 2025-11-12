# Mock Data Setup Guide

This directory contains SQL scripts to create mock data for Databricks Genie MCP demonstrations.

## What's Included

1. **01_create_tables.sql** - E-commerce dataset (customers, products, orders)
2. **02_create_vector_search.sql** - Documentation corpus for Vector Search
3. **03_create_uc_functions.sql** - Unity Catalog Functions for calculations

## Quick Setup

### Option 1: Run All Scripts at Once

From Databricks SQL Editor or notebook
%run ./mock-data/01_create_tables.sql
%run ./mock-data/02_create_vector_search.sql
%run ./mock-data/03_create_uc_functions.sql


### Option 2: Run Individually

1. **Create Tables** (Required)

-- Run in Databricks SQL Editor
-- File: 01_create_tables.sql
-- Creates: demo_retail.ecommerce catalog with 4 tables + 3 views


2. **Create Vector Search Data** (Optional)

-- File: 02_create_vector_search.sql
-- Creates: documentation table with 12 articles


3. **Create UC Functions** (Optional)


-- File: 03_create_uc_functions.sql
-- Creates: 5 callable functions


## What You Get

### Tables

| Table | Rows | Purpose |
|-------|------|---------|
| `customers` | 15 | Customer master data |
| `products` | 10 | Product catalog |
| `orders` | 24 | Order transactions (Q1-Q4 2024) |
| `order_items` | 48 | Line item details |
| `documentation` | 12 | Searchable docs for Vector Search |

### Views

| View | Purpose |
|------|---------|
| `revenue_by_quarter` | Quarterly revenue summary |
| `customer_performance` | Customer lifetime value analysis |
| `product_performance` | Product sales and profitability |

### Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `calculate_discount` | Customer discounts | `SELECT calculate_discount(50000, 'Enterprise')` |
| `calculate_sales_tax` | Tax by country | `SELECT calculate_sales_tax(10000, 'USA')` |
| `check_credit_limit` | Credit approval | `SELECT check_credit_limit('SMB', 40000, 15000)` |
| `calculate_loyalty_points` | Rewards program | `SELECT calculate_loyalty_points(10000, 'Enterprise', true)` |
| `recommend_product` | Next best product | `SELECT recommend_product('Mid-Market', ARRAY('Data Platform Pro'))` |

## Data Summary

**Revenue by Quarter:**
- Q1 2024: $106,000
- Q2 2024: $142,500
- Q3 2024: $187,500
- Q4 2024: $155,300
- **Total: $591,300**

**Customer Segments:**
- Enterprise: 5 customers ($2.2M lifetime value)
- Mid-Market: 5 customers ($0.9M lifetime value)
- SMB: 5 customers ($0.6M lifetime value)

**Product Mix:**
- Software: 7 products (high margin ~75-80%)
- Services: 1 product (medium margin ~47%)
- Training: 1 product (high margin ~80%)
- Support: 1 product (medium margin ~70%)

## Genie Space Configuration

After running the scripts, create a Genie Space with these settings:

**Tables to Include:**
- ✅ demo_retail.ecommerce.customers
- ✅ demo_retail.ecommerce.products
- ✅ demo_retail.ecommerce.orders
- ✅ demo_retail.ecommerce.order_items
- ✅ demo_retail.ecommerce.revenue_by_quarter
- ✅ demo_retail.ecommerce.customer_performance
- ✅ demo_retail.ecommerce.product_performance

**Genie Space Instructions:**

You are a retail analytics assistant for a B2B software company.

Available Data:

Customers: 15 B2B customers across Enterprise, Mid-Market, and SMB segments

Products: Mix of software, services, training, and support

Orders: Q1-Q4 2024 transaction history

Metrics: Revenue, margins, customer lifetime value

Common Questions:

"What was our Q4 2024 revenue?"

"Show me top 5 customers by revenue"

"Which products have the highest profit margins?"

"Compare Q3 vs Q4 performance"

"What is the average order value by customer segment?"

Always show the SQL query and explain key insights.



## Sample Queries to Test


-- Test Genie with these questions:

-- Revenue analysis
"What was our total revenue in Q4 2024?"
"Show me revenue by quarter for 2024"
"Compare Q3 vs Q4 2024 revenue growth"

-- Customer analysis
"Who are our top 5 customers by revenue?"
"Show me customer lifetime value by segment"
"Which customers haven't ordered recently?"

-- Product analysis
"What are our best-selling products?"
"Show me profit margin by product category"
"Which products generate the most profit?"

-- Segment analysis
"Compare revenue across customer segments"
"What is the average order value by segment?"
"Show me order frequency by customer segment"



## Cleanup

To remove all mock data:

DROP SCHEMA IF EXISTS demo_retail.ecommerce CASCADE;
DROP CATALOG IF EXISTS demo_retail CASCADE;



## Next Steps

1. ✅ Run these SQL scripts in your Databricks workspace
2. ✅ Create a Genie Space pointing to these tables
3. ✅ Test queries in Genie UI to verify setup
4. ✅ Update your `.env` file with the Genie Space ID
5. ✅ Run the CLI demo: `python demos/01-cli/genie_cli.py`

## Support

If you encounter issues:
- Check that Unity Catalog is enabled
- Verify you have CREATE permissions on catalogs/schemas
- Ensure SQL Warehouse is running
- Review Databricks SQL error messages for permission issues

