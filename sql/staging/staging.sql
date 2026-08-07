-- 4
USE DATABASE LAPTOP_DWH;
USE SCHEMA STAGING;

CREATE TABLE IF NOT EXISTS STAGING.STG_LAPTOPS (
-- CREATE OR REPLACE TABLE STAGING.STG_LAPTOPS (
    title TEXT,
    brand TEXT,
    series TEXT,
    is_refurbished NUMBER(1, 0),
    current_price NUMBER(6, 2),
    old_price NUMBER(6, 2),
    discount_percent NUMBER(3, 1),
    shipping_cost NUMBER(4, 2),
    is_free_shipping NUMBER(1, 0),
    rating NUMBER(2, 1),
    rating_num NUMBER(3, 0),
    operating_system TEXT,
    screen_size_inches NUMBER(3, 1),
    resolution TEXT,
    resolution_category TEXT,
    is_touchscreen NUMBER(1, 0),
    ram_capacity_gb NUMBER(2, 0),
    ram_type TEXT,
    storage_capacity_gb NUMBER(4, 0),
    storage_type TEXT,
    cpu_brand TEXT,
    cpu_series TEXT,
    cpu_model TEXT,
    cpu_cores NUMBER(5, 1),
    gpu_brand TEXT,
    gpu_type TEXT,
    gpu_model TEXT,
    is_ai_pc NUMBER(1, 0),
    has_backlit_keyboard NUMBER(1, 0),
    link TEXT
);