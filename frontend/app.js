const API = '/api';
const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labelStatus = (value) => ({NUEVO:'Nuevo',ASIGNADO:'Asignado',EN_PROCESO:'En proceso',RESUELTO:'Resuelto',CERRADO:'Cerrado'}[value] || value);
const labelPriority = (value) => ({CRITICA:'Crítica',ALTA:'Alta',MEDIA:'Media',BAJA:'Baja'}[value] || value);
let incidents = [];
let activeView = '';
let pageOffset = 0;
let pageHasMore = false;
let toastTimer;

async function request(path, options = {}) {
  const response = await fetch(API + path, {headers:{'Content-Type':'application/json'}, ...options});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'No se pudo completar la solicitud.');
  return result;
}
function toast(message) {
  const node = $('#toast'); node.textContent = message; node.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => node.classList.remove('show'), 2600);
}
function dateLabel(value) {
  const date = new Date(value);
  return new Intl.DateTimeFormat('es-GT', {day:'2-digit',month:'short'}).format(date).replace('.', '');
}
function avatarName(value) { return value.split(/\s+/).slice(0,2).map((part) => part[0] || '').join('').toUpperCase(); }

async function load(append = false) {
  const params = new URLSearchParams();
  for (const [key, id] of [['status','filter-status'],['priority','filter-priority'],['category','filter-category'],['technician','filter-technician']]) {
    if ($('#'+id).value) params.set(key, $('#'+id).value);
  }
  if (activeView === 'critical') params.set('priority', 'CRITICA');
  params.set('limit', '100');
  params.set('offset', append ? String(pageOffset) : '0');
  const [data, metrics, allIncidents] = await Promise.all([request('/incidents?'+params), request('/metrics'), request('/incidents?limit=100')]);
  const page = activeView === 'open' ? data.items.filter((item) => !['RESUELTO','CERRADO'].includes(item.status)) : data.items;
  incidents = append ? incidents.concat(page) : page;
  pageOffset = data.pagination.next_offset;
  pageHasMore = pageOffset !== null;
  renderRows(); renderMetrics(metrics); renderCharts(metrics); updateSelects(allIncidents.items);
}
function renderMetrics(m) {
  $('#nav-count').textContent = m.open;
  $('#metrics').innerHTML = [
    ['Incidentes abiertos',m.open,'En atención','↗','open'],
    ['Prioridad crítica',m.critical,'Requieren atención','◇','critical'],
    ['Incidentes cerrados',m.closed,'Resueltos y cerrados','✓','closed'],
    ['Total registrados',m.total,'Histórico completo','▤','total']
  ].map(([title,value,note,icon,kind]) => `<article class="metric ${kind}"><span class="metric-icon">${icon}</span><div class="metric-label">${title}</div><div class="metric-value">${value}</div><span class="metric-note">${note}</span></article>`).join('');
}
function renderBars(id, items, key) {
  const host = $(id); const max = Math.max(1, ...items.map((item) => item.count));
  host.innerHTML = items.length ? items.slice(0,5).map((item) => `<div class="bar-row"><span title="${escapeHtml(item[key])}">${escapeHtml(item[key])}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(5, item.count/max*100)}%"></div></div><b class="bar-num">${item.count}</b></div>`).join('') : '<span class="date">Sin datos</span>';
}
function renderCharts(m) { renderBars('#category-chart',m.by_category,'category'); renderBars('#technician-chart',m.by_technician,'technician'); }
function renderRows() {
  const search = $('#search').value.trim().toLocaleLowerCase('es');
  const items = incidents.filter((item) => !search || `${item.title} ${item.description} ${item.reporter} ${item.category} ${item.technician || ''}`.toLocaleLowerCase('es').includes(search));
  $('#list-count').textContent = items.length;
  $('#incident-rows').innerHTML = items.map((item) => `<tr>
    <td><span class="incident-title" data-open="${item.id}">${escapeHtml(item.title)}</span><span class="incident-id">INC-${String(item.id).padStart(4,'0')}</span></td>
    <td><span class="category">${escapeHtml(item.category)}</span></td><td><span class="priority ${item.priority}">${labelPriority(item.priority)}</span></td>
    <td><span class="status ${item.status}">${labelStatus(item.status)}</span></td>
    <td>${item.technician ? `<span class="person"><i class="person-dot">${escapeHtml(avatarName(item.technician))}</i>${escapeHtml(item.technician)}</span>` : '<span class="person none">Sin asignar</span>'}</td>
    <td><span class="date">${dateLabel(item.created_at)}</span></td><td><button class="row-menu" aria-label="Ver detalle" data-open="${item.id}">···</button></td></tr>`).join('');
  $('#empty-state').hidden = items.length > 0;
  $('#load-more').hidden = !pageHasMore;
}
function updateSelects(allIncidents) {
  const category = $('#filter-category'); const technician = $('#filter-technician');
  const currentCategory = category.value; const currentTech = technician.value;
  const categories = [...new Set(allIncidents.map((i) => i.category))].sort();
  const techs = [...new Set(allIncidents.map((i) => i.technician).filter(Boolean))].sort();
  category.innerHTML = '<option value="">Categoría: todas</option>' + categories.map((v) => `<option>${escapeHtml(v)}</option>`).join('');
  technician.innerHTML = '<option value="">Responsable: todos</option>' + techs.map((v) => `<option>${escapeHtml(v)}</option>`).join('') + '<option value="Sin asignar">Sin asignar</option>';
  category.value = currentCategory; technician.value = currentTech;
}
async function openDetail(id) {
  const item = await request(`/incidents/${id}`);
  const activity = item.activity.map((entry) => `<div class="activity-item"><b>${escapeHtml(entry.author)}</b><p>${escapeHtml(entry.message)}</p><small>${new Intl.DateTimeFormat('es-GT',{dateStyle:'medium',timeStyle:'short'}).format(new Date(entry.created_at))}</small></div>`).join('');
  $('#detail-content').innerHTML = `<div class="detail-head"><div class="eyebrow">INC-${String(item.id).padStart(4,'0')} · ${escapeHtml(item.category.toUpperCase())}</div><h2>${escapeHtml(item.title)}</h2><div class="detail-meta"><span class="priority ${item.priority}">${labelPriority(item.priority)}</span><span class="status ${item.status}">${labelStatus(item.status)}</span><span class="date">Reportado por ${escapeHtml(item.reporter)}</span></div><button class="close-button detail-close" aria-label="Cerrar">×</button></div>
    <div class="detail-body"><p class="detail-description">${escapeHtml(item.description)}</p><div class="detail-controls"><label>Estado<select id="detail-status">${['NUEVO','ASIGNADO','EN_PROCESO','RESUELTO','CERRADO'].map((s) => `<option ${s===item.status?'selected':''} value="${s}">${labelStatus(s)}</option>`).join('')}</select></label><label>Técnico asignado<input id="detail-tech" value="${escapeHtml(item.technician || '')}" placeholder="Nombre del técnico"></label></div>
    <button class="ghost-button" id="save-detail">Guardar cambios</button><div class="activity-title">Bitácora · ${item.activity.length} eventos</div>${activity || '<p class="date">Aún no hay actividad.</p>'}<form class="activity-form" id="activity-form"><label>Agregar comentario<input name="message" placeholder="Escribe una actualización..." required></label><button class="primary-button">Enviar</button></form></div>`;
  const dialog = $('#detail-dialog'); dialog.showModal();
  dialog.querySelector('.detail-close').onclick = () => dialog.close();
  $('#save-detail').onclick = async () => {
    try { await request(`/incidents/${id}`, {method:'PATCH',body:JSON.stringify({status:$('#detail-status').value,technician:$('#detail-tech').value})}); toast('Cambios guardados'); dialog.close(); await load(); }
    catch (error) { toast(error.message); }
  };
  $('#activity-form').onsubmit = async (event) => {
    event.preventDefault(); const message = new FormData(event.currentTarget).get('message');
    try { await request(`/incidents/${id}/activity`,{method:'POST',body:JSON.stringify({author:'Equipo de soporte',message})}); await openDetail(id); await load(); toast('Comentario agregado'); }
    catch (error) { toast(error.message); }
  };
}

$('#new-incident').onclick = () => $('#incident-dialog').showModal();
document.querySelectorAll('[data-close]').forEach((button) => button.onclick = () => $('#incident-dialog').close());
$('#incident-form').onsubmit = async (event) => {
  event.preventDefault(); const form = event.currentTarget; const payload = Object.fromEntries(new FormData(form));
  try { await request('/incidents',{method:'POST',body:JSON.stringify(payload)}); form.reset(); $('#incident-dialog').close(); $('#form-error').textContent=''; activeView=''; await load(); toast('Incidente creado correctamente'); }
  catch (error) { $('#form-error').textContent=error.message; }
};
['filter-status','filter-priority','filter-category','filter-technician'].forEach((id) => $('#'+id).onchange = () => { activeView=''; load().catch((e) => toast(e.message)); });
$('#search').oninput = renderRows;
$('#load-more').onclick = () => load(true).catch((e) => toast(e.message));
$('#reset-filters').onclick = () => { ['filter-status','filter-priority','filter-category','filter-technician'].forEach((id) => $('#'+id).value=''); $('#search').value=''; activeView=''; load().catch((e) => toast(e.message)); };
$('#view-open').onclick = () => { activeView='open'; $('#filter-status').value=''; load().catch((e) => toast(e.message)); };
$('#view-critical').onclick = () => { activeView='critical'; $('#filter-priority').value=''; load().catch((e) => toast(e.message)); };
$('#nav-dashboard').onclick = () => $('#dashboard-panel').scrollIntoView({behavior:'smooth',block:'center'});
$('#incident-rows').onclick = (event) => { const button = event.target.closest('[data-open]'); if (button) openDetail(button.dataset.open).catch((e) => toast(e.message)); };
load().catch((error) => { toast(error.message); $('#empty-state').hidden=false; });
