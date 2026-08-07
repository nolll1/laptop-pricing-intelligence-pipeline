-- 9
USE DATABASE LAPTOP_DWH;
USE SCHEMA CURATED;

-- =========================================
-- 2. POPULATE FACT TABLE
--    Join staging back to each dim on its
--    natural attributes to resolve surrogate keys
-- =========================================

INSERT INTO CURATED.FACT_LAPTOP_LISTING (
    product_key, brand_key, cpu_key, gpu_key, display_key,
    memory_key, storage_key, os_key, flags_key,
    current_price, old_price, discount_percent, shipping_cost, rating, rating_num
)
SELECT
    dp.product_key,
    db.brand_key,
    dc.cpu_key,
    dg.gpu_key,
    dd.display_key,
    dm.memory_key,
    ds.storage_key,
    do_.os_key,
    df.flags_key,
    s.current_price,
    s.old_price,
    s.discount_percent,
    s.shipping_cost,
    s.rating,
    s.rating_num
FROM STAGING.STG_LAPTOPS s
LEFT JOIN CURATED.DIM_PRODUCT dp
    ON s.title = dp.title
    AND (s.series = dp.series OR (s.series IS NULL AND dp.series IS NULL))
    AND (s.link = dp.link OR (s.link IS NULL AND dp.link IS NULL))
LEFT JOIN CURATED.DIM_BRAND db
    ON s.brand = db.brand_name
LEFT JOIN CURATED.DIM_CPU dc
    ON (s.cpu_brand = dc.cpu_brand OR (s.cpu_brand IS NULL AND dc.cpu_brand IS NULL))
    AND (s.cpu_series = dc.cpu_series OR (s.cpu_series IS NULL AND dc.cpu_series IS NULL))
    AND (s.cpu_model = dc.cpu_model OR (s.cpu_model IS NULL AND dc.cpu_model IS NULL))
    AND (s.cpu_cores = dc.cpu_cores OR (s.cpu_cores IS NULL AND dc.cpu_cores IS NULL))
LEFT JOIN CURATED.DIM_GPU dg
    ON (s.gpu_brand = dg.gpu_brand OR (s.gpu_brand IS NULL AND dg.gpu_brand IS NULL))
    AND (s.gpu_type = dg.gpu_type OR (s.gpu_type IS NULL AND dg.gpu_type IS NULL))
    AND (s.gpu_model = dg.gpu_model OR (s.gpu_model IS NULL AND dg.gpu_model IS NULL))
LEFT JOIN CURATED.DIM_DISPLAY dd
    ON (s.screen_size_inches = dd.screen_size_inches OR (s.screen_size_inches IS NULL AND dd.screen_size_inches IS NULL))
    AND (s.resolution = dd.resolution OR (s.resolution IS NULL AND dd.resolution IS NULL))
    AND (s.resolution_category = dd.resolution_category OR (s.resolution_category IS NULL AND dd.resolution_category IS NULL))
    AND (s.is_touchscreen = dd.is_touchscreen OR (s.is_touchscreen IS NULL AND dd.is_touchscreen IS NULL))
LEFT JOIN CURATED.DIM_MEMORY dm
    ON (s.ram_capacity_gb = dm.ram_capacity_gb OR (s.ram_capacity_gb IS NULL AND dm.ram_capacity_gb IS NULL))
    AND (s.ram_type = dm.ram_type OR (s.ram_type IS NULL AND dm.ram_type IS NULL))
LEFT JOIN CURATED.DIM_STORAGE ds
    ON (s.storage_capacity_gb = ds.storage_capacity_gb OR (s.storage_capacity_gb IS NULL AND ds.storage_capacity_gb IS NULL))
    AND (s.storage_type = ds.storage_type OR (s.storage_type IS NULL AND ds.storage_type IS NULL))
LEFT JOIN CURATED.DIM_OS do_
    ON (s.operating_system = do_.operating_system OR (s.operating_system IS NULL AND do_.operating_system IS NULL))
LEFT JOIN CURATED.DIM_FLAGS df
    ON (s.is_refurbished = df.is_refurbished OR (s.is_refurbished IS NULL AND df.is_refurbished IS NULL))
    AND (s.is_free_shipping = df.is_free_shipping OR (s.is_free_shipping IS NULL AND df.is_free_shipping IS NULL))
    AND (s.is_ai_pc = df.is_ai_pc OR (s.is_ai_pc IS NULL AND df.is_ai_pc IS NULL))
    AND (s.has_backlit_keyboard = df.has_backlit_keyboard OR (s.has_backlit_keyboard IS NULL AND df.has_backlit_keyboard IS NULL));