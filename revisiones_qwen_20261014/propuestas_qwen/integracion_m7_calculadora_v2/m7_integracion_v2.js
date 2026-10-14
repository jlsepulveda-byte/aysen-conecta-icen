'use strict';
const M7S = { res: null, docs: [], alerts: [], obs: [], evs: [], rev: {}, err: null, msgs: [], suggestions: [] };

const M7_TO_CALCULATOR = {
  'PAGOS': { field: 'c_pay', label: 'plazo de pago pactado', unit: 'días' },
  'ANTICIPO': { field: 'c_adv', label: 'anticipo', unit: '%' },
  'RETENCION': { field: 'c_ret', label: 'retención', unit: '%' },
  'MULTA': { field: 'c_pen', label: 'exposición a multa', unit: '%' },
  'PLAZO_EJECUCION': { field: 'c_months', label: 'duración', unit: 'meses' }
};

const M7_BLOQUEO = {
  pago: ['c_pay', 'c_retDays', 'c_adv', 'c_ret'], credito_servicio: ['c_pen'],
  PLAZOS_PAGO: ['c_pay', 'c_retDays', 'c_adv', 'c_ret'], PORCENTAJES_CREDITO_SERVICIO: ['c_pen'],
  ANTICIPO: ['c_adv'], RETENCION: ['c_ret'], MULTA: ['c_pen']
};

const M7_ETQ = { c_pay: 'plazo de pago pactado', c_retDays: 'liberación de retención', c_adv: 'anticipo', c_ret: 'retención', c_pen: 'exposición a multa', c_months: 'duración del proyecto' };
const m7e = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function generateSuggestions() {
  M7S.suggestions = [];
  if (!M7S.res || !M7S.res.issues) return;
  for (const issue of M7S.res.issues) {
    const mapping = M7_TO_CALCULATOR[issue.matter];
    if (!mapping) continue;
    for (const ev of issue.evidence) {
      for (const nv of ev.numericValues) {
        if ((nv.tipo === 'PORCENTAJE' && mapping.unit === '%') || (nv.tipo === 'DIAS' && mapping.unit === 'días')) {
          M7S.suggestions.push({
            id: `SUG_${M7S.suggestions.length + 1}`, field: mapping.field, label: mapping.label, value: nv.valor, unit: mapping.unit,
            source: { documentId: ev.documentId, section: ev.section, page: ev.page, quote: ev.quote },
            confidence: ev.confidence, status: 'PENDIENTE'
          });
        }
      }
    }
  }
}

function applySuggestion(suggestionId, action) {
  const sug = M7S.suggestions.find(s => s.id === suggestionId);
  if (!sug) return;
  if (action === 'CONFIRMAR') {
    sug.status = 'CONFIRMADO';
    const field = document.getElementById(sug.field);
    if (field) {
      field.value = sug.value;
      const srcField = document.getElementById(sug.field + '_src');
      if (srcField) srcField.innerHTML = `<small>Confirmado desde ${m7e(sug.source.section)} · ${m7e(sug.source.documentId)} · Pág ${sug.source.page}</small>`;
    }
  } else if (action === 'RECHAZAR') {
    sug.status = 'RECHAZADO';
  }
  m7RenderSuggestions();
}

function m7RenderSuggestions() {
  const container = document.getElementById('m7Suggestions');
  if (!container) return;
  if (M7S.suggestions.length === 0) {
    container.innerHTML = '<p class="small muted">No hay valores sugeridos desde el análisis contractual.</p>';
    return;
  }
  let html = '<h3>Valores sugeridos desde el contrato</h3><p class="small">Cada valor debe ser confirmado manualmente antes de aplicarse a la calculadora.</p>';
  for (const sug of M7S.suggestions) {
    const badge = sug.confidence === 'ALTA' ? '<span class="badge" style="background:#4caf50;color:white">ALTA</span>' :
                  sug.confidence === 'MEDIA' ? '<span class="badge" style="background:#ff9800;color:white">MEDIA</span>' :
                  '<span class="badge" style="background:#f44336;color:white">BLOQUEADA</span>';
    const status = sug.status === 'CONFIRMADO' ? '<span style="color:#4caf50">✓ Confirmado</span>' :
                   sug.status === 'RECHAZADO' ? '<span style="color:#9e9e9e">✗ Rechazado</span>' : '';
    html += `<div class="card" style="margin:12px 0;padding:12px;border-left:4px solid ${sug.confidence === 'ALTA' ? '#4caf50' : sug.confidence === 'MEDIA' ? '#ff9800' : '#f44336'}">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div><strong>${m7e(sug.label)}:</strong> ${sug.value} ${sug.unit} ${badge} ${status}</div>
        ${sug.status === 'PENDIENTE' ? `<div><button class="btn secondary sm" onclick="applySuggestion('${sug.id}','CONFIRMAR')">Confirmar</button><button class="btn secondary sm" onclick="applySuggestion('${sug.id}','RECHAZAR')">Rechazar</button></div>` : ''}
      </div>
      <div class="small muted" style="margin-top:8px">Fuente: ${m7e(sug.source.section)} · ${m7e(sug.source.documentId)} · Pág ${sug.source.page}</div>
      <blockquote style="margin:8px 0;padding:8px;border-left:3px solid #116e65;background:#f5f8f7;font-size:12px">${m7e(sug.source.quote.slice(0, 200))}${sug.source.quote.length > 200 ? '…' : ''}</blockquote>
    </div>`;
  }
  container.innerHTML = html;
}

function m7RenderContradictions() {
  const container = document.getElementById('m7Contradictions');
  if (!container || !M7S.res || !M7S.res.contradictions) return;
  if (M7S.res.contradictions.length === 0) {
    container.innerHTML = '<p class="small muted">No se detectaron contradicciones numéricas entre cláusulas.</p>';
    return;
  }
  let html = '<h3>⚠️ Contradicciones detectadas</h3><p class="small">Estas diferencias requieren revisión humana antes de continuar.</p>';
  for (const c of M7S.res.contradictions) {
    html += `<div class="card" style="margin:12px 0;padding:12px;border-left:4px solid #f44336">
      <strong>Contradicción en ${m7e(c.topic)}:</strong>
      <div style="margin:8px 0"><div><strong>${m7e(c.clauseA.section)}:</strong> ${c.clauseA.valor} ${c.clauseA.raw}</div>
      <div><strong>${m7e(c.clauseB.section)}:</strong> ${c.clauseB.valor} ${c.clauseB.raw}</div></div>
      <div class="small muted">Esta contradicción bloquea la transferencia automática. Revise ambas cláusulas y confirme cuál aplica.</div>
    </div>`;
  }
  container.innerHTML = html;
}

function m7Blocked() {
  const s = new Set();
  M7S.alerts.forEach(a => { if (!m7Revisada(a.id)) (M7_BLOQUEO[a.topic] || []).forEach(x => s.add(x)); });
  M7S.obs.forEach((o, i) => { if (!m7Revisada('OBS'+i)) (M7_BLOQUEO[o.code.replace(/^PORCENTAJES_(.*)$/, 'PORCENTAJES_$1')] || []).forEach(x => s.add(x)); });
  return [...s];
}
function m7Revisada(id) { return M7S.rev[id] === 'revisada' || M7S.rev[id] === 'descartada'; }
function m7Rev(id, v) { M7S.rev[id] = v; m7Guard(); }

function m7Guard() {
  const el = document.getElementById('m7Guard');
  if (!el) return;
  const b = m7Blocked();
  el.innerHTML = `<b>Transferencia a la calculadora:</b> ninguna conclusión jurídica del evaluador M7 pasa a la Calculadora ICEN. ${b.length ? ' Además, estos valores quedan retenidos hasta que una persona revise los hallazgos relacionados: <b>' + b.map(x => M7_ETQ[x]).join(', ') + '</b>.' : ' No hay valores retenidos por hallazgos sin revisar.'} ${M7S.suggestions.length ? ` Hay ${M7S.suggestions.filter(s => s.status === 'PENDIENTE').length} valores sugeridos pendientes de confirmación.` : ''}`;
}

window.applySuggestion = applySuggestion;
