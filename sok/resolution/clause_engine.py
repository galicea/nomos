# backend0/resolution/clause_engine.py
from typing import List, Dict, Any, Generator, Optional, Tuple
from schemas.kn_schemas import KBClause
from db.session import SessionLocal
from services.dbviews import ViewRepository

class UnifyingVariable:
    def __init__(self, value=None):
        self.value = value

    def unify(self, arg):
        if self.value is not None and self.value != arg:
            return False
        self.value = arg
        return True

    def set(self, arg):
        self.value = arg
        return True

    def __repr__(self):
        return f"Var({self.value})"

class KnowledgeEngine:
    def __init__(self):
        self.db_session = SessionLocal()
        self.view_repo = ViewRepository(self.db_session)
        self.clauses_by_id: Dict[int, KBClause] = {}
        self.clauses_by_ident: Dict[str, KBClause] = {}

    def close(self):
        self.db_session.close()

    def load_clauses(self, clauses: List[KBClause]):
        for clause in clauses:
            if clause.id is None:
                continue
            if clause.id not in self.clauses_by_id:
                self.clauses_by_id[clause.id] = clause
            if clause.cl_ident and clause.cl_ident not in self.clauses_by_ident:
                self.clauses_by_ident[clause.cl_ident] = clause

    def get_clause_by_id(self, clause_id: int) -> Optional[KBClause]:
        return self.clauses_by_id.get(clause_id)

    def get_clause_by_ident(self, cl_ident: str) -> Optional[KBClause]:
        return self.clauses_by_ident.get(cl_ident)

    def _execute_base(self, clause: KBClause, context: Dict[str, UnifyingVariable]) -> Generator[bool, None, None]:
        table_name = clause.cl_view_name
        if not table_name:
            return

        qbe_filter = {}
        output_vars = {}

        for param in clause.parameters:
            par_ident = param.par_ident
            if par_ident in context:
                var = context[par_ident]
                if var.value is not None:
                    qbe_filter[par_ident] = var.value
                else:
                    output_vars[par_ident] = var

        for row in self.view_repo.query_view(table_name, **qbe_filter):
            vars_set_in_this_iteration: List[Tuple[UnifyingVariable, Any]] = []
            for par_ident, var in output_vars.items():
                if par_ident in row:
                    vars_set_in_this_iteration.append((var, var.value))
                    var.set(row[par_ident])
            yield True
            for var, old_value in vars_set_in_this_iteration:
                var.set(old_value)

    def _execute_rule(self, clause: KBClause, parent_context: Dict[str, UnifyingVariable]) -> Generator[bool, None, None]:
        rule_context = parent_context
        parent_param_names = {p.par_ident for p in clause.parameters}

        for sub in clause.subs:
            for sub_par in sub.parameters:
                if sub_par.unify_par and sub_par.unify_par not in rule_context:
                    if sub_par.unify_par not in parent_param_names:
                        rule_context[sub_par.unify_par] = UnifyingVariable()

        def run_subs(sub_index: int) -> Generator[bool, None, None]:
            if sub_index == len(clause.subs):
                yield True
                return

            current_sub = clause.subs[sub_index]
            child_clause = self.get_clause_by_id(current_sub.sub_id)
            if not child_clause:
                return

            child_context: Dict[str, UnifyingVariable] = {}
            for sub_par in current_sub.parameters:
                child_par_ident = sub_par.par_ident
                if sub_par.unify_par and sub_par.unify_par in rule_context:
                    child_context[child_par_ident] = rule_context[sub_par.unify_par]
                elif sub_par.value:
                    child_context[child_par_ident] = UnifyingVariable(sub_par.value)
                elif sub_par.par_ident in rule_context:
                    child_context[child_par_ident] = rule_context[sub_par.par_ident]

            if child_clause.cl_category == 'baza':
                sub_generator = self._execute_base(child_clause, child_context)
            else:
                sub_generator = self._execute_rule(child_clause, child_context)

            for _ in sub_generator:
                yield from run_subs(sub_index + 1)

        yield from run_subs(0)

    def run(self, clause_ident: str = '', clause_id: int = 0, **kwargs: Any) -> Generator[Dict[str, Any], None, None]:
        if clause_id > 0:
            main_clause = self.get_clause_by_id(clause_id)
        else:
            main_clause = self.get_clause_by_ident(clause_ident)
        if not main_clause:
            raise ValueError(f"Nie znaleziono klauzuli: '{clause_ident or clause_id}'")

        parent_context: Dict[str, UnifyingVariable] = {}
        for param in main_clause.parameters:
            par_ident = param.par_ident
            parent_context[par_ident] = UnifyingVariable(kwargs.get(par_ident))

        if main_clause.cl_category == 'definicja':
            executor = self._execute_rule(main_clause, parent_context)
        elif main_clause.cl_category == 'baza':
            executor = self._execute_base(main_clause, parent_context)
        else:
            raise TypeError(f"Nieznana kategoria: {main_clause.cl_category}")

        for _ in executor:
            result = {k: v.value for k, v in parent_context.items() if v.value is not None}
            if result:
                yield result
