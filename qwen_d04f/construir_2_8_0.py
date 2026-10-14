# Armado reproducible de AC-ICEN-MVP 2.8.0 PROPUESTA a partir de la base canónica 2.7.0 (que no se modifica).
import json,hashlib,os
W=os.path.dirname(os.path.abspath(__file__))+'/'
rd=lambda p:open(W+p,encoding='utf-8').read()
mods=[('motor_m4',rd('fuentes/motor_m4.js')),('relaciones',rd('fuentes/relaciones.js')),('nucleo_m6',rd('fuentes/nucleo_m6.js')),('motor_m7',rd('fuentes/motor_m7.js'))]
b='const ICEN=(function(){const modules={};const cache={};\n'+''.join('modules["%s"]=function(require,module,exports){\n%s\n};\n'%m for m in mods)
b+='function req(n){n=n.replace(/^\\.\\//,"");if(!modules[n])throw Error("Módulo no encontrado: "+n);if(!cache[n]){let m={exports:{}};cache[n]=m;modules[n](req,m,m.exports);}return cache[n].exports;}\nconst m7=req("motor_m7"),m6=req("nucleo_m6"),m4=req("motor_m4");return{analyzeM7:m7.analyzeM7,analyzeM6:m6.analyzeM6,segment:m4.segment};})();\n'
open(W+'fuentes/motor_m7_bundle.js','w',encoding='utf-8').write(b)
base=open(W+'base_canonica/AC-ICEN_MVP_2_7_0_20261013_CANONICA.html','rb').read()
open(W+'base_sha256.txt','w').write(hashlib.sha256(base).hexdigest())
s=base.decode('utf-8')
def rep(a,c):
    global s
    assert a in s,a[:60];s=s.replace(a,c,1)
rep('accept=".txt,.csv,.pdf"','accept=".txt,.csv,.pdf,.docx"');rep('en texto o PDF con texto','en PDF con texto, Word (.docx) o texto')
rep("<button class=\"btn secondary\" onclick=\"mvLoad('f')\">Estados financieros de prueba</button>","<button class=\"btn secondary\" onclick=\"mvLoad('f')\">Estados financieros de prueba</button><button class=\"btn\" onclick=\"m7LoadMaster()\">Contrato maestro (caso 2027-211)</button>")
rep('<div id="mvOut"></div>','<div id="mvOut"></div><div id="m7Out"></div>')
rep('MVP 2.7.0 · Evaluación, evidencia y calculadora','MVP 2.8.0 PROPUESTA · Evaluación, evidencia y calculadora');rep('MVP 2.7.0 · Base canónica de colaboración','MVP 2.8.0 · Propuesta sobre la base canónica 2.7.0');rep('<span>Aysén Conecta + ICEN · MVP 2.7.0</span>','<span>Aysén Conecta + ICEN · MVP 2.8.0 · PROPUESTA</span>')
lib=lambda p:rd(p).replace('</script','<\\/script')
blk='<script type="text/plain" id="lib-pdfjs">'+lib('lib/pdf.min.mjs')+'</script>\n<script type="text/plain" id="lib-pdfworker">'+lib('lib/pdf.worker.min.mjs')+'</script>\n<script>'+lib('lib/jszip.min.js')+'</script>\n<script>'+b+'</script>\n<script>'+rd('fuentes/lector_documental.js').replace("if(typeof module!=='undefined')module.exports=LECTOR;","")+'</script>\n<script>const M7_MASTER='+json.dumps(rd('casos/contrato_maestro_extraido.txt'),ensure_ascii=False).replace('</','<\\/')+';</script>\n<script>'+rd('fuentes/m7_integracion.js')+'</script>\n'
j=s.rfind('</body>');s=s[:j]+blk+s[j:]
open(W+'AC-ICEN-MVP_2.8.0_20261013_PROPUESTA.html','w',encoding='utf-8').write(s);print('2.8.0:',len(s.encode()),'bytes')