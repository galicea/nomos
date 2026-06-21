"""
lt_engine.py – Silnik semantyczny

funkcje
  - Trwały model bazy (SQLAlchemy ORM) dla pola semantycznego
  - Odczyt SemanticMemory z trwałej bazy
  - Zapis stanu RAM → trwała baza na żądanie
  - Procedurę zasilającą pole semantyczne z tabeli Question
  - Generator promptu dla LLM
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional
from models.lt import *

from sqlalchemy import select
from sqlalchemy.orm import (
    DeclarativeBase, Session
)

# ---------------------------------------------------------------------------
# Stałe
# ---------------------------------------------------------------------------

DECAY_RATE           = 0.2   # zostawione dla kompatybilności (nieużywane w decay GlobalContext)
DECAY_COEFFICIENT    = 0.8   # δ ∈ (0,1) – współczynnik zanikania wykładniczego
ACTIVATION_THRESHOLD = 0.1
SPREAD_FACTOR        = 0.5

NODE_WORD               = 1
NODE_PHRASE_ARCHETYPE   = 2
NODE_SEMANTIC_ARCHETYPE = 3
NODE_PREDICATE_ARCHETYPE = 4


# ===========================================================================
# ORM – TRWAŁA BAZA DANYCH
# ===========================================================================
# zaimplementowana w models.lt

# ===========================================================================
# Dataclassy in-memory
# ===========================================================================

@dataclass
class Node:
    id:    int
    name:  str
    kind:  int
    fuzzy: float = 1.0


@dataclass
class Edge:
    target_id: int
    weight:    float


# ===========================================================================
# SemanticMemory – zarządzanie grafem (RAM + DB)
# ===========================================================================
class SemanticMemory:
    """
    Ładuje pole semantyczne z trwałej bazy SQLAlchemy do cache RAM.
    Oferuje metody zapisu z RAM → DB.
    """

    def __init__(self, session: Session):
        self.session = session
        self._nodes_cache: Dict[str, Node]         = {}
        self._edges_cache: Dict[int, List[Edge]]   = defaultdict(list)
        self._id_map:      Dict[int, str]           = {}
        self._load_cache()

    # --- Ładowanie cache ---------------------------------------------------

    def _load_cache(self):
        """Ładuje węzły i krawędzie z trwałej bazy do RAM."""
        print("[CACHE] Ładowanie pola semantycznego z bazy...")
        for node in self.session.scalars(select(SemanticNode)):
            n = Node(id=node.id, name=node.name, kind=node.kind, fuzzy=node.fuzzy or 1.0)
            self._nodes_cache[n.name] = n
            self._id_map[n.id] = n.name

        for edge in self.session.scalars(select(SemanticEdge)):
            self._edges_cache[edge.source_id].append(Edge(target_id=edge.target_id, weight=edge.weight))

        print(f"[CACHE] Załadowano {len(self._nodes_cache)} węzłów, "
              f"{sum(len(v) for v in self._edges_cache.values())} krawędzi.")

    # --- Dostęp -----------------------------------------------------------

    def get_node(self, name: str) -> Optional[Node]:
        return self._nodes_cache.get(name)

    def get_node_by_id(self, nid: int) -> Optional[Node]:
        name = self._id_map.get(nid)
        return self._nodes_cache.get(name) if name else None

    def get_neighbors(self, node_id: int) -> List[Edge]:
        return self._edges_cache.get(node_id, [])

    # --- Modyfikacja RAM ---------------------------------------------------

    def add_node(self, name: str, kind: int, fuzzy: float = 1.0) -> Node:
        """Dodaje węzeł do cache (bez zapisu do DB – użyj flush_to_db)."""
        if name in self._nodes_cache:
            return self._nodes_cache[name]
        # Tymczasowe ujemne id (zostanie nadpisane po flushu)
        tmp_id = -(len(self._nodes_cache) + 1)
        node = Node(id=tmp_id, name=name, kind=kind, fuzzy=fuzzy)
        self._nodes_cache[name] = node
        self._id_map[tmp_id] = name
        return node

    def add_edge(self, source_name: str, target_name: str, weight: float):
        """Dodaje krawędź do cache."""
        src = self._nodes_cache.get(source_name)
        tgt = self._nodes_cache.get(target_name)
        if src and tgt:
            existing = [e for e in self._edges_cache[src.id] if e.target_id == tgt.id]
            if not existing:
                self._edges_cache[src.id].append(Edge(target_id=tgt.id, weight=weight))

    # --- Zapis RAM → trwała baza ------------------------------------------

    def flush_to_db(self):
        """
        Zapisuje aktualny stan cache RAM do trwałej bazy danych.
        Wywołuj na żądanie (np. po zasileniu z Question).
        """
        print("[DB] Zapisywanie pola semantycznego do bazy...")

        # 1. Upsert węzłów
        existing_names = {
            row.name: row for row in self.session.scalars(select(SemanticNode))
        }
        name_to_db_id: Dict[str, int] = {}

        for name, node in self._nodes_cache.items():
            if name in existing_names:
                db_node = existing_names[name]
                db_node.kind  = node.kind
                db_node.fuzzy = node.fuzzy
            else:
                db_node = SemanticNode(name=name, kind=node.kind, fuzzy=node.fuzzy)
                self.session.add(db_node)
                self.session.flush()  # uzyskaj id

            name_to_db_id[name] = db_node.id

        self.session.flush()

        # 2. Upsert krawędzi (na podstawie aktualnych id DB)
        existing_edges: set[tuple[int, int]] = {
            (e.source_id, e.target_id)
            for e in self.session.scalars(select(SemanticEdge))
        }

        for cache_source_id, edges in self._edges_cache.items():
            source_name = self._id_map.get(cache_source_id)
            if not source_name:
                continue
            db_source_id = name_to_db_id.get(source_name)
            if db_source_id is None:
                continue

            for edge in edges:
                target_name = self._id_map.get(edge.target_id)
                if not target_name:
                    continue
                db_target_id = name_to_db_id.get(target_name)
                if db_target_id is None:
                    continue

                if (db_source_id, db_target_id) not in existing_edges:
                    self.session.add(SemanticEdge(
                        source_id=db_source_id,
                        target_id=db_target_id,
                        weight=edge.weight,
                    ))
                    existing_edges.add((db_source_id, db_target_id))

        self.session.commit()

        # 3. Przeładuj cache (pobierz prawdziwe id z DB)
        self._nodes_cache.clear()
        self._edges_cache.clear()
        self._id_map.clear()
        self._load_cache()

        print("[DB] Zapis zakończony.")

class SemanticMemory_bak:
    """
    Ładuje pole semantyczne z trwałej bazy SQLAlchemy do cache RAM.
    Oferuje metody zapisu z RAM → DB.
    """

    def __init__(self, session: Session):
        self.session = session
        self._nodes_cache: Dict[str, Node]         = {}
        self._edges_cache: Dict[int, List[Edge]]   = defaultdict(list)
        self._id_map:      Dict[int, str]           = {}
        self._load_cache()

    # --- Ładowanie cache ---------------------------------------------------

    def _load_cache(self):
        """Ładuje węzły i krawędzie z trwałej bazy do RAM."""
        print("[CACHE] Ładowanie pola semantycznego z bazy...")
        for node in self.session.scalars(select(SemanticNode)):
            n = Node(id=node.id, name=node.name, kind=node.kind, fuzzy=node.fuzzy or 1.0)
            self._nodes_cache[n.name] = n
            self._id_map[n.id] = n.name

        for edge in self.session.scalars(select(SemanticEdge)):
            self._edges_cache[edge.source_id].append(Edge(target_id=edge.target_id, weight=edge.weight))

        print(f"[CACHE] Załadowano {len(self._nodes_cache)} węzłów, "
              f"{sum(len(v) for v in self._edges_cache.values())} krawędzi.")

    # --- Dostęp -----------------------------------------------------------

    def get_node(self, name: str) -> Optional[Node]:
        return self._nodes_cache.get(name)

    def get_node_by_id(self, nid: int) -> Optional[Node]:
        name = self._id_map.get(nid)
        return self._nodes_cache.get(name) if name else None

    def get_neighbors(self, node_id: int) -> List[Edge]:
        return self._edges_cache.get(node_id, [])

    # --- Modyfikacja RAM ---------------------------------------------------

    def add_node(self, name: str, kind: int, fuzzy: float = 1.0) -> Node:
        """Dodaje węzeł do cache (bez zapisu do DB – użyj flush_to_db)."""
        if name in self._nodes_cache:
            return self._nodes_cache[name]
        # Tymczasowe ujemne id (zostanie nadpisane po flushu)
        tmp_id = -(len(self._nodes_cache) + 1)
        node = Node(id=tmp_id, name=name, kind=kind, fuzzy=fuzzy)
        self._nodes_cache[name] = node
        self._id_map[tmp_id] = name
        return node

    def add_edge(self, source_name: str, target_name: str, weight: float):
        """Dodaje krawędź do cache."""
        src = self._nodes_cache.get(source_name)
        tgt = self._nodes_cache.get(target_name)
        if src and tgt:
            existing = [e for e in self._edges_cache[src.id] if e.target_id == tgt.id]
            if not existing:
                self._edges_cache[src.id].append(Edge(target_id=tgt.id, weight=weight))

    # --- Zapis RAM → trwała baza ------------------------------------------

    def flush_to_db(self):
        """
        Zapisuje aktualny stan cache RAM do trwałej bazy danych.
        Wywołuj na żądanie (np. po zasileniu z Question).
        """
        print("[DB] Zapisywanie pola semantycznego do bazy...")

        # 1. Upsert węzłów
        existing_names = {
            row.name: row for row in self.session.scalars(select(SemanticNode))
        }
        name_to_db_id: Dict[str, int] = {}

        for name, node in self._nodes_cache.items():
            if name in existing_names:
                db_node = existing_names[name]
                db_node.kind  = node.kind
                db_node.fuzzy = node.fuzzy
            else:
                db_node = SemanticNode(name=name, kind=node.kind, fuzzy=node.fuzzy)
                self.session.add(db_node)
                self.session.flush()  # uzyskaj id

            name_to_db_id[name] = db_node.id

        self.session.flush()

        # 2. Upsert krawędzi (na podstawie aktualnych id DB)
        existing_edges: set[tuple[int, int]] = {
            (e.source_id, e.target_id)
            for e in self.session.scalars(select(SemanticEdge))
        }

        for cache_source_id, edges in self._edges_cache.items():
            source_name = self._id_map.get(cache_source_id)
            if not source_name:
                continue
            db_source_id = name_to_db_id.get(source_name)
            if db_source_id is None:
                continue

            for edge in edges:
                target_name = self._id_map.get(edge.target_id)
                if not target_name:
                    continue
                db_target_id = name_to_db_id.get(target_name)
                if db_target_id is None:
                    continue

                if (db_source_id, db_target_id) not in existing_edges:
                    self.session.add(SemanticEdge(
                        source_id=db_source_id,
                        target_id=db_target_id,
                        weight=edge.weight,
                    ))
                    existing_edges.add((db_source_id, db_target_id))

        self.session.commit()

        # 3. Przeładuj cache (pobierz prawdziwe id z DB)
        self._nodes_cache.clear()
        self._edges_cache.clear()
        self._id_map.clear()
        self._load_cache()

        print("[DB] Zapis zakończony.")


# ===========================================================================
# GlobalContext – tło semantyczne
# ===========================================================================
class GlobalContext:
    def __init__(self):
        self.background_activation: Dict[int, float] = defaultdict(float)
        self.lock = threading.Lock()

    def get_background(self) -> Dict[int, float]:
        with self.lock:
            return self.background_activation.copy()

    def merge_activations(self, new_activations: Dict[int, float]):
        """
        Scala lokalne aktywacje z tlem semantycznym.

        Tlo traktujemy jako mu(t) – przed scaleniem stosujemy jeden krok
        zanikania (czlon delta), a nastepnie dodajemy nowe pobudzenia jako
        boost (czlon boost_i).  Pozwala to na spojny model miedzy sesjami:
            background_i = background_i * delta + new_i
        """
        with self.lock:
            # Najpierw zastosuj zanikanie do istniejacego tla
            for nid in list(self.background_activation):
                self.background_activation[nid] *= DECAY_COEFFICIENT

            # Dodaj nowe pobudzenia jako boost
            for nid, val in new_activations.items():
                self.background_activation[nid] = min(
                    self.background_activation.get(nid, 0.0) + val,
                    2.0
                )

            # Wyczysc wezly ponizej progu
            to_remove = [k for k, v in self.background_activation.items()
                         if v < ACTIVATION_THRESHOLD]
            for k in to_remove:
                del self.background_activation[k]

    def decay(self):
        """
        Zanikanie wykładnicze zgodnie z modelem:
            mu_i(t+1) = mu_i(t) * delta
        (człon propagacji i boost są zerowe w tej fazie – brak nowego wejścia).
        """
        with self.lock:
            to_remove = [k for k, v in self.background_activation.items()
                         if v * DECAY_COEFFICIENT < ACTIVATION_THRESHOLD]
            for k in to_remove:
                del self.background_activation[k]
            for k in self.background_activation:
                self.background_activation[k] *= DECAY_COEFFICIENT
            if to_remove:
                print(f"[CZAS] Zapomniano {len(to_remove)} elementów tła.")


class GlobalContext_bak:
    def __init__(self):
        self.background_activation: Dict[int, float] = defaultdict(float)
        self.lock = threading.Lock()

    def get_background(self) -> Dict[int, float]:
        with self.lock:
            return self.background_activation.copy()

    def merge_activations(self, new_activations: Dict[int, float]):
        """
        Scala lokalne aktywacje z tlem semantycznym.

        Tlo traktujemy jako mu(t) – przed scaleniem stosujemy jeden krok
        zanikania (czlon delta), a nastepnie dodajemy nowe pobudzenia jako
        boost (czlon boost_i).  Pozwala to na spojny model miedzy sesjami:
            background_i = background_i * delta + new_i
        """
        with self.lock:
            # Najpierw zastosuj zanikanie do istniejacego tla
            for nid in list(self.background_activation):
                self.background_activation[nid] *= DECAY_COEFFICIENT

            # Dodaj nowe pobudzenia jako boost
            for nid, val in new_activations.items():
                self.background_activation[nid] = min(
                    self.background_activation.get(nid, 0.0) + val,
                    2.0
                )

            # Wyczysc wezly ponizej progu
            to_remove = [k for k, v in self.background_activation.items()
                         if v < ACTIVATION_THRESHOLD]
            for k in to_remove:
                del self.background_activation[k]

    def decay(self):
        """
        Zanikanie wykładnicze zgodnie z modelem:
            mu_i(t+1) = mu_i(t) * delta
        (człon propagacji i boost są zerowe w tej fazie – brak nowego wejścia).
        """
        with self.lock:
            to_remove = [k for k, v in self.background_activation.items()
                         if v * DECAY_COEFFICIENT < ACTIVATION_THRESHOLD]
            for k in to_remove:
                del self.background_activation[k]
            for k in self.background_activation:
                self.background_activation[k] *= DECAY_COEFFICIENT
            if to_remove:
                print(f"[CZAS] Zapomniano {len(to_remove)} elementów tła.")


# ===========================================================================
# QuestionSeeder – zasilanie pola semantycznego z tabeli Question
# ===========================================================================
class QuestionSeeder:
    """
    Przetwarza wiersze z tabeli Question i zasila pole semantyczne:
      - Dodaje tokeny jako węzły NODE_WORD (jeśli nie istnieją)
      - Tworzy węzeł NODE_PHRASE_ARCHETYPE dla każdego pytania
      - Łączy tokeny z archetypem frazy
      - Łączy archetyp frazy z predykatami przez QuestionPredicateMapping
    """

    WORD_TO_PHRASE_WEIGHT      = 0.8
    PHRASE_TO_PREDICATE_WEIGHT = 0.9

    def __init__(self, memory: SemanticMemory, session: Session):
        self.memory  = memory
        self.session = session

    def seed_all(self):
        """Przetwarza wszystkie pytania z bazy."""
        questions = self.session.scalars(select(Question)).all()
        print(f"[SEED] Przetwarzanie {len(questions)} pytań...")
        for q in questions:
            self._seed_question(q)
        print("[SEED] Gotowe. Wywołaj memory.flush_to_db() aby zapisać do bazy.")

    def seed_one(self, question_id: int):
        """Przetwarza pojedyncze pytanie."""
        q = self.session.get(Question, question_id)
        if q is None:
            raise ValueError(f"Pytanie {question_id} nie istnieje.")
        self._seed_question(q)

    def _seed_question(self, q: Question):
        tokens = q.question_text.lower().split()
        archetype_name = f"PHRASE_Q{q.question_id}"

        # 1. Węzeł archetypu frazy
        arch_node = self.memory.add_node(archetype_name, NODE_PHRASE_ARCHETYPE)

        # 2. Tokeny → węzły słów + krawędź słowo→archetyp
        for token in tokens:
            word_node = self.memory.add_node(token, NODE_WORD)
            self.memory.add_edge(token, archetype_name, self.WORD_TO_PHRASE_WEIGHT)

        # 3. Powiązanie archetypu frazy z predykatami
        mappings = (
            self.session.scalars(
                select(QuestionPredicateMapping)
                .where(QuestionPredicateMapping.question_id == q.question_id)
            ).all()
        )
        for mapping in mappings:
            pred_name = f"PRED_{mapping.predicate_id}"
            pred_node = self.memory.add_node(pred_name, NODE_PREDICATE_ARCHETYPE)
            self.memory.add_edge(archetype_name, pred_name, self.PHRASE_TO_PREDICATE_WEIGHT)

        print(f"[SEED] Q{q.question_id}: '{q.question_text}' → "
              f"{len(tokens)} tokenów, {len(mappings)} predykatów")

class QuestionSeeder_bak:
    """
    Przetwarza wiersze z tabeli Question i zasila pole semantyczne:
      - Dodaje tokeny jako węzły NODE_WORD (jeśli nie istnieją)
      - Tworzy węzeł NODE_PHRASE_ARCHETYPE dla każdego pytania
      - Łączy tokeny z archetypem frazy
      - Łączy archetyp frazy z predykatami przez QuestionPredicateMapping
    """

    WORD_TO_PHRASE_WEIGHT      = 0.8
    PHRASE_TO_PREDICATE_WEIGHT = 0.9

    def __init__(self, memory: SemanticMemory, session: Session):
        self.memory  = memory
        self.session = session

    def seed_all(self):
        """Przetwarza wszystkie pytania z bazy."""
        questions = self.session.scalars(select(Question)).all()
        print(f"[SEED] Przetwarzanie {len(questions)} pytań...")
        for q in questions:
            self._seed_question(q)
        print("[SEED] Gotowe. Wywołaj memory.flush_to_db() aby zapisać do bazy.")

    def seed_one(self, question_id: int):
        """Przetwarza pojedyncze pytanie."""
        q = self.session.get(Question, question_id)
        if q is None:
            raise ValueError(f"Pytanie {question_id} nie istnieje.")
        self._seed_question(q)

    def _seed_question(self, q: Question):
        tokens = q.question_text.lower().split()
        archetype_name = f"PHRASE_Q{q.question_id}"

        # 1. Węzeł archetypu frazy
        arch_node = self.memory.add_node(archetype_name, NODE_PHRASE_ARCHETYPE)

        # 2. Tokeny → węzły słów + krawędź słowo→archetyp
        for token in tokens:
            word_node = self.memory.add_node(token, NODE_WORD)
            self.memory.add_edge(token, archetype_name, self.WORD_TO_PHRASE_WEIGHT)

        # 3. Powiązanie archetypu frazy z predykatami
        mappings = (
            self.session.scalars(
                select(QuestionPredicateMapping)
                .where(QuestionPredicateMapping.question_id == q.question_id)
            ).all()
        )
        for mapping in mappings:
            pred_name = f"PRED_{mapping.predicate_id}"
            pred_node = self.memory.add_node(pred_name, NODE_PREDICATE_ARCHETYPE)
            self.memory.add_edge(archetype_name, pred_name, self.PHRASE_TO_PREDICATE_WEIGHT)

        print(f"[SEED] Q{q.question_id}: '{q.question_text}' → "
              f"{len(tokens)} tokenów, {len(mappings)} predykatów")


# ===========================================================================
# CognitiveProcessor – silnik wnioskowania
# ===========================================================================
class CognitiveProcessor:
    """
    Przetwarza pytanie użytkownika przez spreading activation,
    zwraca dopasowane archetypy i predykaty.
    """

    def __init__(self, memory: SemanticMemory, global_ctx: GlobalContext):
        self.memory          = memory
        self.global_ctx      = global_ctx
        self.local_activations: Dict[int, float] = global_ctx.get_background()

    def process(self, text: str) -> Dict:
        tokens = text.lower().split()

        # --- Krok 1: Pobudzenie bezpośrednie ---------------------------------
        input_nodes: List[Node] = []
        for token in tokens:
            node = self.memory.get_node(token)
            if node:
                input_nodes.append(node)
                cur = self.local_activations.get(node.id, 0.0)
                self.local_activations[node.id] = min(cur + 1.0, 2.0)

        # --- Krok 2: Propagacja (2 kroki) ------------------------------------
        for _ in range(2):
            snapshot = self.local_activations.copy()
            for source_id, activation in snapshot.items():
                if activation < ACTIVATION_THRESHOLD:
                    continue
                for edge in self.memory.get_neighbors(source_id):
                    transfer = activation * edge.weight * SPREAD_FACTOR
                    prev = self.local_activations.get(edge.target_id, 0.0)
                    self.local_activations[edge.target_id] = prev + transfer

        # --- Krok 3: Wybór archetypów ----------------------------------------
        phrase_candidates:    List[tuple[Node, float]] = []
        semantic_candidates:  List[tuple[Node, float]] = []
        predicate_candidates: List[tuple[Node, float]] = []

        for nid, activation in self.local_activations.items():
            node = self.memory.get_node_by_id(nid)
            if not node:
                continue
            if node.kind == NODE_PHRASE_ARCHETYPE:
                phrase_candidates.append((node, activation))
            elif node.kind == NODE_SEMANTIC_ARCHETYPE:
                semantic_candidates.append((node, activation))
            elif node.kind == NODE_PREDICATE_ARCHETYPE:
                predicate_candidates.append((node, activation))

        for lst in (phrase_candidates, semantic_candidates, predicate_candidates):
            lst.sort(key=lambda x: x[1], reverse=True)

        # --- Krok 4: Aktualizacja tła ----------------------------------------
        self.global_ctx.merge_activations(self.local_activations)

        return {
            "input_tokens":        [n.name for n in input_nodes],
            "phrase_archetypes":   [(n.name, round(s, 3)) for n, s in phrase_candidates[:5]],
            "semantic_archetypes": [(n.name, round(s, 3)) for n, s in semantic_candidates[:3]],
            "predicate_nodes":     [(n.name, round(s, 3)) for n, s in predicate_candidates[:5]],
            "top_phrase":          phrase_candidates[0]    if phrase_candidates    else None,
            "top_semantic":        semantic_candidates[0]  if semantic_candidates  else None,
            "top_predicates":      predicate_candidates[:3],
        }


class CognitiveProcessor_new:
    """
    Przetwarza pytanie użytkownika przez spreading activation,
    zwraca dopasowane archetypy i predykaty.
    """

    def __init__(self, memory: SemanticMemory, global_ctx: GlobalContext):
        self.memory          = memory
        self.global_ctx      = global_ctx
        self.local_activations: Dict[int, float] = global_ctx.get_background()

    def process(self, text: str,
                boost: Optional[Dict[int, float]] = None,
                propagation_steps: int = 2) -> Dict:
        """
        Przetwarza pytanie użytkownika przez spreading activation.

        Model aktualizacji (jeden krok propagacji):
            mu_i(t+1) = mu_i(t) * delta
                        + sum_{j in N_in(i)} w_ji * mu_j(t)
                        + boost_i(t)

        gdzie:
          delta  = DECAY_COEFFICIENT   -- zanikanie resztkowe miedzy krokami
          w_ji   = waga krawedzi j->i  -- sila propagacji
          boost  = zewnetrzny sygnal top-down (priming z brakujacych argumentow)
        """
        tokens = text.lower().split()
        boost = boost or {}

        # --- Krok 1: Pobudzenie bezposrednie (bottom-up) ---------------------
        # Slowa uzytkownika ustawiaja boost_i = 1.0 dla dopasowanych wezlow.
        input_nodes: List[Node] = []
        for token in tokens:
            node = self.memory.get_node(token)
            if node:
                input_nodes.append(node)
                boost[node.id] = min(boost.get(node.id, 0.0) + 1.0, 1.0)

        # --- Krok 2: Iteracyjna propagacja z modelem matematycznym -----------
        # mu_i(t+1) = mu_i(t) * delta + sum_j(w_ji * mu_j(t)) + boost_i(t)
        for step in range(propagation_steps):
            # boost dziala tylko w pierwszym kroku (bezposrednie wejscie)
            step_boost = boost if step == 0 else {}

            mu_prev = self.local_activations.copy()

            # Zbierz sume propagacji dla kazdego wezla docelowego
            propagation_sum: Dict[int, float] = defaultdict(float)
            for source_id, mu_j in mu_prev.items():
                if mu_j < ACTIVATION_THRESHOLD:
                    continue
                for edge in self.memory.get_neighbors(source_id):
                    propagation_sum[edge.target_id] += edge.weight * mu_j

            # Wyznacz nowy zbior aktywnych wezlow (unia starych i docelowych)
            all_nodes = (set(mu_prev.keys())
                         | set(propagation_sum.keys())
                         | set(step_boost.keys()))

            new_activations: Dict[int, float] = {}
            for nid in all_nodes:
                mu_t   = mu_prev.get(nid, 0.0)
                prop   = propagation_sum.get(nid, 0.0)
                b      = step_boost.get(nid, 0.0)
                mu_new = mu_t * DECAY_COEFFICIENT + prop + b
                if mu_new >= ACTIVATION_THRESHOLD:
                    new_activations[nid] = min(mu_new, 2.0)   # gorne ograniczenie

            self.local_activations = new_activations

        # --- Krok 3: Wybor archetypow ----------------------------------------
        phrase_candidates:    List[tuple[Node, float]] = []
        semantic_candidates:  List[tuple[Node, float]] = []
        predicate_candidates: List[tuple[Node, float]] = []

        for nid, activation in self.local_activations.items():
            node = self.memory.get_node_by_id(nid)
            if not node:
                continue
            if node.kind == NODE_PHRASE_ARCHETYPE:
                phrase_candidates.append((node, activation))
            elif node.kind == NODE_SEMANTIC_ARCHETYPE:
                semantic_candidates.append((node, activation))
            elif node.kind == NODE_PREDICATE_ARCHETYPE:
                predicate_candidates.append((node, activation))

        for lst in (phrase_candidates, semantic_candidates, predicate_candidates):
            lst.sort(key=lambda x: x[1], reverse=True)

        # --- Krok 4: Aktualizacja tła ----------------------------------------
        self.global_ctx.merge_activations(self.local_activations)

        return {
            "input_tokens":        [n.name for n in input_nodes],
            "phrase_archetypes":   [(n.name, round(s, 3)) for n, s in phrase_candidates[:5]],
            "semantic_archetypes": [(n.name, round(s, 3)) for n, s in semantic_candidates[:3]],
            "predicate_nodes":     [(n.name, round(s, 3)) for n, s in predicate_candidates[:5]],
            "top_phrase":          phrase_candidates[0]    if phrase_candidates    else None,
            "top_semantic":        semantic_candidates[0]  if semantic_candidates  else None,
            "top_predicates":      predicate_candidates[:3],
        }


# ===========================================================================
# PromptBuilder – generator promptu dla LLM
# ===========================================================================

class PromptBuilder:
    """
    Buduje prompt dla LLM na podstawie:
      - Oryginalnego pytania użytkownika
      - Wyników CognitiveProcessor (dopasowane predykaty)
      - Danych z tabeli Predicate (logic_expression + short_answer)
    """

    SYSTEM_PROMPT = (
        "Jesteś kognitywnym asystentem biznesowym firmy Transmem. Twoim zadaniem jest "
        "odpowiadanie na pytania klientów w sposób profesjonalny, konkretny i naturalny.\n\n"

        "ZASADY INTERPRETACJI KONTEKSTU:\n"
        "1. Kontekst otrzymujesz w postaci wytypowanych przez algorytm predykatów oraz ich opisów (format: P_ID: PREDYKAT | Opis).\n"
        "2. Twoja odpowiedź musi być płynną syntezą językową dostarczonych opisów. Nigdy nie wyświetlaj użytkownikowi surowego kodu predykatów (np. 'OFFER(TRANSMEM...)').\n"
        "3. Opieraj się WYŁĄCZNIE na dostarczonych faktach. Zakaz uogólniania poza kontekst i zmyślania informacji (halucynacji).\n\n"

        "OBSŁUGA BRAKU INFORMACJI:\n"
        "- Jeśli dostarczone predykaty nie zawierają odpowiedzi na pytanie klienta, napisz wprost: "
        "'Nie posiadam w tej chwili szczegółowych danych na ten temat.'\n"
        "- W tym samym zdaniu zaproponuj rozwiązanie: 'Zostaw swój adres e-mail, a nasz zespół chętnie przygotuje dla Ciebie dedykowaną odpowiedź.'\n\n"

        "ZASADY FORMATOWANIA I LINKÓW:\n"
        "- ZACHOWANIE LINKÓW: W opisach predykatów mogą znajdować się linki Markdown [tekst](url). Masz absolutny obowiązek wpleść je dokładnie i nienaruszone w treść odpowiedzi (np. jako naturalny odnośnik typu: '...szczegóły znajdziesz w naszym [opisie Smart Data Streams](url)').\n"
        "- WIZUALNA PRZEJRZYSTOŚĆ: Stosuj formatowanie Markdown: **pogrubiaj** kluczowe terminy rynkowe/technologiczne, używaj list z myślnikami przy wyliczeniach.\n"
        "- JĘZYK: Odpowiadaj zwięźle, wyłącznie po polsku."
    )

    def __init__(self, session: Session):
        self.session = session

    def build(self, user_question: str, cognitive_result: Dict) -> Dict[str, str]:
        """
        Zwraca słownik z kluczami 'system' i 'user' gotowy do przekazania do LLM.
        """
        # Wyłuskaj identyfikatory predykatów z nazw węzłów ("PRED_<predicate_id>")
        pred_ids = []
        for node_name, _score in cognitive_result.get("predicate_nodes", []):
            if node_name.startswith("PRED_"):
                pred_ids.append(node_name[5:])  # usuń prefix

        # Pobierz predykaty z DB
        predicates: List[Predicate] = []
        if pred_ids:
            predicates = list(
                self.session.scalars(
                    select(Predicate).where(Predicate.predicate_id.in_(pred_ids))
                ).all()
            )

        # Zbuduj sekcję kontekstu
        context_lines: List[str] = []
        for pred in predicates:
            line = f"[{pred.predicate_id}]"
            if pred.category:
                line += f" ({pred.category})"
            line += f"\nLogika: {pred.logic_expression}"
            if pred.short_answer:
                line += f"\nOdpowiedź pomocnicza: {pred.short_answer}"
            context_lines.append(line)

        if context_lines:
            context_block = "\n\n".join(context_lines)
        else:
            context_block = "Brak dopasowanych predykatów."

        # Opcjonalnie: dołącz najlepszy archetyp semantyczny jako wskazówkę
        semantic_hint = ""
        if cognitive_result.get("top_semantic"):
            arch_node, score = cognitive_result["top_semantic"]
            semantic_hint = f"\nZidentyfikowany wzorzec semantyczny: {arch_node.name} (pewność: {score:.2f})"

        user_message = (
            f"Pytanie użytkownika: {user_question}"
            f"{semantic_hint}\n\n"
            f"Kontekst (predykaty):\n{context_block}"
        )

        return {
            "system": self.SYSTEM_PROMPT,
            "user":   user_message,
        }

    def format_for_display(self, prompt: Dict[str, str]) -> str:
        """Czytelna reprezentacja promptu (do debugowania / logowania)."""
        return (
            "=== SYSTEM ===\n"
            f"{prompt['system']}\n\n"
            "=== USER ===\n"
            f"{prompt['user']}"
        )


class PromptBuilder_bak:
    """
    Buduje prompt dla LLM na podstawie:
      - Oryginalnego pytania użytkownika
      - Wyników CognitiveProcessor (dopasowane predykaty)
      - Danych z tabeli Predicate (logic_expression + short_answer)
    """

    def __init__(self, session: Session):
        self.session = session

    def build(self, user_question: str, cognitive_result: Dict) -> Dict[str, str]:
        """
        Zwraca słownik z kluczami 'system' i 'user' gotowy do przekazania do LLM.
        """
        # Wyłuskaj identyfikatory predykatów z nazw węzłów ("PRED_<predicate_id>")
        pred_ids = []
        for node_name, _score in cognitive_result.get("predicate_nodes", []):
            if node_name.startswith("PRED_"):
                pred_ids.append(node_name[5:])  # usuń prefix

        # Pobierz predykaty z DB
        predicates: List[Predicate] = []
        if pred_ids:
            predicates = list(
                self.session.scalars(
                    select(Predicate).where(Predicate.predicate_id.in_(pred_ids))
                ).all()
            )

        # Zbuduj sekcję kontekstu
        context_lines: List[str] = []
        for pred in predicates:
            line = f"[{pred.predicate_id}]"
            if pred.category:
                line += f" ({pred.category})"
            line += f"\nLogika: {pred.logic_expression}"
            if pred.short_answer:
                line += f"\nOdpowiedź pomocnicza: {pred.short_answer}"
            context_lines.append(line)

        if context_lines:
            context_block = "\n\n".join(context_lines)
        else:
            context_block = "Brak dopasowanych predykatów."

        # Opcjonalnie: dołącz najlepszy archetyp semantyczny jako wskazówkę
        semantic_hint = ""
        if cognitive_result.get("top_semantic"):
            arch_node, score = cognitive_result["top_semantic"]
            semantic_hint = f"\nZidentyfikowany wzorzec semantyczny: {arch_node.name} (pewność: {score:.2f})"

        user_message = (
            f"Pytanie użytkownika: {user_question}"
            f"{semantic_hint}\n\n"
            f"Kontekst (predykaty):\n{context_block}"
        )

        return {
            "system": self.SYSTEM_PROMPT,
            "user":   user_message,
        }

    def format_for_display(self, prompt: Dict[str, str]) -> str:
        """Czytelna reprezentacja promptu (do debugowania / logowania)."""
        return (
            "=== SYSTEM ===\n"
            f"{prompt['system']}\n\n"
            "=== USER ===\n"
            f"{prompt['user']}"
        )


# ===========================================================================
# ChatbotPipeline – orkiestracja całego przepływu
# ===========================================================================

class ChatbotPipeline:
    """
    Łączy wszystkie komponenty w jeden przepływ:
      question_text → CognitiveProcessor → PromptBuilder → prompt dla LLM
    """

    def __init__(self, engine_url: str = "sqlite:///semantic.db"):
        """
        from sqlalchemy import create_engine
        engine = create_engine(engine_url, echo=False)
        Base.metadata.create_all(engine)

        self.session        = Session(engine)
        """
        self.memory         = SemanticMemory(self.session)
        self.global_ctx     = GlobalContext()
        self.seeder         = QuestionSeeder(self.memory, self.session)
        self.prompt_builder = PromptBuilder(self.session)

    def __init__(self, session: Session):
        self.session        = session
        self.memory         = SemanticMemory(self.session)
        self.global_ctx     = GlobalContext()
        self.seeder         = QuestionSeeder(self.memory, self.session)
        self.prompt_builder = PromptBuilder(self.session)

    # --- Zasilanie ----------------------------------------------------------

    def seed_from_questions(self, save: bool = True):
        """Zasila pole semantyczne ze wszystkich pytań w tabeli Question."""
        self.seeder.seed_all()
        if save:
            self.memory.flush_to_db()

    def save_memory(self):
        """Zapisuje bieżący stan RAM → DB na żądanie."""
        self.memory.flush_to_db()

    # --- Przetwarzanie pytania ----------------------------------------------

    def answer(self, user_question: str) -> Dict:
        """
        Główna metoda pipeline:
          1. Spreading activation
          2. Wybór archetypów i predykatów
          3. Budowanie promptu dla LLM
        Zwraca słownik z wynikami i gotowym promptem.
        """
        #processor_bak      = CognitiveProcessor(self.memory, self.global_ctx)
        #cognitive_bak      = processor_bak.process(user_question)
        #prompt_bak         = self.prompt_builder.build(user_question, cognitive_bak)
        processor  = CognitiveProcessor(self.memory, self.global_ctx)
        cognitive  = processor.process(user_question)
        prompt = self.prompt_builder.build(user_question, cognitive)

        return {
            "question":        user_question,
            "cognitive_result": cognitive,
            "llm_prompt":      prompt,
        }

    def get_prompt_text(self, user_question: str) -> str:
        """Skrócona ścieżka – zwraca gotowy tekst promptu."""
        result = self.answer(user_question)
        return self.prompt_builder.format_for_display(result["llm_prompt"])

    def close(self):
        self.session.close()


# ===========================================================================
# Demo / przykład użycia
# ===========================================================================

def demo():
    """
    Demonstracja pipeline z przykładowymi danymi.
    """
    from db.session import SessionLocal

    with SessionLocal() as session:
        # --- Dane przykładowe -----------------------------------------------
        if not session.scalars(select(Predicate)).first():
            p1 = Predicate(
                predicate_id="SHIPPING_TIME",
                category="logistyka",
                logic_expression="shipping_days IN (1, 2, 3)",
                short_answer="Standardowa dostawa trwa 2–3 dni robocze.",
            )
            p2 = Predicate(
                predicate_id="RETURN_POLICY",
                category="obsługa klienta",
                logic_expression="return_window_days >= 30",
                short_answer="Przyjmujemy zwroty w ciągu 30 dni od zakupu.",
            )
            p3 = Predicate(
                predicate_id="PAYMENT_METHODS",
                category="płatności",
                logic_expression="payment IN ('card', 'blik', 'transfer')",
                short_answer="Akceptujemy kartę, BLIK i przelew bankowy.",
            )
            session.add_all([p1, p2, p3])
            session.flush()

        q1 = Question(question_text="jak długo trwa dostawa", intent="logistics")
        q2 = Question(question_text="czy mogę zwrócić towar", intent="returns")
        q3 = Question(question_text="jakie są metody płatności", intent="payments")
        session.add_all([q1, q2, q3])
        session.flush()

        session.add(QuestionPredicateMapping(question_id=q1.question_id, predicate_id="SHIPPING_TIME"))
        session.add(QuestionPredicateMapping(question_id=q2.question_id, predicate_id="RETURN_POLICY"))
        session.add(QuestionPredicateMapping(question_id=q3.question_id, predicate_id="PAYMENT_METHODS"))
        session.commit()

# --- Pipeline -----------------------------------------------------------
        pipeline = ChatbotPipeline(session)

        print("=== Zasilanie pola semantycznego z pytań ===")
        pipeline.seed_from_questions(save=True)

        print("\n=== Przetwarzanie pytania użytkownika ===")
        test_questions = [
            "ile trwa dostawa",
            "chcę zwrócić zakup",
            "czym mogę zapłacić",
            "Mamy mnóstwo dokumentacji prawnej do analizy. Czy możecie to zautomatyzować?"
        ]

        for q in test_questions:
            print(f"\n{'='*60}")
            print(f"Pytanie: {q}")
            result = pipeline.answer(q)
            print(f"Dopasowane archetypy fraz: {result['cognitive_result']['phrase_archetypes']}")
            print(f"Dopasowane predykaty:      {result['cognitive_result']['predicate_nodes']}")
            print("\n--- Prompt dla LLM ---")
            print(pipeline.prompt_builder.format_for_display(result["llm_prompt"]))

        pipeline.close()

# ===========================================================================
# Executor - funkcje używane w systemie
# ===========================================================================

def eng_QuesteiosToSemanticField():
    from db.session import SessionLocal
    with SessionLocal() as session:
        pipeline = ChatbotPipeline(session)
        pipeline.seed_from_questions(save=True)

def eng_QuestionToPrompt(question : str):
    from db.session import SessionLocal
    with SessionLocal() as session:
        pipeline = ChatbotPipeline(session)
        result = pipeline.answer(question)
        # print(f"Dopasowane archetypy fraz: {result['cognitive_result']['phrase_archetypes']}")
        # print(f"Dopasowane predykaty:      {result['cognitive_result']['predicate_nodes']}")
        pipeline.close()
        return result["llm_prompt"]


if __name__ == "__main__":
#    demo()
    eng_QuesteiosToSemanticField()
    from db.session import SessionLocal
    with SessionLocal() as session:
        pass
    exit()
    #prompt1=eng_QuestionToPrompt('Czy mogę zainstalować waszego chatbota na swojej stronie?')
    prompt2 = eng_QuestionToPrompt('Jak wygląda Wasz model współpracy')
    from db.session import SessionLocal

    with SessionLocal() as session:
        pipeline = ChatbotPipeline(session)
        #print(pipeline.prompt_builder.format_for_display(prompt1))
        print(pipeline.prompt_builder.format_for_display(prompt2))