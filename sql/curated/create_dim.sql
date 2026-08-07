-- 6
USE DATABASE LAPTOP_DWH;
USE SCHEMA CURATED;

-- =========================================
-- DIMENSION TABLES
-- =========================================

CREATE OR REPLACE TABLE CURATED.DIM_PRODUCT (
    product_key INTEGER AUTOINCREMENT PRIMARY KEY,
    title TEXT,
    series TEXT,
    link TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_BRAND (
    brand_key INTEGER AUTOINCREMENT PRIMARY KEY,
    brand_name TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_CPU (
    cpu_key INTEGER AUTOINCREMENT PRIMARY KEY,
    cpu_brand TEXT,
    cpu_series TEXT,
    cpu_model TEXT,
    cpu_cores NUMBER(5,1)
);

CREATE OR REPLACE TABLE CURATED.DIM_GPU (
    gpu_key INTEGER AUTOINCREMENT PRIMARY KEY,
    gpu_brand TEXT,
    gpu_type TEXT,
    gpu_model TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_DISPLAY (
    display_key INTEGER AUTOINCREMENT PRIMARY KEY,
    screen_size_inches NUMBER(3,1),
    resolution TEXT,
    resolution_category TEXT,
    is_touchscreen NUMBER(1,0)
);

CREATE OR REPLACE TABLE CURATED.DIM_MEMORY (
    memory_key INTEGER AUTOINCREMENT PRIMARY KEY,
    ram_capacity_gb NUMBER(2,0),
    ram_type TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_STORAGE (
    storage_key INTEGER AUTOINCREMENT PRIMARY KEY,
    storage_capacity_gb NUMBER(4,0),
    storage_type TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_OS (
    os_key INTEGER AUTOINCREMENT PRIMARY KEY,
    operating_system TEXT
);

CREATE OR REPLACE TABLE CURATED.DIM_FLAGS (
    flags_key INTEGER AUTOINCREMENT PRIMARY KEY,
    is_refurbished NUMBER(1,0),
    is_free_shipping NUMBER(1,0),
    is_ai_pc NUMBER(1,0),
    has_backlit_keyboard NUMBER(1,0)
);

