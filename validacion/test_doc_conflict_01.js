'use strict';
const {analyzeM7}=require('../fuentes/motor_m7');
const docs=[
{id:'CONTRATO',type:'CONTRATO',text:'Artículo 1 | Condiciones de pago\n1.1 El pago de la factura deberá realizarse dentro de 30 días corridos desde su recepción.'},
{id:'ANEXO',type:'ANEXO',text:'Artículo 1 | Condiciones de pago\n1.1 El pago de la factura deberá realizarse dentro de 45 días corridos desde su recepción.'}
];
const r=analyzeM7({documents:docs});
const evidence=JSON.stringify(r);
const contradiction=r.issues.some(x=>/contradic|conflict|inconsisten|discrepan/i.test(JSON.stringify(x)));
const result={test:'DOC-CONFLICT-01',expected:'Identificar contradicción entre 30 y 45 días',bothEvidenceFound:evidence.includes('30 días')&&evidence.includes('45 días'),explicitConflict:contradiction,humanReviewRequired:r.safety.humanReviewRequired,passed:contradiction};
console.log(JSON.stringify(result,null,2));
if(!result.passed)process.exitCode=1;
