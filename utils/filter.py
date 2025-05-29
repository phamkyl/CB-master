def loc_dien_thoai(info, df):
    ket_qua = df.copy()

    if "PriceRange" in info:
        price_from, price_to = info["PriceRange"]
        ket_qua = ket_qua[(ket_qua["FinalPrice"] >= price_from) & (ket_qua["FinalPrice"] <= price_to)]
    elif "FinalPrice" in info:
        price = info["FinalPrice"]
        ket_qua = ket_qua[(ket_qua["FinalPrice"] >= price - 1_000_000) & (ket_qua["FinalPrice"] <= price + 1_000_000)]

    if "Brand" in info:
        ket_qua = ket_qua[ket_qua["Brand"].str.lower().isin([b.lower() for b in info["Brand"]])]
    if "RAM" in info:
        ket_qua = ket_qua[ket_qua["RAM"] >= info["RAM"]]
    if "Storage" in info:
        ket_qua = ket_qua[ket_qua["Storage"] >= info["Storage"]]
    if "RearCameraResolution" in info:
        ket_qua = ket_qua[ket_qua["RearCameraResolution"] >= info["RearCameraResolution"]]
    if "BatteryCapacity" in info:
        ket_qua = ket_qua[ket_qua["BatteryCapacity"] >= info["BatteryCapacity"]]

    return ket_qua
