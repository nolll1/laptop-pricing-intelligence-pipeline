import pandas as pd
import numpy as np
import re
from pathlib import Path


# refurbished or not
def get_refurbished(row):
    text = f"{row['title']} {row['Cosmetic Condition']}"
    if re.search(r'\b(refurbished|refurb|grade a|grade b|grade c)\b', text, re.IGNORECASE):
        return 1
    return 0


# extracting brands
def clean_brand(row):
    KNOWN_BRANDS = [
        'ASUS', 'Acer', 'Apple', 'Dell', 'DELL', 'HP', 'Lenovo', 'MSI', 'Microsoft', 
        'Samsung', 'Panasonic', 'GPD', 'THUNDEROBOT', 'NIAKUN', 'BiTECOOL', 
        'Auusda', 'Exsurf', 'NINGMEI', 'SAGAWHALE', 'Gigabyte', 'LG', 'Razer'
    ]

    BRAND_MAP = {
        'dell': 'Dell', 'asus': 'Asus', 'hp': 'HP', 'lenovo': 'Lenovo', 'acer': 'Acer',
        'msi': 'MSI', 'apple': 'Apple', 'bitecool': 'BiTECOOL', 'auusda': 'Auusda',
        'exsurf': 'Auusda', 'ningmei': 'NINGMEI', 'sagawhale': 'SAGAWHALE', 'microsoft': 'Microsoft',
        'samsung': 'Samsung', 'panasonic': 'Panasonic', 'gpd': 'GPD', 'thunderobot': 'THUNDEROBOT',
        'gigabyte': 'Gigabyte', 'lg': 'LG', 'razer': 'Razer'
    }

    SERIES_BRAND_MAP = {
        r'\bthinkpad\b': 'Lenovo', r'\bideapad\b': 'Lenovo', r'\byoga\b': 'Lenovo', r'\blegion\b': 'Lenovo', r'\bloq\b': 'Lenovo',
        r'\blatitude\b': 'Dell', r'\bprecision\b': 'Dell', r'\binspiron\b': 'Dell', r'\bvostro\b': 'Dell', r'\balienware\b': 'Dell', r'\bxps\b': 'Dell',
        r'\belitebook\b': 'HP', r'\bprobook\b': 'HP', r'\bvictus\b': 'HP', r'\bpavilion\b': 'HP', r'\bomnibook\b': 'HP', r'\bzbook\b': 'HP', r'\benvy\b': 'HP', r'\bchromebook\b': 'HP',
        r'\bvivobook\b': 'Asus', r'\bzenbook\b': 'Asus', r'\brog\b': 'Asus', r'\btuf\b': 'Asus',
        r'\baspire\b': 'Acer', r'\bpredator\b': 'Acer', r'\bnitro\b': 'Acer', r'\bswift\b': 'Acer',
        r'\bkatana\b': 'MSI', r'\braider\b': 'MSI', r'\bstealth\b': 'MSI', r'\bprestige\b': 'MSI', r'\bventure\b': 'MSI',
        r'\bmacbook\b': 'Apple', r'\bsurface\b': 'Microsoft', r'\bgalaxy book\b': 'Samsung'
    }

    b = str(row['Brand']).strip()
    if b and b.lower() != 'nan':
        return BRAND_MAP.get(b.lower(), b)
    title = str(row['title'])
    for kb in KNOWN_BRANDS:
        if re.search(r'\b' + re.escape(kb) + r'\b', title, re.IGNORECASE):
            return BRAND_MAP.get(kb.lower(), kb.title())
    for series_pat, brand in SERIES_BRAND_MAP.items():
        if re.search(series_pat, title, re.IGNORECASE):
            return brand
    first_word = title.split()[0].replace('Refurbished', '').strip()
    if first_word:
        return BRAND_MAP.get(first_word.lower(), first_word.capitalize())
    return 'Unknown'


# series extraction
def clean_series(row):
    # extracting laptop series (e.g. ThinkPad, VivoBook, EliteBook)
    SERIES_MAP = {
        # Apple / Microsoft / Samsung — check compound names before the bare word
        r'\bmacbook pro\b': 'MacBook Pro', r'\bmacbook air\b': 'MacBook Air', r'\bmacbook\b': 'MacBook',
        r'\bsurface laptop\b': 'Surface Laptop', r'\bsurface pro\b': 'Surface Pro', r'\bsurface\b': 'Surface',
        r'\bgalaxy book\d?\s*(?:pro|ultra)?\b': 'Galaxy Book',
        # Lenovo
        r'\bthinkbook\b': 'ThinkBook', r'\bthinkpad\b': 'ThinkPad', r'\bideapad\b': 'IdeaPad',
        r'\blegion\b': 'Legion', r'\bloq\b': 'LOQ', r'\byoga\b': 'Yoga', r'\bslim\b': 'Slim',
        r'\bv[\s-]?series\b': 'V-Series', r'\bv1[0-9](?:\s|-|$)': 'V-Series',
        # Dell
        r'\bxps\b': 'XPS', r'\balienware\b': 'Alienware', r'\blatitude\b': 'Latitude',
        r'\bprecision\b': 'Precision', r'\bvostro\b': 'Vostro', r'\binspiron\b': 'Inspiron',
        r'\bdell pro\b': 'Dell Pro', r'\b(?:16|14)\s*plus\b': 'Dell Plus',
        # HP
        r'\belitebook\b': 'EliteBook', r'\bprobook\b': 'ProBook', r'\bzbook\b': 'ZBook',
        r'\bvictus\b': 'Victus', r'\bomnibook\b': 'OmniBook', r'\benvy\b': 'Envy',
        r'\bpavilion\b': 'Pavilion', r'\bchromebook\b': 'Chromebook',
        # Asus
        r'\brog\b': 'ROG', r'\btuf\b': 'TUF', r'\bzenbook\b': 'ZenBook', r'\bvivobook\b': 'VivoBook',
        # Acer
        r'\bpredator\b': 'Predator', r'\btravelmate\b': 'TravelMate', r'\bnitro\b': 'Nitro',
        r'\baspire\b': 'Aspire', r'\bswift\b': 'Swift',
        # MSI
        r'\bventurepro\b': 'VenturePro', r'\bventure\b': 'Venture', r'\braider\b': 'Raider',
        r'\bkatana\b': 'Katana', r'\bstealth\b': 'Stealth', r'\bprestige\b': 'Prestige',
        r'\bsummit\b': 'Summit', r'\bmodern\b': 'Modern',
    }

    title = str(row['title'])
    for pat, name in SERIES_MAP.items():
        if re.search(pat, title, re.IGNORECASE):
            return name
    # fall back to the raw 'Series' column when title has no known keyword
    raw = row.get('Series')
    if pd.notnull(raw):
        raw = str(raw).strip()
        for pat, name in SERIES_MAP.items():
            if re.search(pat, raw, re.IGNORECASE):
                return name
        # only trust it if it looks like a real series name, not a part/model number
        if raw and re.fullmatch(r'[A-Za-z][A-Za-z0-9\-\s\.]{1,24}', raw) and not raw.isdigit():
            return raw.title()
    return 'Other'


# shipping or not, with cost
def clean_shipping(val):
    s = str(val).strip()
    if 'free' in s.lower():
        return 0.0, 1
    m = re.search(r'(\d+(?:\.\d+)?)', s)
    if m:
        return float(m.group(1)), 0
    return 0.0, 1


# ram(memory) capacity and type
def extract_ram_gb(row):
    mem = str(row['Memory'])
    m = re.search(r'(\d+)\s*GB', mem, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if val in [4, 8, 12, 16, 24, 32, 40, 48, 64, 96, 128]:
            return val
    title = str(row['title'])
    m = re.search(r'(\d+)\s*GB\s*(?:DDR|LPDDR|RAM|Memory|onboard)', title, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if val in [4, 8, 12, 16, 24, 32, 40, 48, 64, 96, 128]:
            return val
    m = re.search(r'\b(4|8|12|16|24|32|40|48|64|96|128)\s*GB\b', title, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 16

def extract_ram_type(row):
    text = f"{row['Memory']} {row['Memory Spec']} {row['title']}"
    m = re.search(r'(LPDDR5X|LPDDR5|LPDDR4X|LPDDR4|LPDDR3|DDR5|DDR4|DDR3)', text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    return 'DDR4'


# storage capacity and type
def extract_storage_gb(row):
    text = f"{row['SSD']} {row['HDD']} {row['Storage Spec']} {row['title']}"
    m = re.search(r'(\d+(?:\.\d+)?)\s*TB', text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        return int(val * 1024)
    m = re.search(r'(\d+)\s*GB\s*(?:SSD|NVMe|PCIe|SATA|HDD|Storage|UFS|eMMC)', text, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if val >= 64 and val != 1000:
            return val
    m = re.search(r'\b(128|256|512)\s*GB\b', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 512

def extract_storage_type(row):
    text = f"{row['SSD']} {row['HDD']} {row['Storage Spec']} {row['title']}"
    if re.search(r'\b(NVMe|PCIe)\b', text, re.IGNORECASE):
        return 'NVMe PCIe SSD'
    elif re.search(r'\bSATA\b', text, re.IGNORECASE):
        return 'SATA SSD'
    elif re.search(r'\bSSD\b', text, re.IGNORECASE):
        return 'SSD'
    elif re.search(r'\bHDD\b', text, re.IGNORECASE):
        return 'HDD'
    return 'SSD'


# screen size, display resolution categoy and touchscreen
def extract_screen_size(row):
    val = row['Screen Size']
    if pd.notnull(val):
        m = re.search(r'(\d+(?:\.\d+)?)', str(val))
        if m:
            s = float(m.group(1))
            if 10 <= s <= 20:
                return s
    title = str(row['title'])
    m = re.search(r'(\d{2}(?:\.\d)?)\s*(?:"|inch|in\b|-inch)', title, re.IGNORECASE)
    if m:
        s = float(m.group(1))
        if 10 <= s <= 20:
            return s
    return 15.6

def extract_resolution(row):
    res = f"{row['Resolution']} {row['Display Type']} {row['title']}"
    m = re.search(r'(\d{3,4})\s*x\s*(\d{3,4})', res, re.IGNORECASE)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        return f"{w}x{h}"
    if re.search(r'\b3K\b', res, re.IGNORECASE):
        return '2880x1800'
    elif re.search(r'\b4K\b|UHD', res, re.IGNORECASE):
        return '3840x2160'
    elif re.search(r'\bFHD\b|1080p', res, re.IGNORECASE):
        return '1920x1080'
    elif re.search(r'\bHD\b', res, re.IGNORECASE):
        return '1366x768'
    return '1920x1080'

def get_res_category(res):
    if '3840' in res or '2160' in res or '4K' in res:
        return '4K UHD'
    elif '2880' in res or '2560' in res or '3K' in res or '2K' in res or '1600' in res:
        return 'QHD / 3K'
    elif '1200' in res or '1920x1200' in res:
        return 'FHD+ (1200p)'
    elif '1080' in res or '1920x1080' in res or '1980' in res:
        return 'FHD (1080p)'
    elif '768' in res or '900' in res or '1366' in res:
        return 'HD'
    return 'FHD (1080p)'


# processor(cpu - brand, series and model) and core count
def extract_cpu_info(row):
    text = f"{row['Processor Name']} {row['CPU Type']} {row['CPU']} {row['title']}"
    brand = 'Intel'
    if re.search(r'\b(AMD|Ryzen|Athlon)\b', text, re.IGNORECASE):
        brand = 'AMD'
    elif re.search(r'\b(Apple|MacBook|M1|M2|M3)\b', text, re.IGNORECASE):
        brand = 'Apple'
    elif re.search(r'\b(Snapdragon|Qualcomm)\b', text, re.IGNORECASE):
        brand = 'Snapdragon'
    elif re.search(r'\b(Intel|Core|Celeron|Pentium|Xeon)\b', text, re.IGNORECASE):
        brand = 'Intel'
        
    series = 'Other'
    m = re.search(r'Core Ultra \d', text, re.IGNORECASE)
    if m:
        series = m.group(0)
    else:
        m = re.search(r'Core i\d', text, re.IGNORECASE)
        if m:
            series = m.group(0)
        else:
            m = re.search(r'Ryzen AI \d', text, re.IGNORECASE)
            if m:
                series = m.group(0)
            else:
                m = re.search(r'Ryzen \d', text, re.IGNORECASE)
                if m:
                    series = m.group(0)
                elif re.search(r'Athlon', text, re.IGNORECASE):
                    series = 'Athlon'
                elif re.search(r'Pentium', text, re.IGNORECASE):
                    series = 'Pentium'
                elif re.search(r'Celeron', text, re.IGNORECASE):
                    series = 'Celeron'
                elif re.search(r'Processor N\d+|Intel N\d+|N150|N95|N5095', text, re.IGNORECASE):
                    series = 'Intel N-Series'
                else:
                    m = re.search(r'M[123](?:\s*(?:Pro|Max|Ultra))?', text, re.IGNORECASE)
                    if m:
                        series = m.group(0)

    model = ''
    patterns = [
        r'Intel Core Ultra \d \d+[A-Z]*',
        r'Core Ultra \d \d+[A-Z]*',
        r'i\d[- ]\d{4,5}[A-Z]*',
        r'Ryzen (?:AI )?\d \d{4}[A-Z]*',
        r'Ryzen AI \d \d+',
        r'Ryzen \d PRO \d{4}[A-Z]*',
        r'Athlon Silver \d+[A-Z]*',
        r'Pentium Gold \d+[A-Z]*',
        r'Celeron N\d+',
        r'N\d{3,4}'
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            model = m.group(0)
            break
    if not model:
        model = series

    return pd.Series([brand, series.title(), model])

def extract_cores(row):
    text = f"{row['Number of Cores']} {row['title']}"
    m = re.search(r'(\d+)\s*[- ]*(?:core|cores)\b', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    if re.search(r'Quad-core|4-core|4 Cores', text, re.IGNORECASE):
        return 4
    if re.search(r'Octa-core|8-core|8 Cores', text, re.IGNORECASE):
        return 8
    if re.search(r'Dual-core|2-core|2 Cores', text, re.IGNORECASE):
        return 2
    if re.search(r'Hexa-core|6-core|6 Cores', text, re.IGNORECASE):
        return 6
    if re.search(r'10-core', text, re.IGNORECASE):
        return 10
    if re.search(r'12-core', text, re.IGNORECASE):
        return 12
    if re.search(r'14-core', text, re.IGNORECASE):
        return 14
    if re.search(r'16-core', text, re.IGNORECASE):
        return 16
    return None


# gpu - brand, type, model and operating system
def extract_gpu_info(row):
    text = f"{row['GPU/VPU']} {row['Graphic Type']} {row['Graphics Card']} {row['title']}"
    brand = 'Integrated / Other'
    if re.search(r'NVIDIA|GeForce|RTX|GTX|Quadro|T550|T1200|T2000', text, re.IGNORECASE):
        brand = 'NVIDIA'
    elif re.search(r'AMD|Radeon|Vega', text, re.IGNORECASE):
        brand = 'AMD'
    elif re.search(r'Intel|Iris|Arc|UHD|HD Graphics', text, re.IGNORECASE):
        brand = 'Intel'
    elif re.search(r'Apple', text, re.IGNORECASE):
        brand = 'Apple'

    gpu_type = 'Integrated'
    if brand in ['NVIDIA'] or re.search(r'Dedicated|GeForce|RTX|GTX|Quadro', text, re.IGNORECASE):
        gpu_type = 'Dedicated'

    model = 'Integrated Graphics'
    patterns = [
        r'RTX \d{4}(?:\s*Laptop GPU)?',
        r'Quadro T\d{4}',
        r'T\d{3,4}',
        r'Radeon 780M',
        r'Radeon RX Vega \d',
        r'Radeon Graphics',
        r'Arc 140V|Arc Graphics',
        r'Iris Xe',
        r'UHD Graphics'
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            model = m.group(0)
            break
            
    return pd.Series([brand, gpu_type, model])

def clean_os(val, title):
    text = f"{val} {title}"
    if re.search(r'Windows 11 Pro', text, re.IGNORECASE):
        return 'Windows 11 Pro'
    elif re.search(r'Windows 11 Home', text, re.IGNORECASE):
        return 'Windows 11 Home'
    elif re.search(r'Windows 11', text, re.IGNORECASE):
        return 'Windows 11 Home'
    elif re.search(r'Windows 10 Pro', text, re.IGNORECASE):
        return 'Windows 10 Pro'
    elif re.search(r'Windows 10', text, re.IGNORECASE):
        return 'Windows 10 Home'
    elif re.search(r'Chrome', text, re.IGNORECASE):
        return 'Chrome OS'
    elif re.search(r'Mac', text, re.IGNORECASE):
        return 'macOS'
    return 'Windows 11 Home'


def main(df) -> None:
    # Filter non-laptop items (e.g. USB-C Docking Stations)
    df = df[~df['title'].str.contains('USB-C DOCKING STATION', case=False, na=False)].copy().reset_index(drop=True)
    print(f"Filtered Laptop Dataset: {len(df)} rows")


    # refurbished or not
    df['is_refurbished'] = df.apply(get_refurbished, axis=1)


    # extracting brands
    df['brand'] = df.apply(clean_brand, axis=1)


    # extracting series
    df['series'] = df.apply(clean_series, axis=1)


    # current and old prices, and discounts
    df['current_price'] = df['current_price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')

    df['old_price'] = df['old_price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    df['old_price'] = pd.to_numeric(df['old_price'], errors='coerce')

    df['discount_percent'] = df['discount'].astype(str).str.replace('%', '', regex=False).str.strip()
    df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce')

    # Impute old price when missing but current_price & discount exist
    mask = df['old_price'].isnull() & (df['discount_percent'] > 0) & df['current_price'].notnull()
    df.loc[mask, 'old_price'] = np.round(df.loc[mask, 'current_price'] / (1 - df.loc[mask, 'discount_percent'] / 100), 2)
    df['old_price'] = df['old_price'].fillna(df['current_price'])

    # Calculate missing discount percent
    mask = df['discount_percent'].isnull() & df['current_price'].notnull() & df['old_price'].notnull()
    calc_disc = np.maximum(0, np.round((df['old_price'] - df['current_price']) / df['old_price'] * 100, 1))
    df.loc[mask, 'discount_percent'] = calc_disc
    df['discount_percent'] = df['discount_percent'].fillna(0)

    df['current_price'] = df['current_price'].fillna(df['old_price'])


    # shipping free or not, with cost 
    shipping_info = df['shipping'].apply(clean_shipping)
    df['shipping_cost'] = [x[0] for x in shipping_info]
    df['is_free_shipping'] = [x[1] for x in shipping_info]


    # ram(memory) capacity and type
    df['ram_capacity_gb'] = df.apply(extract_ram_gb, axis=1)
    df['ram_type'] = df.apply(extract_ram_type, axis=1)


    # storage capacity and type
    df['storage_capacity_gb'] = df.apply(extract_storage_gb, axis=1)
    df['storage_type'] = df.apply(extract_storage_type, axis=1)


    # screen size, display resolution categoy and touchscreen
    df['screen_size_inches'] = df.apply(extract_screen_size, axis=1)
    df['resolution'] = df.apply(extract_resolution, axis=1)
    df['resolution_category'] = df['resolution'].apply(get_res_category)
    df['is_touchscreen'] = df.apply(lambda r: 1 if re.search(r'Touch|Touchscreen', f"{r['Touchscreen']} {r['Display Type']} {r['title']}", re.IGNORECASE) else 0, axis=1)


    # processor(cpu - brand, series and model) and core count
    df[['cpu_brand', 'cpu_series', 'cpu_model']] = df.apply(extract_cpu_info, axis=1)
    df['cpu_cores'] = df.apply(extract_cores, axis=1)


    # gpu - brand, type, model and operating system
    df[['gpu_brand', 'gpu_type', 'gpu_model']] = df.apply(extract_gpu_info, axis=1)
    df['operating_system'] = df.apply(lambda r: clean_os(r['Operating System'], r['title']), axis=1)


    # rating, backlit keyboard, ai ready or not
    df['is_ai_pc'] = df.apply(lambda r: 1 if re.search(r'Copilot\+|AI Ready|AI PC|NPU', f"{r['AI Features']} {r['Neural Processing Unit (NPU)']} {r['title']}", re.IGNORECASE) else 0, axis=1)
    df['has_backlit_keyboard'] = df.apply(lambda r: 1 if re.search(r'Backlit', f"{r['Backlit Keyboard']} {r['Keyboard']} {r['title']}", re.IGNORECASE) else 0, axis=1)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_num'] = pd.to_numeric(df['rating_num'], errors='coerce').fillna(0).astype(int)


    # cleaned_df
    final_cols = [
        'title', 'brand', 'series', 'is_refurbished', 'current_price', 'old_price', 'discount_percent',
        'shipping_cost', 'is_free_shipping', 'rating', 'rating_num', 'operating_system',
        'screen_size_inches', 'resolution', 'resolution_category', 'is_touchscreen',
        'ram_capacity_gb', 'ram_type', 'storage_capacity_gb', 'storage_type',
        'cpu_brand', 'cpu_series', 'cpu_model', 'cpu_cores',
        'gpu_brand', 'gpu_type', 'gpu_model', 'is_ai_pc', 'has_backlit_keyboard', 'link'
    ]

    cleaned_df = df[final_cols].copy()
    print(f"Final Shape: {cleaned_df.shape[0]} rows x {cleaned_df.shape[1]} columns\n")

    return cleaned_df


if __name__ == "__main__":
    cleaned_df = main()