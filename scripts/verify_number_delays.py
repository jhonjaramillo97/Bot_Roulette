"""
verify_number_delays.py — Auditoria de la base de datos.

Para cada mesa:
1. Cuenta el total de giros registrados
2. Calcula delays de numeros con compute_number_delays (ultimos 100)
3. Verifica contra un calculo manual independiente
4. Detecta mesas sin datos o con anomalias
5. Reporta numeros mas retrasados

Uso:  python verify_number_delays.py [--umbral 50] [--db ruta/ruleta.db]
"""

import sys
import os
import sqlite3
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config.config import TABLES
from backend.roulette.thresholds import get_number_delay_threshold

DB_PATH = None  # Se setea en main()


def get_connection():
    return sqlite3.connect(DB_PATH)


def manual_delays(numeros):
    """
    Calcula delays manualmente (independiente de compute_number_delays).
    numeros[0] es el mas reciente.
    """
    last_seen = {n: None for n in range(37)}
    total = 0
    for idx, item in enumerate(numeros):
        if isinstance(item, dict):
            n = item.get("numero")
        elif hasattr(item, "__getitem__") and not isinstance(item, (str, bytes)):
            try:
                n = item["numero"]
            except:
                n = item
        else:
            n = item

        if n == -1:
            break
        total = idx + 1
        if last_seen[n] is None:
            last_seen[n] = idx
        if None not in last_seen.values():
            break

    delays = {}
    for num in range(37):
        delays[num] = total if last_seen[num] is None else last_seen[num]
    return delays


def format_color(num):
    reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    if num == 0:
        return "[G]"
    elif num in reds:
        return "[R]"
    return "[N]"


def audit_table(table_name, threshold):
    conn = get_connection()

    cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_spins = cursor.fetchone()[0]

    if total_spins == 0:
        conn.close()
        return {
            "table_name": table_name,
            "total_spins": 0,
            "delays": {},
            "alerts": [],
            "errors": ["TABLA VACIA - sin giros registrados"]
        }

    cursor = conn.execute(
        f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC LIMIT 100"
    )
    rows = cursor.fetchall()

    cursor = conn.execute(f"SELECT MAX(timestamp) FROM {table_name}")
    last_ts = cursor.fetchone()[0] or "-"

    conn.close()

    numeros = [{"numero": r[0], "color": r[1], "timestamp": r[2]} for r in rows]

    from backend.roulette.logic import compute_number_delays
    real_delays = compute_number_delays(numeros)

    manual = manual_delays(numeros)
    mismatches = []
    for n in range(37):
        if real_delays[n] != manual[n]:
            mismatches.append(f"N.{n}: real={real_delays[n]} manual={manual[n]}")

    errors = []
    if mismatches:
        errors.append(f"DISCREPANCIA! {len(mismatches)} numeros no coinciden: {', '.join(mismatches[:5])}")

    alerts = [(n, real_delays[n], format_color(n)) for n in range(37) if real_delays[n] >= threshold]
    alerts.sort(key=lambda x: -x[1])

    return {
        "table_name": table_name,
        "total_spins": total_spins,
        "delays": real_delays,
        "alerts": alerts,
        "errors": errors,
        "last_ts": last_ts
    }


def main():
    global DB_PATH

    # Ruta por defecto: buscar en dist/data (donde corre el .exe), luego backend/data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_paths = [
        os.path.join(script_dir, "dist", "data", "ruleta.db"),
        os.path.join(script_dir, "backend", "data", "ruleta.db"),
    ]
    default_db = next((p for p in default_paths if os.path.exists(p)), default_paths[0])

    parser = argparse.ArgumentParser(description="Auditar delays de numeros en la BD")
    parser.add_argument("--umbral", type=int, default=None, help="Umbral de delay (default: valor de la GUI)")
    parser.add_argument("--db", type=str, default=default_db, help="Ruta a la base de datos SQLite")
    args = parser.parse_args()

    DB_PATH = args.db
    threshold = args.umbral or get_number_delay_threshold()

    print(f"=== AUDITORIA DE NUMEROS ===")
    print(f"=== BD: {DB_PATH} ===")
    print(f"=== Umbral configurado: {threshold} giros ===\n")

    if not os.path.exists(DB_PATH):
        print(f"ERROR: No se encontro la base de datos en: {DB_PATH}")
        return

    tables_with_data = 0
    tables_with_alerts = 0
    total_alerts = 0

    for t in TABLES:
        tn = t["table_name"]
        result = audit_table(tn, threshold)

        status = "OK"
        if result["total_spins"] == 0:
            status = "XX"
        elif len(result["alerts"]) > 0:
            status = "!!"

        print(f"{status} {t['name']} ({tn})")
        print(f"   Giros totales: {result['total_spins']} | Ultimo: {result['last_ts']}")

        if result["total_spins"] > 0:
            if result["alerts"]:
                tables_with_alerts += 1
                total_alerts += len(result["alerts"])
                print(f"   !! {len(result['alerts'])} numeros en alerta (>={threshold}):")
                for num, delay, color in result["alerts"][:10]:
                    print(f"      {color} #{num:>2} -> {delay} giros sin salir")
                if len(result["alerts"]) > 10:
                    print(f"      ... y {len(result['alerts']) - 10} mas")
            else:
                top_delays = sorted(result["delays"].items(), key=lambda x: -x[1])[:5]
                print(f"   OK Sin alertas. Top 5 mas retrasados:")
                for num, delay in top_delays[:5]:
                    print(f"      {format_color(num)} #{num:>2} -> {delay} giros (lejos del umbral {threshold})")
        else:
            print(f"   **  Esta mesa no tiene datos -- verifica que el bot la este escaneando")

        if result["errors"]:
            for err in result["errors"]:
                print(f"   **  {err}")

        tables_with_data += 1 if result["total_spins"] > 0 else 0
        print()

    print("=" * 55)
    print(f"Resumen: {tables_with_data}/{len(TABLES)} mesas con datos")
    print(f"         {tables_with_alerts}/{len(TABLES)} mesas con alertas activas")
    print(f"         {total_alerts} alertas totales detectadas")
    print(f"         Umbral: {threshold} giros")

    if tables_with_alerts == 0 and tables_with_data > 0:
        print(f"\nTIP: Ninguna mesa tiene numeros con delay >= {threshold}.")
        print(f"   Si esperabas senales, prueba con un umbral mas bajo: --umbral 20")


if __name__ == "__main__":
    main()
