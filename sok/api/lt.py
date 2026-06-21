# api.lt.py

from fastapi import APIRouter
from services.lt_engine import eng_QuestionToPrompt
import logging

from schemas.lt_schemas import QuestionPost
from .gemini import gemini_q

logger = logging.getLogger(__name__)


router = APIRouter(
  prefix="",  # Upewnij się, że ten prefix pasuje do głównego routera
  tags=["LT"]
)


# ==========================================
# ENDPOINTY DLA PREDYKATÓW
# ==========================================

@router.get("/query")
def get_query(query : str):
    prompt = eng_QuestionToPrompt(query)
    return gemini_q(query, prompt)


#           message: userInput,
#           conversation_history: messages.map((m) => ({
#             role: m.sender,
#             content: m.text,
#           })),

@router.post("/query")
def post_query(query : QuestionPost):
    prompt = eng_QuestionToPrompt(query.message)
    ret=gemini_q(query.message, prompt)
    ret['response']=ret['response']
    return ret



# Statyczny słownik — lista
OFERTY = {
    "help": "<b>Pomoc</b><br />",
    "doc":   "<b>Dokumentacja</b><br />",
}

@router.get("/link/{slug}")
def get_oferta(slug: str):
    tekst = OFERTY.get(slug, "Nie znaleziono oferty.")

    return {"response": tekst}