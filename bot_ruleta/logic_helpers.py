"""
Helpers compartidos por las funciones de analytics (logic.py).
Extraidos para eliminar duplicacion de codigo.
"""

KEYCAP_MAP = {
    "0": "0\u20e3", "1": "1\u20e3", "2": "2\u20e3", "3": "3\u20e3", "4": "4\u20e3",
    "5": "5\u20e3", "6": "6\u20e3", "7": "7\u20e3", "8": "8\u20e3", "9": "9\u20e3",
}


def extract_numero(item):
    """Extrae el valor numerico de un item que puede ser dict/Row o int.
    Retorna el numero (o el item mismo si no es dict).
    """
    if hasattr(item, '__getitem__') and not isinstance(item, (str, bytes, int)):
        try:
            return item['numero']
        except Exception:
            return item
    return item


def nums_to_emoji(items):
    """Convierte una lista de numeros/dicts recientes en string de emojis.
    items[0] es el mas reciente; se invierte para mostrar orden cronologico.
    """
    emojis = []
    for item in reversed(items[:10]):
        n = item["numero"] if isinstance(item, dict) else item
        if n == 10:
            emojis.append("\U0001f51f")
        else:
            emojis.append("".join(KEYCAP_MAP[c] for c in str(n)))
    return " ".join(emojis)
