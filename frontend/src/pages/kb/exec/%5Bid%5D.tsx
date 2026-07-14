import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { ArrowLeft } from 'lucide-react';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { kbApi } from '../../../api/kbApi';
import { KBClause } from '../../../types/kbTypes';
import { ClauseRunnerForm, ParameterValueMap } from '../../../components/kb/ClauseRunnerForm';

const ClauseExecPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [clause, setClause] = useState<KBClause | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const init = async () => {
      if (id) {
        try {
          const res = await kbApi.fetchClauseById(Number(id));
          setClause(res.data);
        } catch (err) {
          console.error(err);
        }
      }
    };
    init();
  }, [id]);

  const handleRun = async (values: ParameterValueMap) => {
    if (!clause?.id) return;
    setLoading(true);
    try {
      const res = await kbApi.execClauseCsv(clause.id, values);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `result_${clause.cl_ident}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert('Błąd wykonania klauzuli');
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
            <h1 className="text-2xl font-bold text-foreground">Wykonaj Klauzulę</h1>
          </div>

          <ClauseRunnerForm clause={clause} onSubmit={handleRun} isLoading={loading} />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ClauseExecPage;
