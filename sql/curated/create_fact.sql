-- 7
USE DATABASE LAPTOP_DWH;
USE SCHEMA CURATED;

-- =========================================
-- FACT TABLE
-- =========================================

CREATE OR REPLACE TABLE CURATED.FACT_LAPTOP_LISTING (
    listing_key INTEGER AUTOINCREMENT PRIMARY KEY,
    product_key INTEGER,
    brand_key INTEGER,
    cpu_key INTEGER,
    gpu_key INTEGER,
    display_key INTEGER,
    memory_key INTEGER,
    storage_key INTEGER,
    os_key INTEGER,
    flags_key INTEGER,
    current_price NUMBER(6,2),
    old_price NUMBER(6,2),
    discount_percent NUMBER(3,1),
    shipping_cost NUMBER(4,2),
    rating NUMBER(2,1),
    rating_num NUMBER(3,0),
    FOREIGN KEY (product_key) REFERENCES CURATED.DIM_PRODUCT(product_key),
    FOREIGN KEY (brand_key) REFERENCES CURATED.DIM_BRAND(brand_key),
    FOREIGN KEY (cpu_key) REFERENCES CURATED.DIM_CPU(cpu_key),
    FOREIGN KEY (gpu_key) REFERENCES CURATED.DIM_GPU(gpu_key),
    FOREIGN KEY (display_key) REFERENCES CURATED.DIM_DISPLAY(display_key),
    FOREIGN KEY (memory_key) REFERENCES CURATED.DIM_MEMORY(memory_key),
    FOREIGN KEY (storage_key) REFERENCES CURATED.DIM_STORAGE(storage_key),
    FOREIGN KEY (os_key) REFERENCES CURATED.DIM_OS(os_key),
    FOREIGN KEY (flags_key) REFERENCES CURATED.DIM_FLAGS(flags_key)
);