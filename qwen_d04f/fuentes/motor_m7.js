'use strict';
/**
 * AC-ICEN M7.01 — contracts under Chilean commercial law: evidence-first candidate analyzer.
 * Experimental. Does not issue binding legal opinions or claim normative verification.
 * Read-only, offline, deterministic. No network and no financial export.
 */
const {analyzeM6}=require('./nucleo_m6');
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const contains=(s,re)=>re.test(norm(s));
const checks=[
 ['FORMACION_ORDEN',/\borden(?:es)?(?: de (?:servicio|compra))?\b/,/\baceptad|\bactiv|\bemitid|\bsilencio|\bsolicit|\bentendera|\bfalta de objecion|\binicio material/],
 ['EXCEPCIONES',/\bsalvo\b|\bexcepto\b|\bno operara\b|\bsin perjuicio\b|\ba excepcion\b/,null],
 ['JERARQUIA',/\bderogacion especifica\b|\bprevalec|\bprelacion\b|\bjerarquia\b/,null],
 ['PAGOS',/\bpago\b|\bfacturaci[oó]n\b|\bfactura\b/,/\bdias?\b|\bplazo\b/],
 ['GARANTIAS',/\bgarantia\b|\bboleta\b|\bpoliza\b/,null],
 ['RESPONSABILIDAD',/\bresponsabilidad\b|\bindemnizaci[oó]n\b/,null],
 ['CREDITOS_SERVICIO',/\bcreditos? de servicio\b|\bsla\b|\bniveles? de servicio\b/,null]
];
const actionRe=/\b(debera|pagara|estara obligado|debe|se devenga|se entendera|podra|ser[aá] exigible)\b/i;
const exceptions=/\b(salvo|excepto|siempre que|unicamente|solo si|no operara|condicionad[oa])\b/i;
const controlQuestions={
 FORMACION_ORDEN:'¿Consta emisión, aceptación, vigencia y condición de activación de la orden?',
 EXCEPCIONES:'¿A qué regla, sujeto y supuesto se aplica la excepción?',
 JERARQUIA:'¿Se cumplieron las formalidades contractuales para modificar la cláusula?',
 PAGOS:'¿Cuál es el hecho que inicia el cómputo del plazo y cuál es el documento aplicable?',
 GARANTIAS:'¿La garantía implica inmovilización de efectivo o un instrumento diferente?',
 RESPONSABILIDAD:'¿Qué base de cálculo, exclusiones y período se aplican?',
 CREDITOS_SERVICIO:'¿Los porcentajes corresponden a ámbitos y bases comparables?'
};
function analyzeM7(input){
 if(!input||!Array.isArray(input.documents)||!input.documents.length)throw Error('Se requiere documents no vacío');
 const ids=input.documents.map(d=>d.id);
 if(ids.some(x=>typeof x!=='string'||!x.trim())||new Set(ids).size!==ids.length)throw Error('ID documental único obligatorio');
 const docs=input.documents.map(d=>{
  if(typeof d.text!=='string'||!d.text.trim())throw Error('Texto contractual obligatorio');
  const base=analyzeM6(d.text,d.id);
  const clauses=base.rules.map(r=>{
   const txt=r.source.quote;
   const matters=checks.filter(([,a,b])=>contains(txt,a)&&(!b||contains(txt,b))).map(([c])=>c);
   return {id:r.id,documentId:d.id,section:r.source.section,page:r.source.page,evidence:txt,
    subjectCandidate:r.actorCandidate||null,kindCandidate:r.kind,matters,
    flags:{condition:r.tags.condition,exception:r.tags.exception,priority:r.tags.hierarchy,obligation:contains(txt,actionRe)},
    numbers:r.quantities,confidence:'NO_CALIBRADA',legalConclusion:null};
  });
  return {id:d.id,type:d.type||'NO_DECLARADO',clauses,baseObservations:base.observations,baseCoverage:base.coverage};
 });
 const all=docs.flatMap(x=>x.clauses);
 const issues=[];
 for(const [code,,] of checks){
  const relevant=all.filter(c=>c.matters.includes(code));
  if(relevant.length)issues.push({id:'REVISION_'+code,matter:code,classification:'PENDIENTE_ANALISIS',
   verificationQuestion:controlQuestions[code],evidence:relevant.slice(0,12).map(c=>({documentId:c.documentId,page:c.page,section:c.section,quote:c.evidence})),
   verifiedLegalRule:false,legalConclusion:null});
 }
 // Compare only potentially matching payment subjects. Distinct expressly named
 // invoice objects are not contradictory simply because their deadlines differ.
 function paymentSubject(text){
  const q=norm(text);
  const m=q.match(/\bfactura\s+(?:de|del|por|correspondiente a)\s+([a-z][a-z ]{2,48}?)(?=\s+(?:y\s+)?debera|\s+sera|\s+se pagara|\s+dentro de|[.,;]|$)/);
  if(!m)return null;
  const raw=m[1].trim().replace(/\s+/g,' ');
  // Equivalencia terminológica acotada: suministro/entrega de un mismo bien explícito.
  // No extrapolar equivalencias jurídicas ni eliminar distinciones de servicio.
  const equipment=raw.match(/^(?:suministro|entrega) de (equipos|maquinarias|materiales)$/);
  if(equipment)return 'BIEN:'+equipment[1];
  return raw;
 }
 // Explicit cross-document payment-term conflict; evidence only, not legal priority.
 const paymentTerms=[];
 for(const doc of docs){
  for(const clause of doc.clauses){
   const q=norm(clause.evidence);
   if(!/\b(pago|factura|facturacion)\b/.test(q))continue;
   const m=q.match(/(?:dentro de|plazo de|en un plazo de|a los)\s+(\d{1,4})\s+dias?\s*(corridos|habiles)?/);
   if(!m)continue;
   paymentTerms.push({documentId:doc.id,subject:paymentSubject(clause.evidence),days:Number(m[1]),dayType:m[2]||'NO_ESPECIFICADO',page:clause.page,section:clause.section,quote:clause.evidence});
  }
 }
 for(let i=0;i<paymentTerms.length;i++)for(let j=i+1;j<paymentTerms.length;j++){
  const a=paymentTerms[i],b=paymentTerms[j];
  if(a.documentId===b.documentId || a.days===b.days && a.dayType===b.dayType)continue;
  if(a.subject && b.subject && a.subject!==b.subject)continue;
  // Explicit amendment is not automatically a contradiction; it is a
  // candidate modification requiring confirmation of validity and hierarchy.
  const amendmentRe=/(?:se modifica|modifica expresamente|se sustituye|sustituye expresamente|reemplaza expresamente|queda reemplazad[oa])[^.\n]{0,130}(?:plazo|clausula|pago)|(?:plazo|clausula|pago)[^.\n]{0,130}(?:se modifica|se sustituye|se reemplaza)/;
  const changed=[a,b].find(x=>amendmentRe.test(norm(x.quote)));
  if(changed){
   issues.push({id:'MODIFICACION_EXPRESA_PLAZO_'+issues.length,matter:'PAGOS',classification:'MODIFICACION_DOCUMENTAL_CANDIDATA',
    verificationQuestion:'¿El anexo identifica la cláusula sustituida y cumple los requisitos de modificación y prelación?',
    evidence:[a,b].map(x=>({documentId:x.documentId,page:x.page,section:x.section,quote:x.quote})),
    comparedTerms:[{documentId:a.documentId,days:a.days,dayType:a.dayType},{documentId:b.documentId,days:b.days,dayType:b.dayType}],
    verifiedLegalRule:false,legalConclusion:null});
   continue;
  }
  issues.push({id:'CONTRADICCION_PLAZO_PAGO_'+issues.length,matter:'PAGOS',classification:'CONTRADICCION_DOCUMENTAL_CANDIDATA',
   verificationQuestion:'¿Qué plazo y documento prevalece para el mismo supuesto de pago?',
   evidence:[a,b].map(x=>({documentId:x.documentId,page:x.page,section:x.section,quote:x.quote})),
   comparedTerms:[{documentId:a.documentId,days:a.days,dayType:a.dayType},{documentId:b.documentId,days:b.days,dayType:b.dayType}],
   verifiedLegalRule:false,legalConclusion:null});
 }
 // A missing issue does not prove absence. No 'pass' status without external legal validation.
 return {schema:'AC-ICEN-M7-CHILE-01',jurisdiction:'CL',scope:'CONTRATOS_COMERCIALES_EMPRESARIALES',
  status:'EXPERIMENTAL_PENDIENTE_VALIDACION_JURIDICA',documents:docs,issues,
  sources:{contractEvidence:true,legalNormsVerified:[],caseLawVerified:[],normativeResearchRequired:true},
  safety:{automaticLegalAdvice:false,financialExportAllowed:false,humanReviewRequired:true,
   neverUseToDetermineEnforceability:true},
  coverage:{documentCount:docs.length,candidateClauseCount:all.length,issueCategories:issues.length},
  limitations:['No hay consulta de legislación ni jurisprudencia; no es un dictamen legal.',
   'Detecta candidatos por patrones; puede omitir artículos que no repiten la materia.',
   'No resuelve jerarquía documental, aplicabilidad jurídica, validez ni contradicciones por sí mismo.',
   'Las citas a documentos deben corroborarse visualmente con sus originales.']};
}
module.exports={analyzeM7};