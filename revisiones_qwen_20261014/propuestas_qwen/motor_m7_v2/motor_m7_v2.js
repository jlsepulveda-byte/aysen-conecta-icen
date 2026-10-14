'use strict';
const {analyzeM6} = require('./nucleo_m6');
const norm = s => String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const contains = (s,re) => re.test(norm(s));

const checks = [
  ['FORMACION_ORDEN', /\borden(?:es)?(?: de (?:servicio|compra))?\b/, /\baceptad|\bactiv|\bemitid|\bsilencio|\bsolicit|\bentendera|\bfalta de objecion|\binicio material/],
  ['EXCEPCIONES', /\bsalvo\b|\bexcepto\b|\bno operara\b|\bsin perjuicio\b|\ba excepcion\b/, null],
  ['JERARQUIA', /\bderogacion especifica\b|\bprevalec|\bprelacion\b|\bjerarquia\b/, null],
  ['PAGOS', /\bpago\b|\bfacturaci[oó]n\b|\bfactura\b/, /\bdias?\b|\bplazo\b/],
  ['GARANTIAS', /\bgarantia\b|\bboleta\b|\bpoliza\b/, null],
  ['RESPONSABILIDAD', /\bresponsabilidad\b|\bindemnizaci[oó]n\b/, null],
  ['CREDITOS_SERVICIO', /\bcreditos? de servicio\b|\bsla\b|\bniveles? de servicio\b/, null],
  ['ANTICIPO', /\banticipo\b|\bpago inicial\b|\breserva\b/, /\bporcentaje\b|\b%\b|\bdescuento\b/],
  ['RETENCION', /\bretenci[oó]n\b|\bfondo de garant[ií]a\b/, /\b%\b|\bliberaci[oó]n\b/],
  ['MULTA', /\bmulta\b|\bpenalidad\b|\bpenal\b/, /\bd[ií]a\b|\b%\b|\btope\b/],
  ['PLAZO_EJECUCION', /\bplazo de ejecuci[oó]n\b|\bduraci[oó]n\b|\bvigencia\b/, /\bd[ií]as?\b|\bmeses?\b/]
];

const prelacionPatterns = [
  { re: /\bprevalec(?:e|er[aá]|n)\s+sobre\b/i, tipo: 'PRELACION_EXPLICITA' },
  { re: /\bno\s+obstante\s+lo\s+(?:se[ñn]alado|dispuesto|indicado)\s+en\b/i, tipo: 'EXCEPCION_A_REGLA' },
  { re: /\bsalvo\s+(?:que|cuando|en\s+caso\s+de)\b/i, tipo: 'EXCEPCION_CONDICIONAL' },
  { re: /\bderogaci[oó]n\s+espec[ií]fica\b/i, tipo: 'MODIFICACION_FORMAL' },
  { re: /\banexo\s+[a-z]\b.*\bmodifica\b/i, tipo: 'MODIFICACION_POR_ANEXO' }
];

const exceptionPatterns = [/\bsalvo\b/i, /\bexcepto\b/i, /\bsin\s+perjuicio\b/i, /\bno\s+operar[aá]\b/i, /\ba\s+excepci[oó]n\b/i, /\bsiempre\s+que\b/i, /\bs[oó]lo\s+si\b/i, /\bcondicionad[oa]\b/i, /\ben\s+caso\s+de\b/i];

function extractNumericValues(text, section, documentId, page) {
  const values = [];
  const patterns = [
    { re: /(\d+(?:[.,]\d+)?)\s*d[ií]as?\s*(h[aá]biles|corridos|calendario)?/gi, tipo: 'DIAS' },
    { re: /(\d+(?:[.,]\d+)?)\s*%/g, tipo: 'PORCENTAJE' },
    { re: /\$\s*([\d\.]+(?:,\d+)?)/g, tipo: 'CLP' },
    { re: /(\d+)\s*meses?/gi, tipo: 'MESES' }
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
        flags: { condition: r.tags.condition, exception: r.tags.exception, priority: r.tags.hierarchy, obligation: contains(txt, /\b(debera|pagara|estara obligado|debe|se devenga|se entendera|podra|ser[aá] exigible)\b/i) },
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
