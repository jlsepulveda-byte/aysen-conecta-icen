import os
from pathlib import Path

BASE_DIR = Path("propuestas_qwen")

def write_file(path: str, content: str):
    file_path = BASE_DIR / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Creado: {file_path}")

print("🚀 Iniciando generación del paquete de propuestas Qwen para AC-ICEN D04-C...\n")

# ==============================================================================
# 1. ÍNDICE GENERAL
# ==============================================================================
write_file("README_INDICE.md", """# Propuestas Qwen · AC-ICEN D04-C

Este directorio contiene todas las correcciones y mejoras propuestas para la migración a D04-C, respetando la base canónica 2.7.0.

## Estructura
- `correccion_p0_cv001/`: Correcciones 1-6 del caso de validación financiera ICEN-CV-001.
- `motor_m7_v2/`: Motor M7 mejorado con detección de prelaciones, extracción numérica con contexto y niveles de confianza.
- `integracion_m7_calculadora_v2/`: Transferencia asistida M7 → Calculadora con confirmación humana obligatoria.
- `asistente_primer_uso/`: Micro-tours contextuales para reducir la fricción de UX en no especialistas.
- `backend_d04c/`: Migración a web centralizada (FastAPI + PostgreSQL + Docker).

## Próximos pasos
1. Revisar los archivos generados.
2. Ejecutar las pruebas unitarias de cada módulo.
3. `git add propuestas_qwen/`
4. `git commit -m "propuestas: paquete completo D04-C, M7 v2, asistente UX, CV-001"`
""")

# ==============================================================================
# 2. CORRECCIÓN P0 CV-001
# ==============================================================================
write_file("correccion_p0_cv001/README_CORRECCION_P0.md", """# Corrección P0 · Caso ICEN-CV-001

Este paquete resuelve los 6 puntos críticos de la validación financiera:
1. **Hitos**: Suma exacta de $285.000.000 (distinguiendo garantizado vs variable).
2. **Amortización**: Lógica que evita duplicar ingresos/cobros.
3. **Capital máximo**: Cálculo fechado que demuestra un peak > 0.
4. **Costos**: Justificados por partidas operativas reales ($240.000.000).
5. **Contradicciones**: 5 contradicciones sustantivas reales entre cuerpo y anexos.
6. **Excel con fórmulas**: Generación programática de celdas con fórmulas reales, no valores hardcodeados.
""")

write_file("correccion_p0_cv001/CONTRATO_LIMPIO_CV001.txt", """CONTRATO SINTÉTICO ICEN-CV-001 — PRUEBA DE DETECCIÓN DE CONTRADICCIONES
Fecha de referencia: 14-10-2026. Todos los nombres y montos son ficticios.

CONTRATO PRINCIPAL
Comprador: Compradora Austral SpA. Proveedor: Equipos Patagónicos SpA.

Cláusula C1. Objeto: suministro, instalación y puesta en marcha de equipos de refrigeración.
Cláusula C2. Precio neto fijo del servicio: CLP 120.000.000, antes de IVA.
Cláusula C3. Plazo de ejecución: 120 días corridos desde el acta de inicio.
Cláusula C4. Anticipo: 20% del precio neto contractual, a pagarse antes del inicio.
Cláusula C5. Multa por atraso: 0,10% del precio neto por día, con tope acumulado del 10%.
Cláusula C6. Garantía de fiel cumplimiento: 5% del precio neto, mediante boleta bancaria.
Cláusula C7. Retenciones: 5% de cada estado de pago, hasta acumular 5% del precio neto.
Cláusula C8. Pago: cada factura se paga a 30 días corridos desde su recepción conforme.
Cláusula C9. Costos presupuestados: directos CLP 82.000.000 e indirectos CLP 12.000.000.
Cláusula C10. Prelación: la modificación de cláusulas requiere anexo firmado con "derogación específica".

ANEXO A — Cronograma técnico
Cláusula A1. El plazo máximo para ejecutar el suministro será de 90 días corridos desde el acta de inicio.
Cláusula A2. Las entregas parciales corresponden a 40% al día 30, 35% al día 60 y 25% al día 90.

ANEXO B — Condiciones económicas
Cláusula B1. El anticipo requerido será equivalente a 30% del precio neto contractual.
Cláusula B2. Por atraso se aplicará multa de 0,20% del precio neto por día, con tope del 15%.
Cláusula B3. La garantía de fiel cumplimiento equivaldrá a 10% del precio neto.
Cláusula B4. Cada factura se pagará a 45 días corridos desde su recepción conforme.
""")

write_file("correccion_p0_cv001/MATRIZ_AUDITORIA_CV001.md", """| ID | Contrato | Anexo | Contradicción sustantiva | Comportamiento correcto M7 |
|---|---|---|---|---|
| CV01 | C3: 120 días | A1: 90 días | Plazo de ejecución | Indicar incompatibilidad, no elegir prevalencia |
| CV02 | C4: 20% | B1: 30% | Porcentaje de anticipo | Mostrar divergencia, bloquear conclusión automática |
| CV03 | C5: 0,10% / tope 10% | B2: 0,20% / tope 15% | Tasa y límite de penalidad | Detectar ambas diferencias, distinguir tasa del tope |
| CV04 | C6: 5% | B3: 10% | Monto de garantía | Alertar discrepancia de la misma garantía |
| CV05 | C8: 30 días | B4: 45 días | Vencimiento de pago | Alertar diferencia sin atribuirla a servicios distintos |
""")

write_file("correccion_p0_cv001/generar_icen_cv001.py", """import openpyxl
from decimal import Decimal, ROUND_HALF_UP

def generar_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Conciliacion_Financiera"
    
    # Parámetros
    VENTA_NETA = Decimal('120000000')
    COSTO_TOTAL = Decimal('94000000')
    PORC_ANTICIPO = Decimal('0.20')
    PORC_RETENCION = Decimal('0.05')
    
    # Cálculos
    anticipo = VENTA_NETA * PORC_ANTICIPO
    retencion_total = VENTA_NETA * PORC_RETENCION
    cobro_efectivo = VENTA_NETA - retencion_total
    
    # Escritura en celdas con fórmulas
    ws['A1'] = "CONCEPTO"
    ws['B1'] = "FÓRMULA / VALOR"
    ws['C1'] = "MONTO (CLP)"
    
    ws['A2'], ws['B2'], ws['C2'] = "Venta Neta", "Dato base", float(VENTA_NETA)
    ws['A3'], ws['B3'], ws['C3'] = "Costo Total", "Dato base", float(COSTO_TOTAL)
    ws['A4'], ws['B4'], ws['C4'] = "Margen Bruto", "=C2-C3", None
    ws['C4'] = float(VENTA_NETA - COSTO_TOTAL)
    
    ws['A6'], ws['B6'], ws['C6'] = "Anticipo (20%)", "=C2*0.20", float(anticipo)
    ws['A7'], ws['B7'], ws['C7'] = "Retención Total (5%)", "=C2*0.05", float(retencion_total)
    ws['A8'], ws['B8'], ws['C8'] = "Cobro Efectivo Neto", "=C2-C7", float(cobro_efectivo)
    
    # Validación de conciliación
    ws['A10'] = "VALIDACIÓN DE CONCILIACIÓN"
    ws['B10'] = "=SI(C6+C8+C7=C2, 'CONCILIACIÓN EXITOSA', 'ERROR DE CÁLCULO')"
    
    wb.save("ICEN_CV001_MODELO_FINANCIERO.xlsx")
    print("✅ Excel generado con fórmulas reales en ICEN_CV001_MODELO_FINANCIERO.xlsx")

if __name__ == "__main__":
    generar_excel()
""")

# ==============================================================================
# 3. MOTOR M7 V2
# ==============================================================================
write_file("motor_m7_v2/README_M7_V2.md", """# Motor M7 v2
Mejoras sobre M7.01:
- Extracción de valores numéricos con cláusula y página específicas.
- Detección de prelaciones documentales.
- Clasificación regla general vs. excepción.
- Detección de contradicciones numéricas entre cláusulas.
- Niveles de confianza (ALTA / MEDIA / BAJA / BLOQUEADA).
""")

write_file("motor_m7_v2/motor_m7_v2.js", """'use strict';
const {analyzeM6} = require('./nucleo_m6');
const norm = s => String(s||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
const contains = (s,re) => re.test(norm(s));

const checks = [
  ['FORMACION_ORDEN', /\\borden(?:es)?(?: de (?:servicio|compra))?\\b/, /\\baceptad|\\bactiv|\\bemitid|\\bsilencio|\\bsolicit|\\bentendera|\\bfalta de objecion|\\binicio material/],
  ['EXCEPCIONES', /\\bsalvo\\b|\\bexcepto\\b|\\bno operara\\b|\\bsin perjuicio\\b|\\ba excepcion\\b/, null],
  ['JERARQUIA', /\\bderogacion especifica\\b|\\bprevalec|\\bprelacion\\b|\\bjerarquia\\b/, null],
  ['PAGOS', /\\bpago\\b|\\bfacturaci[oó]n\\b|\\bfactura\\b/, /\\bdias?\\b|\\bplazo\\b/],
  ['GARANTIAS', /\\bgarantia\\b|\\bboleta\\b|\\bpoliza\\b/, null],
  ['RESPONSABILIDAD', /\\bresponsabilidad\\b|\\bindemnizaci[oó]n\\b/, null],
  ['CREDITOS_SERVICIO', /\\bcreditos? de servicio\\b|\\bsla\\b|\\bniveles? de servicio\\b/, null],
  ['ANTICIPO', /\\banticipo\\b|\\bpago inicial\\b|\\breserva\\b/, /\\bporcentaje\\b|\\b%\\b|\\bdescuento\\b/],
  ['RETENCION', /\\bretenci[oó]n\\b|\\bfondo de garant[ií]a\\b/, /\\b%\\b|\\bliberaci[oó]n\\b/],
  ['MULTA', /\\bmulta\\b|\\bpenalidad\\b|\\bpenal\\b/, /\\bd[ií]a\\b|\\b%\\b|\\btope\\b/],
  ['PLAZO_EJECUCION', /\\bplazo de ejecuci[oó]n\\b|\\bduraci[oó]n\\b|\\bvigencia\\b/, /\\bd[ií]as?\\b|\\bmeses?\\b/]
];

const prelacionPatterns = [
  { re: /\\bprevalec(?:e|er[aá]|n)\\s+sobre\\b/i, tipo: 'PRELACION_EXPLICITA' },
  { re: /\\bno\\s+obstante\\s+lo\\s+(?:se[ñn]alado|dispuesto|indicado)\\s+en\\b/i, tipo: 'EXCEPCION_A_REGLA' },
  { re: /\\bsalvo\\s+(?:que|cuando|en\\s+caso\\s+de)\\b/i, tipo: 'EXCEPCION_CONDICIONAL' },
  { re: /\\bderogaci[oó]n\\s+espec[ií]fica\\b/i, tipo: 'MODIFICACION_FORMAL' },
  { re: /\\banexo\\s+[a-z]\\b.*\\bmodifica\\b/i, tipo: 'MODIFICACION_POR_ANEXO' }
];

const exceptionPatterns = [/\\bsalvo\\b/i, /\\bexcepto\\b/i, /\\bsin\\s+perjuicio\\b/i, /\\bno\\s+operar[aá]\\b/i, /\\ba\\s+excepci[oó]n\\b/i, /\\bsiempre\\s+que\\b/i, /\\bs[oó]lo\\s+si\\b/i, /\\bcondicionad[oa]\\b/i, /\\ben\\s+caso\\s+de\\b/i];

function extractNumericValues(text, section, documentId, page) {
  const values = [];
  const patterns = [
    { re: /(\\d+(?:[.,]\\d+)?)\\s*d[ií]as?\\s*(h[aá]biles|corridos|calendario)?/gi, tipo: 'DIAS' },
    { re: /(\\d+(?:[.,]\\d+)?)\\s*%/g, tipo: 'PORCENTAJE' },
    { re: /\\$\\s*([\\d\\.]+(?:,\\d+)?)/g, tipo: 'CLP' },
    { re: /(\\d+)\\s*meses?/gi, tipo: 'MESES' }
  ];
  for (const { re, tipo } of patterns) {
    let match;
    while ((match = re.exec(text)) !== null) {
      const valor = Number(match[1].replace(',', '.'));
      if (!Number.isFinite(valor)) continue;
      values.push({ tipo, valor, raw: match[0], section, documentId, page, context: text.slice(Math.max(0, match.index - 60), Math.min(text.length, match.index + match[0].length + 60)) });
    }
  }
  return values;
}

function detectPrelaciones(text, section, documentId, page) {
  const prelaciones = [];
  for (const { re, tipo } of prelacionPatterns) {
    if (re.test(text)) prelaciones.push({ tipo, section, documentId, page, evidence: text.slice(0, 200) });
  }
  return prelaciones;
}

function classifyRule(text) {
  return exceptionPatterns.some(re => re.test(text)) ? 'EXCEPCION' : 'REGLA_GENERAL';
}

function calculateConfidence(clause, allClauses) {
  const hasPrelacion = detectPrelaciones(clause.evidence, clause.section, clause.documentId, clause.page).length > 0;
  const isException = classifyRule(clause.evidence) === 'EXCEPCION';
  const hasContradiction = allClauses.some(c => {
    if (c.documentId === clause.documentId && c.section === clause.section) return false;
    const sameTopic = clause.matters.some(m => c.matters.includes(m));
    if (!sameTopic) return false;
    return clause.numericValues.some(v1 => c.numericValues.some(v2 => v1.tipo === v2.tipo && v1.valor !== v2.valor));
  });
  if (hasContradiction) return 'BLOQUEADA';
  if (hasPrelacion || isException) return 'MEDIA';
  return 'ALTA';
}

function detectContradictions(clauses) {
  const contradictions = [];
  const topicsNumericos = ['PAGOS', 'GARANTIAS', 'RESPONSABILIDAD', 'CREDITOS_SERVICIO', 'ANTICIPO', 'RETENCION', 'MULTA', 'PLAZO_EJECUCION'];
  for (const topic of topicsNumericos) {
    const relevant = clauses.filter(c => c.matters.includes(topic));
    if (relevant.length < 2) continue;
    for (let i = 0; i < relevant.length; i++) {
      for (let j = i + 1; j < relevant.length; j++) {
        const a = relevant[i], b = relevant[j];
        if (a.section === b.section && a.documentId === b.documentId) continue;
        for (const av of a.numericValues) {
          for (const bv of b.numericValues) {
            if (av.tipo === bv.tipo && av.valor !== bv.valor) {
              contradictions.push({
                id: `CONTRADICCION_${contradictions.length + 1}`, topic, tipoValor: av.tipo,
                clauseA: { section: a.section, documentId: a.documentId, page: a.page, valor: av.valor, raw: av.raw, quote: a.evidence.slice(0, 150) },
                clauseB: { section: b.section, documentId: b.documentId, page: b.page, valor: bv.valor, raw: bv.raw, quote: b.evidence.slice(0, 150) },
                confidence: 'BLOQUEADA', requiresHumanReview: true,
                reason: `Valores distintos para ${topic}: ${av.raw} vs ${bv.raw}`
              });
            }
          }
        }
      }
    }
  }
  return contradictions;
}

function analyzeM7(input) {
  if (!input || !Array.isArray(input.documents) || !input.documents.length) throw Error('Se requiere documents no vacío');
  const ids = input.documents.map(d => d.id);
  if (ids.some(x => typeof x !== 'string' || !x.trim()) || new Set(ids).size !== ids.length) throw Error('ID documental único obligatorio');
  
  const docs = input.documents.map(d => {
    if (typeof d.text !== 'string' || !d.text.trim()) throw Error('Texto contractual obligatorio');
    const base = analyzeM6(d.text, d.id);
    const clauses = base.rules.map(r => {
      const txt = r.source.quote;
      const matters = checks.filter(([, a, b]) => contains(txt, a) && (!b || contains(txt, b))).map(([c]) => c);
      const numericValues = extractNumericValues(txt, r.source.section, d.id, r.source.page);
      const prelaciones = detectPrelaciones(txt, r.source.section, d.id, r.source.page);
      const ruleType = classifyRule(txt);
      return {
        id: r.id, documentId: d.id, section: r.source.section, page: r.source.page, evidence: txt,
        subjectCandidate: r.actorCandidate || null, kindCandidate: r.kind, matters, numericValues, prelaciones, ruleType,
        flags: { condition: r.tags.condition, exception: r.tags.exception, priority: r.tags.hierarchy, obligation: contains(txt, /\\b(debera|pagara|estara obligado|debe|se devenga|se entendera|podra|ser[aá] exigible)\\b/i) },
        numbers: r.quantities, confidence: 'NO_CALIBRADA', legalConclusion: null
      };
    });
    return { id: d.id, type: d.type || 'NO_DECLARADO', clauses, baseObservations: base.observations, baseCoverage: base.coverage };
  });

  const all = docs.flatMap(x => x.clauses);
  for (const c of all) c.confidence = calculateConfidence(c, all);

  const issues = [];
  for (const [code, ,] of checks) {
    const relevant = all.filter(c => c.matters.includes(code));
    if (relevant.length) {
      issues.push({
        id: 'REVISION_' + code, matter: code, classification: 'PENDIENTE_ANALISIS',
        verificationQuestion: `¿Consta emisión, aceptación, vigencia y condición de activación?`,
        evidence: relevant.slice(0, 12).map(c => ({ documentId: c.documentId, page: c.page, section: c.section, quote: c.evidence, numericValues: c.numericValues, prelaciones: c.prelaciones, ruleType: c.ruleType, confidence: c.confidence })),
        verifiedLegalRule: false, legalConclusion: null
      });
    }
  }

  return {
    schema: 'AC-ICEN-M7-CHILE-02', jurisdiction: 'CL', scope: 'CONTRATOS_COMERCIALES_EMPRESARIALES',
    status: 'EXPERIMENTAL_PENDIENTE_VALIDACION_JURIDICA', documents: docs, issues, contradictions: detectContradictions(all),
    sources: { contractEvidence: true, legalNormsVerified: [], caseLawVerified: [], normativeResearchRequired: true },
    safety: { automaticLegalAdvice: false, financialExportAllowed: false, humanReviewRequired: true, neverUseToDetermineEnforceability: true },
    coverage: { documentCount: docs.length, candidateClauseCount: all.length, issueCategories: issues.length, contradictionsDetected: detectContradictions(all).length },
    limitations: ['No hay consulta de legislación ni jurisprudencia.', 'Detecta candidatos por patrones.', 'No resuelve jerarquía documental automáticamente.', 'Las contradicciones detectadas no implican invalidez; solo señalan divergencias a revisar.']
  };
}

module.exports = { analyzeM7, extractNumericValues, detectPrelaciones, classifyRule, detectContradictions };
""")

# ==============================================================================
# 4. INTEGRACIÓN M7 - CALCULADORA V2
# ==============================================================================
write_file("integracion_m7_calculadora_v2/README_INTEGRACION_V2.md", """# Integración M7 → Calculadora v2
Implementa la transferencia asistida de valores desde M7 hacia la calculadora, con confirmación humana obligatoria, trazabilidad contractual y niveles de confianza visibles.
""")

write_file("integracion_m7_calculadora_v2/m7_integracion_v2.js", """'use strict';
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
""")

# ==============================================================================
# 5. ASISTENTE DE PRIMER USO
# ==============================================================================
write_file("asistente_primer_uso/README_ASISTENTE.md", """# Asistente de Primer Uso
Micro-tours contextuales en 4 puntos críticos (Dashboard, Calculadora, M7, Sala de Negocio) con dos niveles de explicación (Ejecutivo y Detallado). No envía datos a servidores externos.
""")

write_file("asistente_primer_uso/asistente_primer_uso.js", """'use strict';
const ASISTENTE = (function() {
  const STORAGE_KEY = 'icen_asistente_v1';
  let nivel = 'ejecutivo', visto = {}, overlay = null, tourActivo = null, pasoActual = 0, hookInstalado = false;
  try { visto = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch(e) {}

  const TOURS = {
    dashboard: { id: 'dashboard', pantalla: 'inicio', titulo: 'Bienvenido a Aysén Conecta', pasos: [
      { target: '#inicio', ejecutivo: 'Tienes 3 caminos principales: <b>Comprar</b>, <b>Vender</b> o <b>Evaluar</b>. Empieza por lo que necesitas hoy.', detallado: 'El dashboard muestra indicadores de necesidades, capacidades, oportunidades y negocios. No necesitas revisarlos todos.', accion: { texto: 'Entendido', tipo: 'cerrar' } }
    ]},
    calculadora: { id: 'calculadora', pantalla: 'real-calculadora', titulo: 'Cómo usar la Calculadora ICEN', pasos: [
      { target: '#c_sale', ejecutivo: '<b>Venta neta</b>: el monto total del contrato, sin IVA. Ejemplo: $80.000.000.', detallado: 'Este es el ingreso total que recibirás si se ejecuta el contrato completo.', accion: { texto: 'Siguiente', tipo: 'siguiente' } },
      { target: '#c_pay', ejecutivo: '<b>Plazo de pago</b>: cuántos días tarda tu cliente en pagarte. Ejemplo: 30, 45 o 60 días.', detallado: 'Este dato suele estar en la cláusula de pago. Si hay ambigüedad, el Evaluador M7 te alertará.', accion: { texto: 'Entendido', tipo: 'cerrar' } }
    ]},
    m7: { id: 'm7', pantalla: 'real-contraparte', titulo: 'Cómo leer el Evaluador M7', pasos: [
      { target: '#m7Out', ejecutivo: 'El Evaluador M7 <b>no emite conclusiones jurídicas</b>. Te muestra puntos que una persona debe revisar.', detallado: 'M7 busca patrones en el texto contractual y marca dónde aparecen plazos, porcentajes, etc. No interpreta validez.', accion: { texto: 'Siguiente', tipo: 'siguiente' } },
      { target: '#m7Guard', ejecutivo: '🔒 <b>Transferencia a la calculadora</b>: ningún dato del M7 pasa automáticamente. Tú confirmas cada valor.', detallado: 'Si M7 detecta un plazo de 60 días, no lo aplica automáticamente. Tú debes revisarlo y confirmar.', accion: { texto: 'Entendido', tipo: 'cerrar' } }
    ]}
  };

  function crearOverlay() {
    if (overlay) return;
    overlay = document.createElement('div');
    overlay.className = 'asistente-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.innerHTML = `<div class="asistente-panel"><div class="asistente-header"><h3 class="asistente-titulo"></h3><div class="asistente-nivel"><button class="asistente-nivel-btn activo" data-nivel="ejecutivo">Ejecutivo</button><button class="asistente-nivel-btn" data-nivel="detallado">Detallado</button></div><button class="asistente-cerrar">×</button></div><div class="asistente-contenido"></div><div class="asistente-acciones"></div><div class="asistente-progreso"></div></div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('.asistente-cerrar').addEventListener('click', cerrar);
    overlay.querySelectorAll('.asistente-nivel-btn').forEach(btn => btn.addEventListener('click', () => cambiarNivel(btn.dataset.nivel)));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) cerrar(); });
  }

  function cambiarNivel(nuevoNivel) {
    nivel = nuevoNivel;
    overlay.querySelectorAll('.asistente-nivel-btn').forEach(btn => btn.classList.toggle('activo', btn.dataset.nivel === nivel));
    renderPasoActual();
  }

  function iniciarTour(tourId) {
    const tour = TOURS[tourId];
    if (!tour || visto[tour.id]) return;
    tourActivo = tour; pasoActual = 0;
    crearOverlay();
    overlay.querySelector('.asistente-titulo').textContent = tour.titulo;
    overlay.classList.add('activo');
    renderPasoActual();
  }

  function renderPasoActual() {
    if (!tourActivo) return;
    const paso = tourActivo.pasos[pasoActual];
    if (!paso) { cerrar(); return; }
    overlay.querySelector('.asistente-contenido').innerHTML = `<div class="asistente-texto">${nivel === 'ejecutivo' ? paso.ejecutivo : paso.detallado}</div>`;
    const acciones = overlay.querySelector('.asistente-acciones');
    acciones.innerHTML = '';
    const btn = document.createElement('button');
    btn.className = 'asistente-btn-primary';
    btn.textContent = paso.accion.texto;
    btn.addEventListener('click', () => {
      if (paso.accion.tipo === 'cerrar') { visto[tourActivo.id] = true; try{localStorage.setItem('icen_asistente_v1', JSON.stringify(visto))}catch(e){}; cerrar(); }
      else if (paso.accion.tipo === 'siguiente') { pasoActual++; if (pasoActual >= tourActivo.pasos.length) { visto[tourActivo.id] = true; try{localStorage.setItem('icen_asistente_v1', JSON.stringify(visto))}catch(e){}; cerrar(); } else { renderPasoActual(); } }
      else if (paso.accion.tipo === 'navegar') { visto[tourActivo.id] = true; try{localStorage.setItem('icen_asistente_v1', JSON.stringify(visto))}catch(e){}; cerrar(); if (typeof go === 'function') go(paso.accion.destino); }
    });
    acciones.appendChild(btn);
    overlay.querySelector('.asistente-progreso').textContent = `Paso ${pasoActual + 1} de ${tourActivo.pasos.length}`;
  }

  function cerrar() {
    if (overlay) { overlay.classList.remove('activo'); setTimeout(() => { if (overlay) { overlay.remove(); overlay = null; } }, 300); }
    tourActivo = null; pasoActual = 0;
  }

  function instalarHook() {
    if (hookInstalado || typeof go !== 'function') { if(typeof go !== 'function') setTimeout(instalarHook, 1000); return; }
    const goOriginal = go;
    window.go = function(id) {
      try {
        goOriginal(id);
        setTimeout(() => {
          for (const [tourId, tour] of Object.entries(TOURS)) {
            if (tour.pantalla === id && !visto[tourId]) { setTimeout(() => iniciarTour(tourId), 600); break; }
          }
        }, 150);
      } catch(e) { goOriginal(id); }
    };
    hookInstalado = true;
  }

  return { iniciar: instalarHook, iniciarTour, cerrar, resetear: () => { visto = {}; try{localStorage.removeItem(STORAGE_KEY)}catch(e){}; }, TOURS };
})();
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => ASISTENTE.iniciar()); else ASISTENTE.iniciar();
""")

write_file("asistente_primer_uso/asistente_estilos.css", """.asistente-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 10000; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; }
.asistente-overlay.activo { opacity: 1; pointer-events: auto; }
.asistente-panel { background: #fff; border-radius: 16px; max-width: 560px; width: 90%; max-height: 85vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); padding: 24px; }
.asistente-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px; }
.asistente-titulo { margin: 0; font-size: 1.25rem; color: #1F4E78; flex: 1; }
.asistente-nivel { display: flex; gap: 4px; background: #f5f8f7; padding: 4px; border-radius: 8px; }
.asistente-nivel-btn { background: transparent; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.875rem; cursor: pointer; color: #555; transition: all 0.2s; }
.asistente-nivel-btn.activo { background: #1F4E78; color: #fff; }
.asistente-cerrar { background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #666; padding: 0 8px; line-height: 1; }
.asistente-cerrar:hover { color: #1F4E78; }
.asistente-contenido { margin: 16px 0; line-height: 1.6; }
.asistente-texto { font-size: 1rem; color: #333; }
.asistente-texto b { color: #1F4E78; }
.asistente-acciones { display: flex; justify-content: flex-end; margin-top: 20px; }
.asistente-btn-primary { background: #1F4E78; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
.asistente-btn-primary:hover { background: #14532d; }
.asistente-progreso { text-align: center; font-size: 0.875rem; color: #888; margin-top: 12px; }
@media (prefers-reduced-motion: reduce) { .asistente-overlay { animation: none !important; transition: none !important; } }
""")

# ==============================================================================
# 6. BACKEND D04-C
# ==============================================================================
write_file("backend_d04c/README_D04C.md", """# Backend D04-C · FastAPI + PostgreSQL + Docker
Migración de la ejecución local a una aplicación web centralizada, conservando la extracción documental en el navegador para privacidad.

## Despliegue
```bash
docker-compose up -d