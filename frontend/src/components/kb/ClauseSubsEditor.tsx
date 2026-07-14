// frontend0/src/components/kb/ClauseSubsEditor.tsx
import React from 'react';
import { KBClauseSub, KBClausePar, KBClauseSimple, KBClauseSubPar, KBClause } from '../../types/kbTypes';
import { Trash2, Plus } from 'lucide-react';
import { ClauseSubParametersEditor } from './ClauseSubParametersEditor';

interface Props {
  subs: KBClauseSub[];
  currentClause: KBClause | null;
  clauseList: KBClauseSimple[];
  onChange: (newSubs: KBClauseSub[]) => void;
}

export const ClauseSubsEditor: React.FC<Props> = ({ subs, currentClause, clauseList, onChange }) => {
  const handleSubChange = (index: number, field: keyof KBClauseSub, value: string | number) => {
    const updated = subs.map((item, i) => {
      if (i !== index) return item;
      return { ...item, [field]: value };
    });
    onChange(updated);
  };

  const handleSubParamsChange = (subIndex: number, newSubParams: KBClauseSubPar[]) => {
    const updatedSubs = subs.map((sub, i) => {
      if (i !== subIndex) return sub;
      return { ...sub, parameters: newSubParams };
    });
    onChange(updatedSubs);
  };

  const addSub = () => {
    onChange([...subs, { sub_id: 0, order: (subs.length + 1) * 10, parameters: [] }]);
  };

  const removeSub = (index: number) => {
    onChange(subs.filter((_, i) => i !== index));
  };

  const getUnifiableParams = (currentSubOrder: number): KBClausePar[] => {
    const parentParams: KBClausePar[] = currentClause?.parameters || [];
    let precedingSubParams: KBClausePar[] = []
    const subs_list = subs;
    if (subs_list) {
      precedingSubParams = subs_list
        .filter(s => s.order < currentSubOrder)
        .flatMap(s => 
          s.parameters
            .filter(p => !p.cut)
            .map(p => ({
              par_ident: p.par_ident,
              par_description: `(z sub, order ${s.order})`
            }))
        );
    }
    const paramMap = new Map<string, KBClausePar>();
    for (const param of precedingSubParams) paramMap.set(param.par_ident, param);
    for (const param of parentParams) paramMap.set(param.par_ident, param);
    return Array.from(paramMap.values());
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground">Klauzule podrzędne (Definicja)</h3>
      
      <div className="space-y-4">
        {subs.map((sub, index) => (
          <div key={index} className="p-4 bg-card border border-border rounded-xl shadow-sm space-y-3">
            <div className="flex flex-col sm:flex-row gap-3 items-center">
              <div className="w-full sm:w-28">
                <label className="block text-xs font-medium text-muted-foreground mb-1">
                  Kolejność
                </label>
                <input
                  type="number"
                  value={sub.order}
                  onChange={(e) => handleSubChange(index, 'order', e.target.value || '')}
                  className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
                />
              </div>

              <div className="flex-1 w-full">
                <label className="block text-xs font-medium text-muted-foreground mb-1">
                  Klauzula podrzędna (sub_id)
                </label>
                <select
                  value={sub.sub_id || 0}
                  onChange={(e) => handleSubChange(index, 'sub_id', Number(e.target.value))}
                  className="w-full px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/45"
                >
                  <option value={0}>*Wybierz klauzulę*</option>
                  {clauseList.map(c => (
                    <option key={c.id} value={c.id}>{c.cl_ident} (ID: {c.id})</option>
                  ))}
                </select>
              </div>

              <button
                type="button"
                onClick={() => removeSub(index)}
                className="sm:mt-5 p-2 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg transition-colors flex items-center justify-center self-end sm:self-center"
                title="Usuń klauzulę podrzędną"
              >
                <Trash2 size={18} />
              </button>
            </div>

            <ClauseSubParametersEditor
              subParams={sub.parameters}
              mainClauseParams={getUnifiableParams(sub.order)}
              onChange={(newParams) => handleSubParamsChange(index, newParams)}
            />
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={addSub}
        className="px-4 py-2 border border-primary text-primary hover:bg-primary/10 rounded-lg text-sm font-medium transition-all flex items-center gap-2"
      >
        <Plus size={16} />
        Dodaj klauzulę podrzędną
      </button>
    </div>
  );
};
