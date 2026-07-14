// frontend0/src/types/kbTypes.ts

export interface KBClausePar {
  id?: number;
  clause_id?: number;
  par_ident: string;
  par_description?: string;
}

export interface KBClauseSubPar {
  id?: number;
  clause_sub_id?: number;
  par_ident: string;
  unify_cl?: string;
  unify_par?: string;
  active?: boolean;
  cut?: boolean;
  value?: string;
}

export interface KBClauseSub {
  id?: number;
  clause_id?: number;
  sub_id: number;
  order: number;
  parameters: KBClauseSubPar[];
}

export interface KBClause {
  id?: number;
  cl_ident: string;
  cl_description?: string;
  cl_category: 'definicja' | 'baza';
  cl_view_name?: string | null;
  cl_net?: string | null;
  parameters: KBClausePar[];
  subs: KBClauseSub[];
}

export interface KBClauseSimple {
  id: number;
  cl_ident: string;
  cl_description?: string;
}

export interface KBClauseListItem extends KBClause {
  id: number;
}

export interface KBClauseListResponse {
  total_count: number;
  items: KBClauseListItem[];
}

export interface DbViewSimple {
  view_name: string;
}

export interface ViewColumnStructure {
  column_name: string;
  data_type: string;
}
