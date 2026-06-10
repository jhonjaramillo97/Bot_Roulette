"""
Tests unitarios para los algoritmos de analytics:
  - compute_delays
  - compute_color_streak
  - compute_number_delays
  - _chain_match (scanner)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.roulette.logic import compute_delays, compute_color_streak, compute_number_delays
from backend.roulette.scanner import _chain_match


# =============================================================================
# compute_delays
# =============================================================================

class TestComputeDelays:
    def test_basico_docenas_y_columnas(self):
        """Caso normal: cada numero cae en su docena y columna correcta.
        La logica procesa del mas reciente al mas antiguo, acumulando delays
        hasta encontrar cada zona."""
        numeros = [1, 13, 25]
        delays = compute_delays(numeros)
        # 1 (doc1,col1) encontrado i=0. 13 (doc2,col1) encontrado i=1. 25 (doc3,col1) i=2.
        # col2 y col3 nunca aparecen -> delays acumulados = 3
        assert delays == {
            "docena_1": 0, "docena_2": 1, "docena_3": 2,
            "columna_1": 0, "columna_2": 3, "columna_3": 3,
        }

    def test_todas_las_zonas_encontradas(self):
        """Si todas las zonas ya salieron, los delays son las distancias al mas reciente."""
        numeros = [1, 14, 27, 2, 15, 28, 3]
        delays = compute_delays(numeros)
        assert all(v < len(numeros) for v in delays.values())
        assert delays["docena_1"] == 0
        assert delays["docena_2"] == 1
        assert delays["docena_3"] == 2
        assert delays["columna_1"] == 0
        assert delays["columna_2"] == 1
        assert delays["columna_3"] == 2

    def test_cadena_rota_marcador_menos_uno(self):
        """El marcador -1 detiene el conteo de delays."""
        numeros = [1, -1, 13, 25]
        delays = compute_delays(numeros)
        assert delays["docena_1"] == 0
        assert delays["docena_2"] == 1  # solo se proceso el 1 antes del -1
        assert delays["docena_3"] == 1

    def test_solo_ceros(self):
        """Los ceros (0) incrementan todos los delays sin romper la busqueda.
        Con 3 ceros antes del 1, los delays acumulan +3 excepto doc1 que se encuentra al final."""
        numeros = [0, 0, 0, 1]
        delays = compute_delays(numeros)
        assert delays["docena_1"] == 3
        assert delays["docena_2"] == 4
        assert delays["docena_3"] == 4

    def test_sin_datos(self):
        """Lista vacia devuelve todo en 0."""
        delays = compute_delays([])
        assert all(v == 0 for v in delays.values())

    def test_items_como_dicts(self):
        """Soporta items como diccionarios con clave 'numero'."""
        numeros = [{"numero": 1}, {"numero": 13}]
        delays = compute_delays(numeros)
        assert delays["docena_1"] == 0
        assert delays["docena_2"] == 1


# =============================================================================
# compute_color_streak
# =============================================================================

class TestComputeColorStreak:
    def test_racha_roja(self):
        """Racha de 5 rojos consecutivos."""
        numeros = [{"numero": 1, "color": "Red"}, {"numero": 3, "color": "Red"},
                   {"numero": 5, "color": "Red"}, {"numero": 7, "color": "Red"},
                   {"numero": 9, "color": "Red"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Red"
        assert result["streak"] == 5

    def test_racha_negra(self):
        """Racha de 3 negros."""
        numeros = [{"numero": 2, "color": "Black"}, {"numero": 4, "color": "Black"},
                   {"numero": 6, "color": "Black"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Black"
        assert result["streak"] == 3

    def test_cero_comodin_no_rompe_racha(self):
        """El verde (0) suma a la racha sin romperla."""
        numeros = [{"numero": 1, "color": "Red"}, {"numero": 0, "color": "Green"},
                   {"numero": 3, "color": "Red"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Red"
        assert result["streak"] == 3

    def test_color_opuesto_rompe_racha(self):
        """Un color opuesto detiene la racha desde el mas reciente.
        El algoritmo lee del mas reciente (Black 2) hacia atras, y se detiene
        al encontrar Red 1. Racha = Black con streak=1."""
        numeros = [{"numero": 2, "color": "Black"}, {"numero": 1, "color": "Red"},
                   {"numero": 3, "color": "Red"}, {"numero": 5, "color": "Red"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Black"
        assert result["streak"] == 1

    def test_verdes_al_inicio(self):
        """Verdes al inicio cuentan para la racha una vez aparece el primer color."""
        numeros = [{"numero": 0, "color": "Green"}, {"numero": 0, "color": "Green"},
                   {"numero": 1, "color": "Red"}, {"numero": 3, "color": "Red"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Red"
        assert result["streak"] == 4

    def test_cadena_rota_color(self):
        """El marcador -1 detiene el conteo."""
        numeros = [{"numero": 1, "color": "Red"}, {"numero": -1, "color": "Reset"}]
        result = compute_color_streak(numeros)
        assert result["color"] == "Red"
        assert result["streak"] == 1

    def test_sin_datos_color(self):
        """Lista vacia."""
        result = compute_color_streak([])
        assert result["color"] is None
        assert result["streak"] == 0

    def test_solo_verdes(self):
        """Solo verdes, sin color definido."""
        numeros = [{"numero": 0, "color": "Green"}, {"numero": 0, "color": "Green"}]
        result = compute_color_streak(numeros)
        assert result["color"] is None
        assert result["streak"] == 0


# =============================================================================
# compute_number_delays
# =============================================================================

class TestComputeNumberDelays:
    def test_basico(self):
        """3 numeros: el delay de cada uno es su posicion desde el mas reciente."""
        numeros = [1, 2, 3]
        delays = compute_number_delays(numeros)
        assert delays[1] == 0
        assert delays[2] == 1
        assert delays[3] == 2
        assert delays[0] == 3  # nunca salio
        assert delays[36] == 3

    def test_numero_repetido(self):
        """Un numero repetido resetea su delay."""
        numeros = [1, 2, 1]
        delays = compute_number_delays(numeros)
        assert delays[1] == 0  # mas reciente
        assert delays[2] == 1

    def test_cadena_rota(self):
        """-1 detiene el conteo, los delays reflejan solo hasta ahi."""
        numeros = [1, -1, 2, 3]
        delays = compute_number_delays(numeros)
        assert delays[1] == 0
        assert delays[2] == 1  # solo se proceso [1]
        assert delays[0] == 1

    def test_todos_presentes(self):
        """Si todos los numeros 0-36 aparecen, el delay = posicion desde el mas reciente.
        numeros[0]=0 es el mas reciente, numeros[36]=36 es el mas antiguo."""
        numeros = list(range(37))
        delays = compute_number_delays(numeros)
        for n in range(37):
            assert delays[n] == n

    def test_items_como_dicts(self):
        """Soporta diccionarios."""
        numeros = [{"numero": 5}, {"numero": 10}]
        delays = compute_number_delays(numeros)
        assert delays[5] == 0
        assert delays[10] == 1


# =============================================================================
# _chain_match (scanner)
# =============================================================================

class TestChainMatch:
    def test_sin_historial(self):
        """Sin historial en DB, todos los numeros del tile son nuevos."""
        nuevos = _chain_match([10, 20, 30, 40], [], "test")
        assert nuevos == [40, 30, 20, 10]

    def test_empalme_perfecto(self):
        """Los ultimos 4 del tile coinciden con la DB."""
        nums_tile = [1, 2, 3, 4, 5, 6]
        db_nums = [3, 4, 5, 6, 7, 8]
        nuevos = _chain_match(nums_tile, db_nums, "test")
        assert nuevos == [2, 1]

    def test_sin_empalme_suficiente(self):
        """Solo 2 coinciden, necesita _MIN_CHAIN=4."""
        nums_tile = [99, 88, 1, 2, 3, 4]
        db_nums = [1, 2, 10, 11]
        nuevos = _chain_match(nums_tile, db_nums, "test")
        assert nuevos[0] == -1

    def test_tile_completo_ya_en_db(self):
        """Todos los numeros del tile ya estan en la DB."""
        nums_tile = [1, 2, 3, 4]
        db_nums = [1, 2, 3, 4, 5, 6]
        nuevos = _chain_match(nums_tile, db_nums, "test")
        assert nuevos == []

    def test_empalme_al_inicio(self):
        """El empalme comienza en el indice 0 del tile (todos nuevos desde ahi)."""
        nums_tile = [3, 4, 5, 6, 1, 2]
        db_nums = [3, 4, 5, 6, 7, 8]
        nuevos = _chain_match(nums_tile, db_nums, "test")
        assert nuevos == []
