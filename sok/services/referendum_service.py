# backend0/services/referendum_service.py
from models.referendum import Referendum

class ReferendumService:
    @staticmethod
    def cast_vote(referendum: Referendum, option: str) -> Referendum:
        """
        Głosowanie na opcję A lub B.
        """
        if referendum.status != 'active':
            raise ValueError("Referendum jest już zamknięte.")

        if option.upper() == 'A':
            referendum.votes_a += 1
        elif option.upper() == 'B':
            referendum.votes_b += 1
        else:
            raise ValueError("Niepoprawna opcja głosowania. Wybierz 'A' lub 'B'.")

        return referendum

    @staticmethod
    def close_referendum(referendum: Referendum) -> Referendum:
        """
        Zamykanie referendum, weryfikacja frekwencji (frekwencja > 50% w makiecie).
        """
        if referendum.status != 'active':
            return referendum

        total_votes = referendum.votes_a + referendum.votes_b
        # Załóżmy na potrzeby demonstracji, że próg ważności (50% elektoratu) wynosi 10 głosów
        threshold = 10 
        
        if total_votes >= threshold:
            referendum.status = 'completed_valid'
        else:
            referendum.status = 'completed_invalid'

        return referendum
