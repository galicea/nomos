// frontend0/src/components/kb/ClauseSubParametersEditor.tsx
import React from 'react';
import { KBClauseSubPar, KBClausePar } from '../../types/kbTypes';
import { Trash2, Plus } from 'lucide-react';

interface Props {
  subParams: KBClauseSubPar[];
  mainClauseParams: KBClausePar[]; 
  onChange: (newSubParams: KBClauseSubPar[]) => void;
}

export const ClauseSubParametersEditor: React.FC<Props> = ({ subParams, mainClauseParams, onChange }) => {
  const handleParamChange = (index: number, field: keyof KBClauseSubPar, value: any) => {
    const updated = [...subParams];
    const param = { ...updated[index] };
    if (field === 'value') {
      param.value = value || undefined;
      param.unify_par = undefined;
      param.unify_cl = undefined;
    } else if (field === 'unify_par') {
      param.unify_par = value || undefined;
      param.unify_cl = 'parent';
      param.value = undefined;
    } else {
      (param as any)[field] = value;
    }
    updated[index] = param;
    onChange(updated);
  };

  const addParam = () => {
    onChange([...subParams, { par_ident: '', cut: false, value: undefined, unify_par: undefined, unify_cl: undefined }]);
  };

  const removeParam = (index: number) => {
    onChange(subParams.filter((_, i) => i !== index));
  };

  return (
    <div className="p-4 border border-dashed border-border rounded-xl mt-3 bg-muted/40 space-y-3">
      <h4 className="text-sm font-semibold text-foreground">Parametry wywołania</h4>
      
      <div className="space-y-2">
        {subParams.map((param, index) => (
          <div 
            key={index} 
            className="flex flex-col lg:flex-row gap-3 p-3 bg-card border border-border rounded-lg items-center shadow-sm"
          >
            <div className="w-full lg:w-1/4">
              <label className="block text-[10px] font-medium text-muted-foreground mb-0.5">
                Ident. parametru
              </label>
              <input
                type="text"
                value={param.par_ident}
                onChange={(e) => handleParamChange(index, 'par_ident', e.target.value)}
                placeholder="np. par_x"
                className="w-full px-2 py-1.5 bg-background border border-border rounded text-xs focus:outline-none focus:ring-2 focus:ring-primary/45"
              />
            </div>
            
            <div className="w-full lg:w-1/4">
              <label className="block text-[10px] font-medium text-muted-foreground mb-0.5">
                Wartość
              </label>
              <input
                type="text"
                value={param.value || ''}
                disabled={!!param.unify_par}
                onChange={(e) => handleParamChange(index, 'value', e.target.value)}
                placeholder="Wartość parametru"
                className="w-full px-2 py-1.5 bg-background border border-border rounded text-xs focus:outline-none focus:ring-2 focus:ring-primary/45 disabled:opacity-50"
              />
            </div>
            
            <div className="text-[10px] font-semibold text-muted-foreground">LUB</div>
            
            <div className="w-full lg:w-1/4">
              <label className="block text-[10px] font-medium text-muted-foreground mb-0.5">
                Unifikuj z...
              </label>
              <select
                value={param.unify_par || ''}
                disabled={!!param.value}
                onChange={(e) => handleParamChange(index, 'unify_par', e.target.value)}
                className="w-full px-2 py-1.5 bg-background border border-border rounded text-xs focus:outline-none focus:ring-2 focus:ring-primary/45 disabled:opacity-50"
              >
                <option value="">*Brak*</option>
                {mainClauseParams.map(p => (
                  <option key={p.par_ident} value={p.par_ident}>{p.par_ident}</option>
                ))}
              </select>
            </div>
            
            <div className="flex items-center gap-1.5 self-end lg:self-center">
              <input
                type="checkbox"
                id={`cut-${index}`}
                checked={param.cut}
                onChange={(e) => handleParamChange(index, 'cut', e.target.checked)}
                className="h-4 w-4 text-primary focus:ring-primary border-border rounded"
              />
              <label htmlFor={`cut-${index}`} className="text-xs text-foreground cursor-pointer select-none">
                Odcięcie
              </label>
            </div>
            
            <button
              type="button"
              onClick={() => removeParam(index)}
              className="lg:ml-auto p-1.5 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded transition-colors"
              title="Usuń parametr wywołania"
            >
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={addParam}
        className="px-3 py-1.5 border border-primary text-primary hover:bg-primary/10 rounded text-xs font-semibold transition-all flex items-center gap-1"
      >
        <Plus size={14} />
        Dodaj parametr wywołania
      </button>
    </div>
  );
};
