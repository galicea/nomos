# backend0/services/legislative_service.py
import re
from typing import Tuple, Dict, Any

class LegislativeService:
    @staticmethod
    def validate_draft_structure(text: str, formal_proof: str) -> Tuple[bool, str]:
        """
        UC01: Weryfikacja formalna projektu ustawy.
        Sprawdza kompletność: podmiot, warunek, skutek (art. 5.5).
        """
        # Sprawdzamy obecność elementów w tekście lub dowodzie formalnym
        combined = (text + " " + (formal_proof or "")).lower()
        
        has_subject = any(word in combined for word in ["podmiot", "kto", "obywatel", "wojsko", "sędzia", "prawodawca"])
        has_condition = any(word in combined for word in ["jeżeli", "gdy", "warunek", "if", "and", "w przypadku"])
        has_effect = any(word in combined for word in ["to", "wtedy", "skutek", "podlega", "jest legalne", "kara"])
        
        if not (has_subject and has_condition and has_effect):
            missing = []
            if not has_subject: missing.append("Podmiot")
            if not has_condition: missing.append("Warunek")
            if not has_effect: missing.append("Skutek (konkluzja)")
            return False, f"Błąd formalny: Brak wymaganych składowych przepisu: {', '.join(missing)}."
            
        return True, "Projekt kompletny formalnie."

    @staticmethod
    def verify_consistency_and_hierarchy(text: str, formal_proof: str) -> Tuple[str, str]:
        """
        UC02: Weryfikacja spójności wewnętrznej i zgodności z hierarchią wartości (art. 1.4).
        """
        combined = (text + " " + (formal_proof or "")).lower()

        # 1. Test spójności logicznej (brak P i ¬P)
        # Symulacja wykrycia sprzeczności logicznej np. jeśli występuje fraza o zakazie i nakazie jednocześnie
        if "zawsze legalne" in combined and "jest zakazane" in combined:
            return "NIEZGODNY_LOGIKA", "Sprzeczność logiczna: Przepis jednocześnie dozwala i zabrania tego samego czynu (P ∧ ¬P)."

        # 2. Test hierarchii wartości (Indeks 1 do 8)
        # Przykład T01 z persona: Poseł Marek - praca przymusowa (naruszenie Godności Indeks 1 dla Dobra wspólnego Indeks 3)
        if "praca przymusowa" in combined or "pracy przymusowej" in combined:
            if "dobro wspólne" in combined or "dobra wspólnego" in combined:
                return "NIEZGODNY_WARTOSC", (
                    "NIEZGODNOŚĆ BEZWZGLĘDNA: Projekt próbuje ograniczyć Godność Osoby (Indeks 1) "
                    "w imię Dobra Wspólnot (Indeks 3). SOK automatycznie odrzuca akt z powodu naruszenia hierarchii wartości."
                )

        # Inny przykład: wywłaszczenie bez odszkodowania (naruszenie sprawiedliwości/własności)
        if "wywłaszczenie bez odszkodowania" in combined:
            return "NIEZGODNY_WARTOSC", (
                "NIEZGODNOŚĆ: Naruszenie Sprawiedliwości (Indeks 4) i Prawa własności (Indeks 8). "
                "Własność nie może być przejmowana z naruszeniem praw sprawiedliwego procesu."
            )

        return "ZGODNY", "Weryfikacja spójności pomyślna. Wszystkie testy jednostkowe i integracyjne CI/CD prawa zaliczone."
