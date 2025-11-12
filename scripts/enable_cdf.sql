-- Enable Change Data Feed on documentation table for Vector Search
USE CATALOG demo_retail;
USE SCHEMA ecommerce;

ALTER TABLE documentation SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

SELECT '✅ Change Data Feed enabled on documentation table' as status;
