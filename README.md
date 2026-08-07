# Laptop Pricing Intelligence Pipeline

## Overview

The Laptop Pricing Intelligence Pipeline is an end-to-end data engineering project that collects, processes, stores, and analyzes laptop pricing data from online retailers.

The goal is to simulate a real-world pricing analytics platform, transforming raw product data into structured warehouse models and actionable business insights.

The pipeline scrapes laptop product information, performs data cleaning and feature engineering, loads the data into a cloud data warehouse, and (upcoming) powers analytical dashboards to surface pricing trends, product segments, and market behavior.

---

## Business Objective

The project aims to answer questions such as:

- How do laptop prices vary across brands?
- Which specifications have the biggest impact on price?
- How do RAM, storage, CPU, and GPU affect pricing?
- Which brands offer the best value for money?
- How do laptop prices change over time?
- Which products see the largest discounts?

---

## Data Source

**Newegg laptop listings**

Selected for:

- Rich laptop product information
- Wide category variety
- Consistent product page structure
- Availability of both pricing and technical specifications

---

## Planned Data Fields

### Product Information
- Product name
- Brand
- Product URL
- Availability

### Pricing Information
- Current price
- Original price (if available)
- Discount percentage
- Scrape date

### Specifications
- Processor (CPU)
- RAM
- Storage
- Display size
- Graphics card (GPU)

### Customer Information
- Rating
- Review count

---

## Technology Stack

### Data Collection
- Python
- Requests
- BeautifulSoup

### Data Processing
- Python
- Pandas

### Data Warehouse
- Snowflake
- SQL

### Visualization
- Power BI

### Version Control
- Git
- GitHub

---

## Status

✅ **Completed:**
- Data collection (scraping)
- Data cleaning and feature engineering
- Loading into Snowflake data warehouse

🚧 **In progress:**
- Analytical dashboards and visualization in Power BI