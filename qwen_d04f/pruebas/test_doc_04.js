const {analyzeM7}=require('../fuentes/motor_m7');
const docs=[
{id:'CONTRATO',text:'Artículo 1 | Pagos\nEl pago de la factura de suministro deberá realizarse dentro de 30 días corridos desde su recepción.'},
{id:'ANEXO',text:'Artículo 1 | Pagos\nSe modifica expresamente el plazo de pago de la factura de suministro y deberá realizarse dentro de 45 días corridos desde su recepción.'}
];
const issues=analyzeM7({documents:docs}).issues;
let amendments=issues.filter(x=>x.classification==='MODIFICACION_DOCUMENTAL_CANDIDATA');
let conflicts=issues.filter(x=>x.classification==='CONTRADICCION_DOCUMENTAL_CANDIDATA');
const ok=amendments.length===1 && conflicts.length===0 && amendments[0].evidence.length===2;
console.log(JSON.stringify({case:'DOC-04',amendments:amendments.length,conflicts:conflicts.length,evidence:amendments[0]?.evidence,passed:ok},null,2));
if(!ok)process.exitCode=1;