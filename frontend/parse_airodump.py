import csv
import json

def parse_airodump_csv(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        lines = list(reader)

    aps = []
    parsing_aps = True
    header_map = {}
    header_found = False

    for row in lines:
        row = [c.strip() for c in row]  # limpiar espacios
        if not any(row):
            continue

        # Detectar cambio de bloque (APs -> Clientes)
        if any("Station MAC" in cell for cell in row):
            parsing_aps = False
            continue

        if parsing_aps:
            # Detectar header de APs y mapear columnas
            if not header_found:
                if any("BSSID" in cell for cell in row):
                    header_found = True
                    for idx, col in enumerate(row):
                        header_map[col.lower()] = idx
                continue

            try:
                bssid = row[header_map.get("bssid")]
                channel = row[header_map.get("channel")]
                power = int(row[header_map.get("power")]) if row[header_map.get("power")] else -100
                privacy = row[header_map.get("privacy")]
                essid_idx = header_map.get("essid")  # algunas versiones no tienen ESSID
                essid = row[essid_idx] if essid_idx is not None else ""

                aps.append({
                    "bssid": bssid,
                    "channel": channel,
                    "essid": essid,
                    "privacy": privacy,
                    "power": power,
                    "clients": []
                })
            except (IndexError, ValueError):
                continue
        else:
            # Parseo de clientes
            try:
                client_mac = row[0]
                ap_mac = row[5]
                power = int(row[3]) if row[3] else -100

                for ap in aps:
                    if ap["bssid"].lower() == ap_mac.lower():
                        ap["clients"].append({
                            "mac": client_mac,
                            "power": power
                        })
            except (IndexError, ValueError):
                continue

    return {"aps": aps}

# === Uso ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 parse_airodump.py archivo.csv")
        exit(1)

    resultado = parse_airodump_csv(sys.argv[1])
    with open("recon_output.json", "w") as f:
        json.dump(resultado, f, indent=2)
    print("✅ JSON generado: recon_output.json")
