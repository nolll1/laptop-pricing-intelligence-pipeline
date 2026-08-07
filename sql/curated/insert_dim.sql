-- 8
USE DATABASE LAPTOP_DWH;
USE SCHEMA CURATED;

-- =========================================
-- 1. POPULATE DIMENSION TABLES
-- =========================================

-- DIM_BRAND
INSERT INTO CURATED.DIM_BRAND (brand_name)
SELECT DISTINCT brand
FROM STAGING.STG_LAPTOPS
WHERE brand IS NOT NULL;

SELECT * FROM DIM_BRAND;

-- DIM_PRODUCT
INSERT INTO CURATED.DIM_PRODUCT (title, series, link)
SELECT DISTINCT title, series, link
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_PRODUCT;

-- DIM_CPU
INSERT INTO CURATED.DIM_CPU (cpu_brand, cpu_series, cpu_model, cpu_cores)
SELECT DISTINCT cpu_brand, cpu_series, cpu_model, cpu_cores
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_CPU;

-- DIM_GPU
INSERT INTO CURATED.DIM_GPU (gpu_brand, gpu_type, gpu_model)
SELECT DISTINCT gpu_brand, gpu_type, gpu_model
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_GPU;

-- DIM_DISPLAY
INSERT INTO CURATED.DIM_DISPLAY (screen_size_inches, resolution, resolution_category, is_touchscreen)
SELECT DISTINCT screen_size_inches, resolution, resolution_category, is_touchscreen
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_DISPLAY;

-- DIM_MEMORY
INSERT INTO CURATED.DIM_MEMORY (ram_capacity_gb, ram_type)
SELECT DISTINCT ram_capacity_gb, ram_type
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_MEMORY;

-- DIM_STORAGE
INSERT INTO CURATED.DIM_STORAGE (storage_capacity_gb, storage_type)
SELECT DISTINCT storage_capacity_gb, storage_type
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_STORAGE;

-- DIM_OS
INSERT INTO CURATED.DIM_OS (operating_system)
SELECT DISTINCT operating_system
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_OS;

-- DIM_FLAGS
INSERT INTO CURATED.DIM_FLAGS (is_refurbished, is_free_shipping, is_ai_pc, has_backlit_keyboard)
SELECT DISTINCT is_refurbished, is_free_shipping, is_ai_pc, has_backlit_keyboard
FROM STAGING.STG_LAPTOPS;

SELECT * FROM DIM_FLAGS;

SELECT COUNT(*) AS unmatched_cpu
FROM CURATED.FACT_LAPTOP_LISTING
WHERE cpu_key IS NULL;