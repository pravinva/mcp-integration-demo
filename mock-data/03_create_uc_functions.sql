-- ============================================================================
-- Unity Catalog Functions for MCP Demo
-- Creates callable functions for business logic demonstrations
-- ============================================================================

USE CATALOG demo_retail;
USE SCHEMA ecommerce;

-- ============================================================================
-- Function 1: Calculate Customer Discount
-- ============================================================================
CREATE OR REPLACE FUNCTION calculate_discount(
    order_amount DOUBLE,
    customer_segment STRING
)
RETURNS STRUCT<
    discount_amount DOUBLE,
    discount_percentage INT,
    final_amount DOUBLE,
    segment STRING
>
LANGUAGE SQL
COMMENT 'Calculate discount based on customer segment and order amount. 
Enterprise customers get 15-20% based on order size, 
Mid-Market get 10-12%, SMB get 5-7%. 
Returns detailed breakdown of discount calculation.'
RETURN 
    CASE 
        WHEN customer_segment = 'Enterprise' AND order_amount >= 50000 THEN
            STRUCT(
                order_amount * 0.20 AS discount_amount,
                20 AS discount_percentage,
                order_amount * 0.80 AS final_amount,
                'Enterprise - Premium Tier' AS segment
            )
        WHEN customer_segment = 'Enterprise' AND order_amount >= 25000 THEN
            STRUCT(
                order_amount * 0.17 AS discount_amount,
                17 AS discount_percentage,
                order_amount * 0.83 AS final_amount,
                'Enterprise - Standard Tier' AS segment
            )
        WHEN customer_segment = 'Enterprise' THEN
            STRUCT(
                order_amount * 0.15 AS discount_amount,
                15 AS discount_percentage,
                order_amount * 0.85 AS final_amount,
                'Enterprise - Basic Tier' AS segment
            )
        WHEN customer_segment = 'Mid-Market' AND order_amount >= 20000 THEN
            STRUCT(
                order_amount * 0.12 AS discount_amount,
                12 AS discount_percentage,
                order_amount * 0.88 AS final_amount,
                'Mid-Market - High Value' AS segment
            )
        WHEN customer_segment = 'Mid-Market' THEN
            STRUCT(
                order_amount * 0.10 AS discount_amount,
                10 AS discount_percentage,
                order_amount * 0.90 AS final_amount,
                'Mid-Market - Standard' AS segment
            )
        WHEN customer_segment = 'SMB' AND order_amount >= 10000 THEN
            STRUCT(
                order_amount * 0.07 AS discount_amount,
                7 AS discount_percentage,
                order_amount * 0.93 AS final_amount,
                'SMB - Volume Buyer' AS segment
            )
        ELSE
            STRUCT(
                order_amount * 0.05 AS discount_amount,
                5 AS discount_percentage,
                order_amount * 0.95 AS final_amount,
                'SMB - Standard' AS segment
            )
    END;

-- ============================================================================
-- Function 2: Calculate Sales Tax
-- ============================================================================
CREATE OR REPLACE FUNCTION calculate_sales_tax(
    amount DOUBLE,
    country STRING
)
RETURNS STRUCT<
    tax_amount DOUBLE,
    tax_rate DOUBLE,
    total_with_tax DOUBLE
>
LANGUAGE SQL
COMMENT 'Calculate sales tax based on country tax rates.
USA: 8.5%, Canada: 13%, UK: 20%, Germany: 19%, France: 20%, Others: 10%'
RETURN
    CASE
        WHEN country = 'USA' THEN 
            STRUCT(amount * 0.085 AS tax_amount, 0.085 AS tax_rate, amount * 1.085 AS total_with_tax)
        WHEN country = 'Canada' THEN
            STRUCT(amount * 0.13 AS tax_amount, 0.13 AS tax_rate, amount * 1.13 AS total_with_tax)
        WHEN country = 'UK' THEN
            STRUCT(amount * 0.20 AS tax_amount, 0.20 AS tax_rate, amount * 1.20 AS total_with_tax)
        WHEN country = 'Germany' THEN
            STRUCT(amount * 0.19 AS tax_amount, 0.19 AS tax_rate, amount * 1.19 AS total_with_tax)
        WHEN country = 'France' THEN
            STRUCT(amount * 0.20 AS tax_amount, 0.20 AS tax_rate, amount * 1.20 AS total_with_tax)
        ELSE
            STRUCT(amount * 0.10 AS tax_amount, 0.10 AS tax_rate, amount * 1.10 AS total_with_tax)
    END;

-- ============================================================================
-- Function 3: Check Credit Limit
-- ============================================================================
CREATE OR REPLACE FUNCTION check_credit_limit(
    customer_segment STRING,
    current_balance DOUBLE,
    new_order_amount DOUBLE
)
RETURNS STRUCT<
    approved BOOLEAN,
    credit_limit DOUBLE,
    available_credit DOUBLE,
    message STRING
>
LANGUAGE SQL
COMMENT 'Check if order can be approved based on customer segment credit limits.
Enterprise: $500K, Mid-Market: $200K, SMB: $50K'
RETURN
    CASE
        WHEN customer_segment = 'Enterprise' THEN
            STRUCT(
                (current_balance + new_order_amount) <= 500000 AS approved,
                500000.0 AS credit_limit,
                500000.0 - current_balance AS available_credit,
                CASE 
                    WHEN (current_balance + new_order_amount) <= 500000 
                    THEN 'Order approved - within Enterprise credit limit'
                    ELSE 'Order exceeds Enterprise credit limit of $500,000'
                END AS message
            )
        WHEN customer_segment = 'Mid-Market' THEN
            STRUCT(
                (current_balance + new_order_amount) <= 200000 AS approved,
                200000.0 AS credit_limit,
                200000.0 - current_balance AS available_credit,
                CASE 
                    WHEN (current_balance + new_order_amount) <= 200000 
                    THEN 'Order approved - within Mid-Market credit limit'
                    ELSE 'Order exceeds Mid-Market credit limit of $200,000'
                END AS message
            )
        ELSE
            STRUCT(
                (current_balance + new_order_amount) <= 50000 AS approved,
                50000.0 AS credit_limit,
                50000.0 - current_balance AS available_credit,
                CASE 
                    WHEN (current_balance + new_order_amount) <= 50000 
                    THEN 'Order approved - within SMB credit limit'
                    ELSE 'Order exceeds SMB credit limit of $50,000'
                END AS message
            )
    END;

-- ============================================================================
-- Function 4: Calculate Loyalty Points
-- ============================================================================
CREATE OR REPLACE FUNCTION calculate_loyalty_points(
    order_amount DOUBLE,
    customer_segment STRING,
    is_repeat_customer BOOLEAN
)
RETURNS STRUCT<
    points_earned INT,
    points_multiplier DOUBLE,
    tier STRING
>
LANGUAGE SQL
COMMENT 'Calculate loyalty points earned. Base: 1 point per $10. 
Enterprise 3x, Mid-Market 2x, SMB 1.5x. Repeat customers get +0.5x bonus.'
RETURN
    CASE
        WHEN customer_segment = 'Enterprise' THEN
            STRUCT(
                CAST((order_amount / 10) * (3.0 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS INT) AS points_earned,
                (3.0 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS points_multiplier,
                'Platinum' AS tier
            )
        WHEN customer_segment = 'Mid-Market' THEN
            STRUCT(
                CAST((order_amount / 10) * (2.0 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS INT) AS points_earned,
                (2.0 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS points_multiplier,
                'Gold' AS tier
            )
        ELSE
            STRUCT(
                CAST((order_amount / 10) * (1.5 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS INT) AS points_earned,
                (1.5 + CASE WHEN is_repeat_customer THEN 0.5 ELSE 0 END) AS points_multiplier,
                'Silver' AS tier
            )
    END;

-- ============================================================================
-- Function 5: Recommend Next Best Product
-- ============================================================================
CREATE OR REPLACE FUNCTION recommend_product(
    customer_segment STRING,
    previous_purchases ARRAY<STRING>
)
RETURNS STRING
LANGUAGE SQL
COMMENT 'Simple product recommendation based on segment and purchase history.
Returns product name recommendation.'
RETURN
    CASE
        -- Enterprise customers who bought Data Platform
        WHEN customer_segment = 'Enterprise' AND array_contains(previous_purchases, 'Data Platform Pro') THEN
            'Analytics Suite Enterprise - Perfect complement for advanced analytics'
        -- Enterprise without Data Platform
        WHEN customer_segment = 'Enterprise' THEN
            'Data Platform Pro - Our flagship product for enterprise scale'
        -- Mid-Market with any software
        WHEN customer_segment = 'Mid-Market' AND (
            array_contains(previous_purchases, 'Data Platform Pro') OR 
            array_contains(previous_purchases, 'Analytics Suite Enterprise')
        ) THEN
            'Professional Services - 10 Days - Maximize your investment'
        -- Mid-Market without software
        WHEN customer_segment = 'Mid-Market' THEN
            'ML Toolkit Advanced - Great starting point for data science'
        -- SMB customers
        WHEN customer_segment = 'SMB' AND size(previous_purchases) > 0 THEN
            'Training Package - 5 Days - Upskill your team'
        ELSE
            'Data Integration Module - Essential for getting started'
    END;

-- ============================================================================
-- Test the functions
-- ============================================================================

-- Test discount calculation
SELECT 
    'Discount Test' as test_name,
    calculate_discount(50000.0, 'Enterprise') as enterprise_50k,
    calculate_discount(25000.0, 'Mid-Market') as midmarket_25k,
    calculate_discount(10000.0, 'SMB') as smb_10k;

-- Test sales tax
SELECT
    'Sales Tax Test' as test_name,
    calculate_sales_tax(10000.0, 'USA') as usa_tax,
    calculate_sales_tax(10000.0, 'UK') as uk_tax,
    calculate_sales_tax(10000.0, 'Germany') as germany_tax;

-- Test credit limit
SELECT
    'Credit Check Test' as test_name,
    check_credit_limit('Enterprise', 400000.0, 50000.0) as within_limit,
    check_credit_limit('SMB', 45000.0, 10000.0) as exceeds_limit;

-- Test loyalty points
SELECT
    'Loyalty Points Test' as test_name,
    calculate_loyalty_points(10000.0, 'Enterprise', true) as enterprise_repeat,
    calculate_loyalty_points(10000.0, 'Mid-Market', false) as midmarket_new;

-- Test recommendations
SELECT
    'Recommendation Test' as test_name,
    recommend_product('Enterprise', ARRAY('Data Platform Pro')) as enterprise_rec,
    recommend_product('SMB', ARRAY()) as smb_rec;

-- ============================================================================
-- Grant execute permissions (adjust as needed)
-- ============================================================================
-- GRANT EXECUTE ON FUNCTION calculate_discount TO `your-user-group`;
-- GRANT EXECUTE ON FUNCTION calculate_sales_tax TO `your-user-group`;
-- GRANT EXECUTE ON FUNCTION check_credit_limit TO `your-user-group`;
-- GRANT EXECUTE ON FUNCTION calculate_loyalty_points TO `your-user-group`;
-- GRANT EXECUTE ON FUNCTION recommend_product TO `your-user-group`;

SELECT '✅ Unity Catalog Functions created!' as status,
       'Catalog: demo_retail | Schema: ecommerce' as location,
       '5 functions: calculate_discount, calculate_sales_tax, check_credit_limit, calculate_loyalty_points, recommend_product' as summary;

