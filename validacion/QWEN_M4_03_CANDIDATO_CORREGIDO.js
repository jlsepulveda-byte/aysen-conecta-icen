'use strict';
/**
 * AC-ICEN M4 generalización 03. Corrección P0-01.
 * Reconoce formato "Cláusula C1.", "Cláusula A1." además de formatos anteriores.
 */
const norm = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

const TERMS = {
  pago: /\b(pago|pagara|factura|vencimiento|cobro)\b/,
  garantia: /\b(garantia|boleta de garantia|poliza)\b/,
  credito_servicio: /\b(credito[s]? de servicio|penalidad|descuento por desempeno|sla)\b/,
  responsabilidad: /\b(responsabilidad|indemnizacion|limite de responsabilidad)\b/,
  combustible: /\b(combustible|diesel|petroleo)\b/,
  orden: /\b(orden de servicio|ordenes de servicio)\b/,
  anticipo: /\b(anticipo|pago inicial)\b/,
  retencion: /\b(retenci[oó]n|fondo de garant[ií]a)\b/,
  multa: /\b(multa|penalidad|penal)\b/,
  plazo_ejecucion: /\b(plazo de ejecuci[oó]n|plazo maximo para ejecutar|duraci[oó]n|vigencia)\b/
};

function runningLines(text) {
  const pg = text.split('\f');
  if (pg.length < 3) return { keys: new Set(), edge: new Set() };
  const c = new Map(), edge = new Set();
  pg.forEach((p, pi) => {
    const ls = p.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    const pos = [...ls.slice(0, 3), ...ls.slice(-3)];
    const seen = new Set();
    for (const l of pos) {
      // CORRECCIÓN P0-01: Excluir también formato "Cláusula Xn."
      if (/^(\d{1,2}\.\d{1,2}|art[ií]culo\s+\d+|anexo\s+[a-z]\b|cl[aá]usula\s+[a-z]\d*)/i.test(l)) continue;
      edge.add(pi + '|' + l);
      const k = l.replace(/\d+/g, '#').toLowerCase();
      if (!seen.has(k)) {
        seen.add(k);
        c.set(k, (c.get(k) || 0) + 1);
      }
    }
  });
  const min = Math.max(3, Math.ceil(pg.length * 0.6));
  return { keys: new Set([...c].filter(([, v]) => v >= min).map(([k]) => k)), edge };
}

function segment(text) {
  if (typeof text !== 'string' || !text.trim()) throw Error('Se requiere texto contractual');
  const running = runningLines(text);
  let page = 1, section = 'SIN_SECCION', out = [], buf = [];
  
  function flush() {
    const t = buf.join(' ').replace(/\s+/g, ' ').trim();
    if (t) out.push({ page, section, text: t });
    buf = [];
  }
  
  for (const raw of text.split(/(\f|\r?\n)/)) {
    if (raw === '\f') { flush(); page++; continue; }
    if (/^\r?\n$/.test(raw)) { flush(); continue; }
    const line = raw.trim();
    if (!line) continue;
    
    // CORRECCIÓN P0-01: Reconocer "Cláusula C1.", "Cláusula A1.", etc.
    const art = line.match(/^art[ií]culo\s+(\d+)\b/i);
    const cl = line.match(/^(\d{1,2}\.\d{1,2})\b/);
    const ann = line.match(/^anexo\s+([a-z])\b/i);
    const clausula = line.match(/^cl[aá]usula\s+([a-z]\d*)\.?/i); // NUEVO
    
    if (art || cl || ann || clausula) {
      flush();
      if (clausula) section = 'CLAUSULA ' + clausula[1].toUpperCase();
      else if (cl) section = 'CLAUSULA ' + cl[1];
      else if (art) section = 'ARTICULO ' + art[1];
      else if (ann) section = 'ANEXO ' + ann[1].toUpperCase();
    }
    
    // Filtrar encabezados repetidos
    if (!(running.keys.has(line.replace(/\d+/g, '#').toLowerCase()) && running.edge.has((page - 1) + '|' + line))) {
      buf.push(line);
    }
  }
  flush();
  return out;
}

function extract(text, documentId = 'DOCUMENTO_SIN_ID') {
  const nodes = segment(text);
  const facts = [];
  
  for (const n of nodes) {
    const t = norm(n.text);
    const topics = Object.entries(TERMS).filter(([, re]) => re.test(t)).map(([k]) => k);
    if (!topics.length) continue;
    
    const quantities = [...n.text.matchAll(/(?:\$\s*[\d\.]+(?:,\d+)?|\b\d+(?:[,.]\d+)?\s*%|\b\d+\s+d[ií]as?(?:\s+(?:h[aá]biles|corridos|calendario))?)/gi)].map(x => ({ raw: x[0], start: x.index }));
    const explicitCondition = /\b(si|siempre que|cuando|s[oó]lo si|en caso de|durante el cual|a condici[oó]n de)\b/i.test(n.text);
    const exception = /\b(salvo|excepto|no aplicar[aá]|sin perjuicio|a excepci[oó]n|derogaci[oó]n espec[ií]fica)\b/i.test(n.text);
    const negation = /\b(no se|no constituye|no podr[aá]|no ser[aá]|no aplica|no operara|no operar[aá])\b/i.test(n.text);
    const actor = /\b(el mandante|el proveedor|las partes|el cliente|el contratista)\b/i.exec(n.text);
    
    for (const topic of topics) {
      facts.push({
        id: 'F' + String(facts.length + 1).padStart(4, '0'),
        topic,
        actor: actor ? actor[0] : null,
        conditionPresent: explicitCondition,
        exceptionPresent: exception,
        negationPresent: negation,
        quantities,
        source: { documentId, page: n.page, section: n.section, quote: n.text },
        status: 'EXTRACCION_CANDIDATA',
        approved: false
      });
    }
  }
  
  return {
    schema: 'AC-ICEN-M4-GENERALIZACION-03',
    documentId,
    nodes: nodes.length,
    facts,
    financialExport: { ready: false, reason: 'Extracción heurística no validada por revisión humana' },
    limitations: [
      'No interpreta prioridad jurídica, semántica profunda ni condiciones entre artículos.',
      'Los sujetos y condiciones se detectan por patrones; pueden omitirse o atribuirse incorrectamente.',
      'Los números extraídos no se asocian de forma concluyente con obligaciones.',
      'No existe extracción directa desde PDF ni cálculo financiero.'
    ]
  };
}

module.exports = { extract, segment };