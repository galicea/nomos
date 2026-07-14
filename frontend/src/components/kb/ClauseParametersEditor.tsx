// frontend0/src/components/kb/ClauseParametersEditor.tsx
import React from 'react';
import { KBClausePar } from '../../types/kbTypes';
import { Trash2, Plus } from 'lucide-react';

interface Props {
  params: KBClausePar[];
  onChange: (newParams: KBClausePar[]) => void;
}

export const ClauseParametersEditor: React.FC<Props> = ({ params, onChange }) => {
  const handleParamChange = (index: number, field: keyof KBClausePar, value: string) => {
    const updated = params.map((item, i) => {
      if (i !== index) return item;
      return { ...item, [field]: value };
    });
    onChange(updated);
  };

  const addParam = () => {
    onChange([...params, { par_ident: '', par_description: '' }]);
  };

  const removeParam = (index: number) => {
    onChange(params.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground">Parametry klauzuli</h3>
      
      <div className="space-y-2">
        {params.map((param, index) => (
          <div 
            key={index} 
            className="flex flex-col sm:flex-row gap-3 p-4 bg-card border border-border rounded-xl items-center shadow-sm"
          >
            <div className="flex-1 w-full">
              <label className="block text-xs font-medium text-muted-foreground mb-1">
                Ident. parametru
              </label>
              <input
                type="text"
                value={param.par_ident}
                onChange={(e) => handleParamChange(index, 'par_ident', e.target.value)}
                placeholder="np. par_nazwa"
                className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
              />
            </div>
            
            <div className="flex-[2] w-full">
              <label className="block text-xs font-medium text-muted-foreground mb-1">
                Opis
              </label>
              <input
                type="text"
                value={param.par_description || ''}
                onChange={(e) => handleParamChange(index, 'par_description', e.target.value)}
                placeholder="Opis parametru"
                className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
              />
            </div>
            
            <button
              type="button"
              onClick={() => removeParam(index)}
              className="mt-5 p-2 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg transition-colors flex items-center justify-center"
              title="Usuń parametr"
            >
              <Trash2 size={18} />
            </button>
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={addParam}
        className="px-4 py-2 border border-primary text-primary hover:bg-primary/10 rounded-lg text-sm font-medium transition-all flex items-center gap-2"
      >
        <Plus size={16} />
        Dodaj parametr
      </button>
    </div>
  );
};
