'use strict';
const ASISTENTE = (function() {
  const STORAGE_KEY = 'icen_asistente_v1';
  let nivel = 'ejecutivo', visto = {}, overlay = null, tourActivo = null, pasoActual = 0, hookInstalado = false;
  try { visto = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch(e) {}

  const TOURS = {
    dashboard: { id: 'dashboard', pantalla: 'inicio', titulo: 'Bienvenido a Aysén Conecta', pasos: [
      { target: 'body', ejecutivo: 'Tienes 3 caminos principales: <b>Comprar</b>, <b>Vender</b> o <b>Evaluar</b>. Empieza por lo que necesitas hoy.', detallado: 'El dashboard muestra indicadores de necesidades, capacidades, oportunidades y negocios. No necesitas revisarlos todos.', accion: { texto: 'Entendido', tipo: 'cerrar' } }
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
    if (overlay) { overlay.remove(); overlay = null; }
    tourActivo = null; pasoActual = 0;
  }

  function instalarHook() {
    if (hookInstalado || typeof go !== 'function') { if(typeof go !== 'function') setTimeout(instalarHook, 1000); return; }
    const goOriginal = go;
    window.go = function(id, ...args) {
      try {
        goOriginal.call(this, id, ...args);
        setTimeout(() => {
          for (const [tourId, tour] of Object.entries(TOURS)) {
            if (tour.pantalla === id && !visto[tourId]) { setTimeout(() => iniciarTour(tourId), 600); break; }
          }
        }, 150);
      } catch(e) { console.error('Asistente:', e); }
    };
    hookInstalado = true;
  }

  return { iniciar: instalarHook, iniciarTour, cerrar, resetear: () => { visto = {}; try{localStorage.removeItem(STORAGE_KEY)}catch(e){}; }, TOURS };
})();
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => ASISTENTE.iniciar()); else ASISTENTE.iniciar();
