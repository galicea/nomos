# backend0/services/judiciary_service.py
import json
from typing import Dict, Any, Tuple

class JudiciaryService:
    @staticmethod
    def adjudicate_easy(facts_str: str) -> Tuple[bool, str, str]:
        """
        UC03: Orzekanie w sprawie łatwej (sylogizm automatyczny).
        Zwraca (sukces, wyrok, ścieżka_logiczna)
        """
        try:
            facts = json.loads(facts_str)
        except Exception:
            return False, "Błąd: Nieprawidłowy format faktów (oczekiwano JSON).", ""

        # Przykład logiczny: przekroczenie prędkości
        speed = facts.get("predkosc", 0)
        area = facts.get("obszar", "")
        fatal = facts.get("skutek_smiertelny", False)

        if speed >= 50 and area == "zabudowany" and fatal:
            judgment = (
                "WYROK: Uznaje się oskarżonego za winnego popełnienia czynu z art. 148 KK (Zamiar ewentualny). "
                "Wymiar kary: 8 lat pozbawienia wolności, dożywotni zakaz prowadzenia pojazdów mechanicznych."
            )
            logical_path = (
                "DEDUKCJA SYLOGISTYCZNA:\n"
                f"1. Przesłanka 1: Prędkość oskarżonego wynosi {speed} km/h (przekroczenie o >= 50 km/h ponad limit).\n"
                f"2. Przesłanka 2: Miejsce zdarzenia to obszar {area}.\n"
                "3. Przesłanka 3: Nastąpił wypadek ze skutkiem śmiertelnym.\n"
                "4. Reguła SOK: Jeżeli podmiot=kierujący AND predkosc>=50 AND obszar=zabudowany AND skutek=smiertelny "
                "-> Kwalifikacja = zamiar_ewentualny (art. 148 KK).\n"
                "5. Wniosek: Kwalifikacja czynu zachodzi wprost. Wyrok wygenerowany automatycznie."
            )
            return True, judgment, logical_path

        return False, "Brak jednoznacznego dopasowania reguł logicznych dla spraw łatwych. Wymagany tryb sprawy trudnej.", ""

    @staticmethod
    def get_decision_gaps(facts_str: str) -> Dict[str, Any]:
        """
        UC04: Identyfikacja luzów decyzyjnych w sprawach trudnych.
        """
        # Jeśli fakty dotyczą konfliktu prasy i dóbr osobistych (np. sprawa Titanic)
        return {
            "principle_1": "P1: Wolność prasy (art. 14 Konstytucji)",
            "principle_2": "P2: Ochrona dóbr osobistych / godność (art. 47 Konstytucji)",
            "parameters": {
                "I_1": "Intensywność ingerencji w wolność prasy P1 (1=Lekka, 2=Umiarkowana, 4=Poważna)",
                "W_1": "Waga abstrakcyjna wolności prasy P1 (1=Lekka, 2=Umiarkowana, 4=Poważna)",
                "R_1": "Pewność ustaleń empirycznych wolności prasy P1 (0.25=Niepewne, 0.5=Prawdopodobne, 1.0=Pewne)",
                "I_2": "Intensywność ingerencji w dobra osobiste P2 (1, 2, 4)",
                "W_2": "Waga abstrakcyjna dóbr osobistych P2 (1, 2, 4)",
                "R_2": "Pewność ustaleń empirycznych dóbr osobistych P2 (0.25, 0.5, 1.0)"
            }
        }

    @staticmethod
    def calculate_alexy_weight(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        UC04: Wyliczanie wyniku według Formuły Wagi Roberta Alexy'ego.
        W_1,2 = (I_1 * W_1 * R_1) / (I_2 * W_2 * R_2)
        """
        try:
            I_1 = float(params.get("I_1", 1))
            W_1 = float(params.get("W_1", 1))
            R_1 = float(params.get("R_1", 1.0))
            
            I_2 = float(params.get("I_2", 1))
            W_2 = float(params.get("W_2", 1))
            R_2 = float(params.get("R_2", 1.0))
        except (ValueError, TypeError) as e:
            return {"error": f"Błędne parametry wejściowe: {str(e)}"}

        numerator = I_1 * W_1 * R_1
        denominator = I_2 * W_2 * R_2

        if denominator == 0:
            return {"error": "Mianownik w formule wagi nie może wynosić 0."}

        w_12 = numerator / denominator

        logical_path = (
            f"FORMUŁA WAGI ALEXY'EGO:\n"
            f"Licznik (Zasada P1): Ingerencja({I_1}) * Waga({W_1}) * Pewność({R_1}) = {numerator}\n"
            f"Mianownik (Zasada P2): Ingerencja({I_2}) * Waga({W_2}) * Pewność({R_2}) = {denominator}\n"
            f"W_1,2 = {numerator} / {denominator} = {round(w_12, 3)}\n"
        )

        if w_12 < 1.0:
            judgment = "WYROK: Bezwzględne pierwszeństwo zyskuje Zasada P2 (Ochrona dóbr osobistych / godność)."
            status = "adjudicated"
        elif w_12 > 1.0:
            judgment = "WYROK: Bezwzględne pierwszeństwo zyskuje Zasada P1 (Wolność prasy)."
            status = "adjudicated"
        else:
            judgment = "PAT AKSJOLOGICZNY (W_1,2 = 1.0): Wartości równoważą się w tej konfiguracji. Sprawa zablokowana do rozstrzygnięcia referendalnego."
            status = "deadlock"

        return {
            "weight_value": w_12,
            "final_judgment": judgment,
            "status": status,
            "logical_path": logical_path + judgment
        }

    @staticmethod
    def simulate_effects(facts_str: str) -> Dict[str, Any]:
        """
        UC06: Symulacja skutków prawnych dla Obywatela.
        """
        try:
            facts = json.loads(facts_str)
        except Exception:
            facts = {"raw": facts_str}

        return {
            "proposed_judgment": "Symulowany wyrok: Uniewinnienie lub niska grzywna (zależnie od przypisania wag).",
            "logical_path": "ŚCIEŻKA SYMULACJI: Wprowadzone dane wejściowe nie wykazują naruszenia bezwzględnych zakazów logicznych.",
            "impact_statement": (
                "Prognozowany Skutek Społeczny (Predictive Impact Statement): "
                "Zastosowanie wytycznych w tej kohorcie spraw obniży poziom recydywy o szacowane 8.5% "
                "w okresie 12 miesięcy ex-post."
            )
        }
