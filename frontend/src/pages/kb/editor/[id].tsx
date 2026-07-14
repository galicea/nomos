import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Save, ArrowLeft } from 'lucide-react';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { kbApi } from '../../../api/kbApi';
import { KBClause, KBClauseSimple } from '../../../types/kbTypes';
import { ClauseParametersEditor } from '../../../components/kb/ClauseParametersEditor';
import { ClauseSubsEditor } from '../../../components/kb/ClauseSubsEditor';

const ClauseEditorPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [clause, setClause] = useState<KBClause | null>(null);
  const [clauseList, setClauseList] = useState<KBClauseSimple[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const init = async () => {
      try {
        const listRes = await kbApi.fetchClauseList();
        setClauseList(listRes.data);
        if (id === 'new') {
          setClause({ cl_ident: '', cl_category: 'definicja', parameters: [], subs: [] });
        } else if (id) {
          const res = await kbApi.fetchClauseById(Number(id));
          setClause(res.data);
        }
      } catch (err) {
        console.error(err);
      }
    };
    if (id) init();
  }, [id]);

  const handleSave = async () => {
    if (!clause) return;
    setLoading(true);
    try {
      if (clause.id) await kbApi.updateClause(clause.id, clause);
      else await kbApi.createClause(clause);
      router.push('/kb');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!clause) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <Navbar />
        <div className="flex-1 flex justify-center items-center">
          <svg className="animate-spin h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 pt-24 pb-12">
        <div className="max-w-4xl mx-auto space-y-6">
          
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push('/kb')}
              className="p-2 border border-border hover:bg-muted text-foreground rounded-lg transition-colors"
              title="Wróć"
            >
              <ArrowLeft size={16} />
            </button>
            <h1 className="text-2xl font-bold text-foreground">Edytor Klauzuli</h1>
          </div>

          <div className="bg-card border border-border rounded-2xl p-6 shadow-sm space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-muted-foreground mb-1">
                  Identyfikator
                </label>
                <input
                  type="text"
                  value={clause.cl_ident}
                  onChange={(e) => setClause({ ...clause, cl_ident: e.target.value })}
                  placeholder="np. cl_identyfikator"
                  className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-muted-foreground mb-1">
                  Kategoria
                </label>
                <select
                  value={clause.cl_category}
                  onChange={(e) => setClause({ ...clause, cl_category: e.target.value as any })}
                  className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
                >
                  <option value="definicja">Definicja (Reguła)</option>
                  <option value="baza">Baza (Widok SQL)</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block text-xs font-semibold text-muted-foreground mb-1">
                  Opis
                </label>
                <textarea
                  value={clause.cl_description || ''}
                  onChange={(e) => setClause({ ...clause, cl_description: e.target.value })}
                  placeholder="Opis klauzuli..."
                  rows={3}
                  className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45 resize-none"
                />
              </div>

              {clause.cl_category === 'baza' && (
                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-muted-foreground mb-1">
                    Nazwa widoku SQL (q_...)
                  </label>
                  <input
                    type="text"
                    value={clause.cl_view_name || ''}
                    onChange={(e) => setClause({ ...clause, cl_view_name: e.target.value })}
                    placeholder="np. q_widok_danych"
                    className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
                  />
                </div>
              )}
            </div>

            <hr className="border-border" />

            <ClauseParametersEditor
              params={clause.parameters}
              onChange={(p) => setClause({ ...clause, parameters: p })}
            />

            {clause.cl_category === 'definicja' && (
              <>
                <hr className="border-border" />
                <ClauseSubsEditor
                  subs={clause.subs || []}
                  currentClause={clause}
                  clauseList={clauseList}
                  onChange={(s) => setClause({ ...clause, subs: s })}
                />
              </>
            )}

            <div className="flex justify-end gap-3 pt-4 border-t border-border">
              <button
                type="button"
                onClick={() => router.push('/kb')}
                className="px-5 py-2 border border-border hover:bg-muted text-foreground rounded-lg text-sm font-semibold transition-all"
              >
                Anuluj
              </button>
              <button
                type="button"
                onClick={handleSave}
                disabled={loading}
                className="px-5 py-2 bg-primary hover:bg-primary/95 text-white rounded-lg text-sm font-semibold transition-all shadow-glow-primary flex items-center gap-1.5 disabled:opacity-50"
              >
                <Save size={16} />
                Zapisz
              </button>
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ClauseEditorPage;
