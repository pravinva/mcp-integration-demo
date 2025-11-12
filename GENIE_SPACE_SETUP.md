# Genie Space Setup Instructions

## Quick Answer

**Genie Space Name:** `ecommerce-analytics` (or any name you prefer)

**Tables to Include:**
- `demo_retail.ecommerce.customers`
- `demo_retail.ecommerce.products`
- `demo_retail.ecommerce.orders`
- `demo_retail.ecommerce.order_items`
- `demo_retail.ecommerce.revenue_by_quarter` (view)
- `demo_retail.ecommerce.customer_performance` (view)
- `demo_retail.ecommerce.product_performance` (view)

**Scripts will NOT create the Genie Space** - you must create it manually after running the SQL scripts.

---

## Step-by-Step Setup

### Step 1: Run SQL Scripts to Create Tables

The scripts create the data, but **NOT** the Genie Space. Run these in Databricks SQL Editor:

```sql
-- Run in Databricks SQL Editor or Notebook
%run ./mock-data/01_create_tables.sql
%run ./mock-data/02_create_vector_search.sql
%run ./mock-data/03_create_uc_functions.sql
```

Or copy/paste the SQL files directly into SQL Editor.

**What gets created:**
- Catalog: `demo_retail`
- Schema: `ecommerce`
- Tables: `customers`, `products`, `orders`, `order_items`, `documentation`
- Views: `revenue_by_quarter`, `customer_performance`, `product_performance`
- Functions: `calculate_discount`, `calculate_sales_tax`, etc.

### Step 2: Create Genie Space Manually

**Genie Spaces CANNOT be created programmatically** - you must use the Databricks UI.

#### Instructions:

1. **Go to Databricks Workspace**
   - Log into your workspace

2. **Navigate to Genie**
   - Click **"Genie"** in the left sidebar
   - OR go to **SQL → Genie**

3. **Create New Space**
   - Click the **"New"** button (upper-right corner)
   - OR click **"Create Space"**

4. **Configure Space Settings:**

   **Name:** `ecommerce-analytics` (or any name you like)
   
   **Catalog:** `demo_retail`
   
   **Schema:** `ecommerce`
   
   **Tables to Include:** Select these tables:
   - ✅ `demo_retail.ecommerce.customers`
   - ✅ `demo_retail.ecommerce.products`
   - ✅ `demo_retail.ecommerce.orders`
   - ✅ `demo_retail.ecommerce.order_items`
   - ✅ `demo_retail.ecommerce.revenue_by_quarter` (view)
   - ✅ `demo_retail.ecommerce.customer_performance` (view)
   - ✅ `demo_retail.ecommerce.product_performance` (view)

   **SQL Warehouse:** Select a SQL Warehouse (Pro or Serverless)
   - Make sure you have "CAN USE" permission

5. **Add Instructions (Optional but Recommended):**

   Paste this in the "Instructions" field:

   ```
   You are a retail analytics assistant for a B2B software company.

   Available Data:
   - Customers: 15 B2B customers across Enterprise, Mid-Market, and SMB segments
   - Products: Mix of software, services, training, and support
   - Orders: Q1-Q4 2024 transaction history
   - Metrics: Revenue, margins, customer lifetime value

   Common Questions:
   - "What was our Q4 2024 revenue?"
   - "Show me top 5 customers by revenue"
   - "Which products have the highest profit margins?"
   - "Compare Q3 vs Q4 performance"
   - "What is the average order value by customer segment?"

   Always show the SQL query and explain key insights.
   ```

6. **Click "Create"**

### Step 3: Find Your Genie Space ID

After creating the space, you need the Space ID for your `.env` file.

**Option 1: From URL**
- Open your Genie Space
- Look at the URL: `https://your-workspace.cloud.databricks.com/sql/genie/{space_id}`
- Copy the `space_id` part

**Option 2: Using Helper Script**
```bash
python scripts/find_genie_space.py --list
```

**Option 3: Find by Name**
```bash
python scripts/find_genie_space.py --find "ecommerce-analytics"
```

### Step 4: Add to .env File

```bash
# Edit .env file
GENIE_SPACE_ID=your-space-id-here
```

---

## Summary

| Step | Action | Automated? |
|------|--------|------------|
| 1. Create tables | Run SQL scripts | ✅ Yes (scripts) |
| 2. Create Genie Space | Use Databricks UI | ❌ No (manual) |
| 3. Get Space ID | From URL or script | ✅ Yes (script helps) |
| 4. Configure .env | Add GENIE_SPACE_ID | ❌ No (manual) |

---

## Where to Find Instructions

1. **Detailed Setup:** `mock-data/README.md` (lines 93-132)
2. **Quick Start:** `docs/setup-guide.md`
3. **Helper Script:** `scripts/find_genie_space.py --instructions`
4. **This File:** `GENIE_SPACE_SETUP.md` (you're reading it!)

---

## Test Your Setup

After creating the Genie Space and adding the Space ID to `.env`:

```bash
cd demos/01-cli
python genie_cli.py
```

Try asking:
- "What was our Q4 2024 revenue?"
- "Show me top 5 customers by revenue"
- "Compare Q3 vs Q4 performance"

If it works, you're all set! 🎉

