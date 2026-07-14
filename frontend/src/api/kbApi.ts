// frontend0/src/api/kbApi.ts
import axios from 'axios';
import { KBClause, KBClauseSimple, KBClauseListResponse, DbViewSimple, ViewColumnStructure } from '../types/kbTypes';

const API_URL = 'http://localhost:8000/kb';

export const kbApi = {
  fetchClauseList: () => axios.get<KBClauseSimple[]>(`${API_URL}/list`),
  fetchClauseById: (id: number) => axios.get<KBClause>(`${API_URL}/${id}`),
  createClause: (clause: Omit<KBClause, 'id'>) => axios.post<KBClause>(`${API_URL}`, clause),
  updateClause: (id: number, clause: Omit<KBClause, 'id'>) => axios.put<KBClause>(`${API_URL}/${id}`, clause),
  deleteClause: (id: number) => axios.delete(`${API_URL}/${id}`),
  fetchPaginatedClauses: (skip: number, limit: number) => 
    axios.get<KBClauseListResponse>(`${API_URL}?skip=${skip}&limit=${limit}`),
  fetchDbViewList: () => axios.get<DbViewSimple[]>(`${API_URL}/views/list`),
  fetchViewStructure: (viewName: string) => axios.get<ViewColumnStructure[]>(`${API_URL}/views/${viewName}/structure`),
  execClauseCsv: (id: number, params: Record<string, string>) => 
    axios.get(`${API_URL}/query/${id}`, { params, responseType: 'blob' }),
};
