// frontend0/src/components/kb/ClauseRunnerForm.tsx
import React, { useState, useEffect } from 'react';
import { KBClause } from '../../types/kbTypes';

export type ParameterValueMap = Record<string, string>;

interface Props {
  clause: KBClause;
  onSubmit: (values: ParameterValueMap) => void;
  isLoading?: boolean;
}

export const ClauseRunnerForm: React.FC<Props> = ({ clause, onSubmit, isLoading = false }) => {
  const [paramValues, setParamValues] = useState<ParameterValueMap>({});

  useEffect(() => {
    if (clause && clause.parameters) {
      const initialValues = clause.parameters.reduce((acc, param) => {
        acc[param.par_ident] = '';
        return acc;
      }, {} as ParameterValueMap);
      setParamValues(initialValues);
    }
  }, [clause]);

  const handleValueChange = (par_ident: string, newValue: string) => {
    setParamValues(prevValues => ({ ...prevValues, [par_ident]: newValue }));
  };

  const handleSubmit = () => {
    onSubmit(paramValues);
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-6 shadow-md max-w-4xl mx-auto mt-6">
      <h2 className="text-2xl font-bold text-foreground mb-6">Uruchom Klauzulę</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-xs font-semibold text-muted-foreground mb-1">
            ID Klauzuli
          </label>
          <input
            type="text"
            value={clause.id || 'Brak'}
            readOnly
            className="w-full px-3 py-2 bg-muted/50 border border-border rounded-lg text-sm text-foreground focus:outline-none"
          />
        </div>
        
        <div>
          <label className="block text-xs font-semibold text-muted-foreground mb-1">
            Identyfikator (cl_ident)
          </label>
          <input
            type="text"
            value={clause.cl_ident}
            readOnly
            className="w-full px-3 py-2 bg-muted/50 border border-border rounded-lg text-sm text-foreground focus:outline-none"
          />
        </div>
        
        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-muted-foreground mb-1">
            Opis
          </label>
          <textarea
            value={clause.cl_description || 'Brak opisu'}
            readOnly
            rows={3}
            className="w-full px-3 py-2 bg-muted/50 border border-border rounded-lg text-sm text-foreground focus:outline-none resize-none"
          />
        </div>
      </div>

      <h3 className="text-lg font-bold text-foreground mb-3">Parametry wejściowe</h3>
      
      <div className="border border-border rounded-xl overflow-hidden shadow-sm bg-background mb-6">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted border-b border-border text-xs font-semibold text-muted-foreground">
              <th className="px-4 py-3">Parametr</th>
              <th className="px-4 py-3">Opis</th>
              <th className="px-4 py-3 w-[40%]">Wartość</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border text-sm">
            {clause.parameters.map((param) => (
              <tr key={param.par_ident} className="hover:bg-muted/30 transition-colors">
                <td className="px-4 py-3 font-mono text-xs font-semibold text-primary">
                  {param.par_ident}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {param.par_description || '---'}
                </td>
                <td className="px-4 py-3">
                  <input
                    type="text"
                    value={paramValues[param.par_ident] || ''}
                    onChange={(e) => handleValueChange(param.par_ident, e.target.value)}
                    disabled={isLoading}
                    placeholder="Podaj wartość"
                    className="w-full px-3 py-1.5 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45 disabled:opacity-50"
                  />
                </td>
              </tr>
            ))}
            {clause.parameters.length === 0 && (
              <tr>
                <td colSpan={3} className="px-4 py-6 text-center text-muted-foreground italic">
                  Ta klauzula nie wymaga parametrów.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className="px-6 py-2.5 bg-primary hover:bg-primary/95 text-white font-semibold rounded-lg shadow-glow-primary transition-all disabled:opacity-50 flex items-center gap-2 text-sm"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Uruchamianie...
            </>
          ) : (
            'Uruchom'
          )}
        </button>
      </div>
    </div>
  );
};
