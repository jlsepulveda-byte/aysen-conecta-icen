const {analyzeM7}=require('../fuentes/motor_m7');
const cases=[
 {name:'DOC-01 mismo objeto',a:'suministro',b:'suministro',expected:1},
 {name:'DOC-02 objetos distintos',a:'suministro',b:'mantencion',expected:0},
 {name:'DOC-03 sinonimia suministro/entrega de equipos',a:'suministro de equipos',b:'entrega de equipos',expected:1}
];
for(const t of cases){
 const docs=[{id:'CONTRATO',text:`Artículo 1 | Pagos\nEl pago de la factura de ${t.a} deberá realizarse dentro de 30 días corridos desde su recepción.`},{id:'ANEXO',text:`Artículo 1 | Pagos\nEl pago de la factura por ${t.b} deberá realizarse dentro de 45 días corridos desde su recepción.`}];
 const issues=analyzeM7({documents:docs}).issues.filter(x=>x.classification==='CONTRADICCION_DOCUMENTAL_CANDIDATA');
 const ok=issues.length===t.expected;
 console.log((ok?'APROBADA':'RECHAZADA')+' '+t.name+': '+issues.length+' alerta(s); esperado '+t.expected);
 if(!ok)process.exitCode=1;
}