import re

def trich_xuat_thong_tin(text, BRANDS):
    info = {}

    brand_matches = [brand for brand in BRANDS if brand.lower() in text.lower()]
    if brand_matches:
        info["Brand"] = brand_matches

    price_numbers = re.findall(r'(\d{1,3})\s*(triệu|tr)?', text.lower())
    price_ranges = re.findall(r'(\d{1,3})\s*(triệu|tr)?\s*(đến|-|~)\s*(\d{1,3})\s*(triệu|tr)?', text.lower())

    if price_ranges:
        start, _, _, end, _ = price_ranges[0]
        price_from = int(start) * 1_000_000
        price_to = int(end) * 1_000_000
        if price_from > price_to:
            price_from, price_to = price_to, price_from
        info["PriceRange"] = (price_from, price_to)
    elif len(price_numbers) >= 2:
        p_from = int(price_numbers[0][0]) * 1_000_000
        p_to = int(price_numbers[1][0]) * 1_000_000
        if p_from > p_to:
            p_from, p_to = p_to, p_from
        info["PriceRange"] = (p_from, p_to)
    elif price_numbers:
        info["FinalPrice"] = int(price_numbers[0][0]) * 1_000_000

    if match := re.search(r'ram\s*(\d+)', text.lower()):
        info["RAM"] = int(match.group(1))
    if match := re.search(r'(?:bộ nhớ|storage)?\s*(\d+)\s*gb', text.lower()):
        info["Storage"] = int(match.group(1))
    if match := re.search(r'camera\s*(\d+)', text.lower()):
        info["RearCameraResolution"] = int(match.group(1))
    if match := re.search(r'(?:pin|battery)\s*(\d+)', text.lower()):
        info["BatteryCapacity"] = int(match.group(1))

    return info
