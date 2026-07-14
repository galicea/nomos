import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Plus, Edit, Trash2, Play, AlertTriangle } from 'lucide-react';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { kbApi } from '../../api/kbApi';
import { KBClauseListItem } from '../../types/kbTypes';

const KBClauseListPage = () => {
  const router = useRouter();
  const [data, setData] = useState<{ items: KBClauseListItem[], total: number }>({ items: [], total: 0 });
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(25);
  const [deleteDialog, setDeleteDialog] = useState<{ open: boolean, id: number | null }>({ open: false, id: null });

  const loadData = async () => {
    setLoading(true);
    try {
      const offset = page * pageSize;
      const res = await kbApi.fetchPaginatedClauses(offset, pageSize);
      setData({ items: res.data.items, total: res.data.total_count });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, pageSize]);

  const handleDelete = async () => {
    if (deleteDialog.id) {
      try {
        await kbApi.deleteClause(deleteDialog.id);
        loadData();
      } catch (err) {
        console.error(err);
      }
    }
    setDeleteDialog({ open: false, id: null });
  };

  const totalPages = Math.ceil(data.total / pageSize);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 pt-24 pb-12">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold text-foreground tracking-tight">Baza Wiedzy</h1>
            <p className="text-muted-foreground text-sm mt-1">Zarządzaj swoimi regułami i definicjami klauzul</p>
          </div>
          <button
            onClick={() => router.push('/kb/editor/new')}
            className="px-5 py-2.5 bg-primary hover:bg-primary/95 text-white font-semibold rounded-xl shadow-glow-primary transition-all flex items-center gap-2 text-sm"
          >
            <Plus size={18} />
            Nowa Klauzula
          </button>
        </div>

        {/* Table Container */}
        <div className="bg-card border border-border/80 rounded-2xl shadow-sm overflow-hidden flex flex-col">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-muted border-b border-border text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  <th className="px-6 py-4">ID</th>
                  <th className="px-6 py-4">Identyfikator</th>
                  <th className="px-6 py-4">Kategoria</th>
                  <th className="px-6 py-4 text-right">Akcje</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-sm">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-12 text-center">
                      <div className="flex justify-center items-center gap-2">
                        <svg className="animate-spin h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        <span className="text-muted-foreground font-medium">Ładowanie danych...</span>
                      </div>
                    </td>
                  </tr>
                ) : data.items.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-12 text-center text-muted-foreground italic">
                      Brak klauzul w bazie wiedzy. Kliknij "Nowa Klauzula" aby dodać.
                    </td>
                  </tr>
                ) : (
                  data.items.map((row) => (
                    <tr key={row.id} className="hover:bg-muted/30 transition-colors">
                      <td className="px-6 py-4 font-semibold text-muted-foreground">{row.id}</td>
                      <td className="px-6 py-4 font-mono text-foreground font-medium">{row.cl_ident}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                          row.cl_category === 'definicja'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                            : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300'
                        }`}>
                          {row.cl_category}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <button
                            onClick={() => router.push(`/kb/exec/${row.id}`)}
                            className="p-2 text-primary hover:bg-primary/10 rounded-lg transition-colors"
                            title="Uruchom"
                          >
                            <Play size={16} />
                          </button>
                          <button
                            onClick={() => router.push(`/kb/editor/${row.id}`)}
                            className="p-2 text-muted-foreground hover:bg-muted rounded-lg transition-colors"
                            title="Edytuj"
                          >
                            <Edit size={16} />
                          </button>
                          <button
                            onClick={() => setDeleteDialog({ open: true, id: row.id })}
                            className="p-2 text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
                            title="Usuń"
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="p-4 border-t border-border flex flex-col sm:flex-row justify-between items-center gap-4 bg-muted/20">
              <div className="text-xs text-muted-foreground font-medium">
                Pokazano {page * pageSize + 1} - {Math.min((page + 1) * pageSize, data.total)} z {data.total} klauzul
              </div>
              <div className="flex items-center gap-2">
                <button
                  disabled={page === 0}
                  onClick={() => setPage(p => p - 1)}
                  className="px-3 py-1.5 border border-border hover:bg-muted text-foreground text-xs font-semibold rounded-lg transition-all disabled:opacity-50"
                >
                  Poprzednia
                </button>
                <div className="text-xs text-foreground font-semibold px-2">
                  Strona {page + 1} z {totalPages}
                </div>
                <button
                  disabled={page >= totalPages - 1}
                  onClick={() => setPage(p => p + 1)}
                  className="px-3 py-1.5 border border-border hover:bg-muted text-foreground text-xs font-semibold rounded-lg transition-all disabled:opacity-50"
                >
                  Następna
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Delete Confirmation Dialog */}
      {deleteDialog.open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
          <div className="bg-card border border-border rounded-2xl max-w-md w-full shadow-2xl overflow-hidden p-6 space-y-4">
            <div className="flex items-center gap-3 text-destructive">
              <AlertTriangle size={24} />
              <h3 className="text-lg font-bold">Potwierdź usunięcie</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Czy na pewno chcesz usunąć tę klauzulę? Ta operacja jest nieodwracalna.
            </p>
            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setDeleteDialog({ open: false, id: null })}
                className="px-4 py-2 border border-border hover:bg-muted text-foreground rounded-lg text-sm font-semibold transition-all"
              >
                Anuluj
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-destructive hover:bg-destructive/90 text-white rounded-lg text-sm font-semibold transition-all shadow-glow-accent"
              >
                Usuń
              </button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};

export default KBClauseListPage;
