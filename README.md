# Laptop Pricing Intelligence Pipeline

## Overview

The Laptop Pricing Intelligence Pipeline is an end-to-end data engineering project designed to collect, process, store, and analyze laptop pricing data from online retailers.

The goal of this project is to simulate a real-world pricing analytics platform where raw product data is transformed into structured warehouse models and business insights.

The pipeline will scrape laptop product information, perform data cleaning and feature engineering, load the data into a data warehouse, and create analytical dashboards to understand pricing trends, product segments, and market behavior.

---

## Business Objective

The objective is to answer business questions such as:

- How do laptop prices vary across different brands?
- Which specifications have the biggest impact on pricing?
- How does RAM, storage, CPU, and GPU affect laptop prices?
- Which brands provide the best value for money?
- How do laptop prices change over time?
- Which products experience the largest discounts?


## Data Source

The initial data source for this project will be:

- Newegg laptop listings

The website was selected based on:

- Availability of laptop product information
- Product category variety
- Consistent product structure
- Presence of pricing and technical specifications

---

## Planned Data Fields

The pipeline will collect information such as:

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

## Planned Technology Stack

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

🚧 The project is currently in the development phase, with data collection, cleaning, transformation, and pipeline implementation underway.
