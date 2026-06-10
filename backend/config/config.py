"""
Configuracion centralizada del bot de ruleta.
Constantes, configuracion de mesas, URLs.
"""

import os
from typing import List, Dict

# --- MODO DE OPERACION ---
LOBBY_MODE: bool = True

# --- MESAS CONFIGURADAS ---
TABLES: List[Dict[str, str]] = [
    {"name": "Ruleta Latina", "id": "roulerw234rwl292-234", "op_id": "234", "table_name": "ruleta_latina"},
    {"name": "Mega Roulette", "id": "1hl65ce1lxuqdrkr-204", "op_id": "204", "table_name": "mega_roulette"},
    {"name": "Brazilian Roulette", "id": "rwbrzportrwa16rg-237", "op_id": "237", "table_name": "brazilian_roulette"},
    {"name": "Roulette 1", "id": "g03y1t9vvuhrfytl-227", "op_id": "227", "table_name": "roulette_1"},
    {"name": "Roulette 3", "id": "chroma229rwltr22-230", "op_id": "230", "table_name": "roulette_3"},
    {"name": "Roulette Macao", "id": "yqpz3ichst2xg439-206", "op_id": "206", "table_name": "roulette_macao"},
     
    # Nuevas mesas añadidas a petición del usuario
    {"name": "Roulette 2 Extra Time", "id": "5kvxlw4c1qm3xcyn-201", "op_id": "201", "table_name": "roulette_2_extra_time"},
    {"name": "Brazilian Mega Roulette", "id": "mrbras531mrbr532-287", "op_id": "287", "table_name": "brazilian_mega_roulette"},
    {"name": "Lucky 6 Roulette", "id": "lucky6roulettea3-211a1", "op_id": "211a1", "table_name": "lucky_6_roulette"},
    {"name": "Auto Roulette", "id": "5bzl2835s5ruvweg-225", "op_id": "225", "table_name": "auto_roulette"},

    # Lote de ruletas regionales
    {"name": "Stake Roulette", "id": "rw321stakerws321-236", "op_id": "236", "table_name": "stake_roulette"},
    {"name": "Turkish Roulette", "id": "p8l1j84prrmxzyic-224", "op_id": "224", "table_name": "turkish_roulette"},
    {"name": "German Roulette", "id": "s2x6b4jdeqza2ge2-222", "op_id": "222", "table_name": "german_roulette"},
    {"name": "Romanian Roulette", "id": "romania233rwl291-233", "op_id": "233", "table_name": "romanian_roulette"},
    {"name": "Roulette Italia Tricolore", "id": "v1c52fgw7yy02upz-223", "op_id": "223", "table_name": "roulette_italia_tricolore"},
    {"name": "Russian Roulette", "id": "t4jzencinod6iqwi-221", "op_id": "221", "table_name": "russian_roulette"},
    {"name": "Gates of Olympus Roulette", "id": "gatesofolympus01-2244", "op_id": "2244", "table_name": "gates_of_olympus_roulette"},
    {"name": "Turkish Mega Roulette", "id": "megar0ul3tt3trk1-208", "op_id": "208", "table_name": "turkish_mega_roulette"},
    {"name": "Mega Roulette 3000", "id": "megaroulette3k01-2901", "op_id": "2901", "table_name": "mega_roulette_3000"},
]

# --- URLs ---
LOBBY_URL: str = "https://stake.com.co/es/casino/juego/roulette-lobby-571"

# --- DIRECTORIOS ---
DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# --- INTERVALOS ---
AFK_INTERVAL: int = 300  # segundos (300 = 5 min produccion)

# --- COLORES DE RULETA ---
REDS: List[str] = ['1', '3', '5', '7', '9', '12', '14', '16', '18',
        '19', '21', '23', '25', '27', '30', '32', '34', '36']


