from __future__ import annotations

import json
from typing import Any


def render_html(report: dict[str, Any]) -> str:
    payload = json.dumps(report).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Unfinished series editor</title><style>body{font:17px system-ui;max-width:1000px;margin:auto;padding:22px;background:#f5f1e8;color:#203442}
section{background:white;border:1px solid #b4c4ca;border-radius:12px;padding:18px;margin:18px 0}
.fields{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px}
label{display:block;margin:10px 0}input,select,textarea{font:inherit;box-sizing:border-box;max-width:100%;padding:9px}
.fields input,.fields select,textarea{width:100%}progress{width:100%;height:20px}button{font:inherit;background:#173d51;color:white;padding:12px;border:0;border-radius:6px}
</style><h1>Unfinished series editor</h1><p>Edit local records and download a new input. Dates and sources remain your own assertions. This page includes only the report's selected records. Changes stay in this page until you download; your original input is unchanged.</p>
<section aria-label="Add a series"><h2>Add a series</h2><form id="new-series"><div class="fields">
<label>Stable ID<input id="add-id" required></label><label>Series title<input id="add-title" required></label>
<label>Publication status<select id="add-status"><option>incomplete</option><option>abandoned</option><option>delayed</option><option>still-writing</option><option>complete</option></select></label>
</div><button id="add-series" type="submit">Add series</button></form><p>Choose a unique ID and keep it when comparing saved lists.</p></section>
<label><input id="stale" type="checkbox"> Show dates needing review</label><div id="entries"></div>
<button id="download" type="button">Download edited dashboard</button><p id="status" role="status"></p>
<script type="application/json" id="data">"""
        + payload
        + r"""</script><script>
const data = JSON.parse(document.getElementById('data').textContent);
const statuses = ['incomplete','abandoned','delayed','still-writing','complete'];
const cards = [];
const message = document.getElementById('status');
function validDate(value) {
  if (value === null || value === '' || value === 'unknown') return true;
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith('0000-')) return false;
  const parsed = new Date(value + 'T00:00:00Z');
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0,10) === value;
}
function validateRecords(records) {
  const seen = new Set();
  for (const item of records) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) return 'Every series must be an object.';
    if (typeof item.id !== 'string' || !item.id.trim() || seen.has(item.id)) return 'Every series needs a unique, nonempty ID.';
    seen.add(item.id);
    if (typeof item.title !== 'string' || !item.title.trim()) return 'Every series needs a title.';
    if (!statuses.includes(item.status)) return 'Choose a supported publication status.';
    for (const key of ['completed_volumes','total_volumes','owned_volumes','priority']) {
      if (Object.hasOwn(item,key) && (!Number.isSafeInteger(item[key]) || item[key] < 0)) return 'Volume counts and priority must be non-negative safe integers.';
    }
    for (const key of ['publisher','source_notes','reader_status','notes']) {
      if (Object.hasOwn(item,key) && typeof item[key] !== 'string') return key + ' must be text.';
    }
    if (item.next_release !== undefined && !validDate(item.next_release)) return 'Next release dates must be YYYY-MM-DD or blank for unknown.';
  }
  return '';
}
function refresh() {
  for (const [item,card,bar,caption,title] of cards) {
    const total = Number(item.total_volumes) || 0, done = Number(item.completed_volumes) || 0;
    bar.max = total || 1; bar.value = Math.min(done,total);
    caption.textContent = total ? `${done} of ${total} completed` : 'Total volumes unknown';
    title.textContent = item.title;
    const stale = item.next_release && item.next_release !== 'unknown' && item.next_release < data.as_of;
    card.hidden = document.getElementById('stale').checked && !stale;
  }
  message.textContent = `${data.series.length} series. Review as of ${data.as_of}. Past release dates need verification; no dates were looked up.`;
}
function renderEntries() {
  cards.length = 0;
  document.getElementById('entries').replaceChildren();
  for (const item of data.series) {
    const card = document.createElement('section'); card.dataset.id = item.id;
    const title = document.createElement('h2'); title.textContent = item.title; card.append(title);
    const bar = document.createElement('progress'); bar.setAttribute('aria-label',`Reading progress: ${item.title}`);
    const caption = document.createElement('p'); card.append(bar,caption);
    const fields = document.createElement('div'); fields.className = 'fields';
    for (const [key,labelText,type] of [['title','Title','text'],['completed_volumes','Completed volumes','number'],['total_volumes','Total volumes','number'],['owned_volumes','Owned volumes','number'],['next_release','Next release date (blank means unknown)','date'],['publisher','Publisher','text']]) {
      const label = document.createElement('label'); label.textContent = labelText;
      const input = document.createElement('input'); input.type = type;
      input.value = type === 'date' && item[key] === 'unknown' ? '' : (item[key] ?? '');
      if (type === 'number') { input.min = '0'; input.max = String(Number.MAX_SAFE_INTEGER); input.step = '1'; }
      input.addEventListener('input',()=>{
        if (type === 'number') {
          if (input.value === '') delete item[key]; else item[key] = Number(input.value);
        } else item[key] = type === 'date' ? (input.value || null) : input.value;
        refresh();
      });
      label.append(input); fields.append(label);
    }
    const label = document.createElement('label'); label.textContent = 'Publication status';
    const select = document.createElement('select');
    for (const status of statuses) { const option = document.createElement('option'); option.value = status; option.textContent = status; select.append(option); }
    select.value = item.status; select.addEventListener('change',()=>{ item.status = select.value; refresh(); });
    label.append(select); fields.append(label); card.append(fields);
    const noteLabel = document.createElement('label'); noteLabel.textContent = 'Source and verification notes';
    const notes = document.createElement('textarea'); notes.rows = 3; notes.value = item.source_notes ?? '';
    notes.addEventListener('input',()=>item.source_notes = notes.value); noteLabel.append(notes); card.append(noteLabel);
    const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = 'Remove series';
    remove.setAttribute('aria-label',`Remove series: ${item.title}`);
    remove.addEventListener('click',()=>{ data.series.splice(data.series.indexOf(item),1); renderEntries(); }); card.append(remove);
    cards.push([item,card,bar,caption,title]); document.getElementById('entries').append(card);
  }
  refresh();
}
document.getElementById('new-series').addEventListener('submit',event=>{
  event.preventDefault();
  const item = {id:document.getElementById('add-id').value.trim(), title:document.getElementById('add-title').value, status:document.getElementById('add-status').value};
  const error = validateRecords([...data.series,item]);
  if (error) { message.textContent = error; return; }
  data.series.push(item); document.getElementById('new-series').reset(); renderEntries();
});
document.getElementById('stale').addEventListener('change',refresh);
document.getElementById('download').addEventListener('click',()=>{
  for (const input of document.querySelectorAll('#entries input')) {
    if (!input.checkValidity()) { input.reportValidity(); return; }
  }
  const error = validateRecords(data.series);
  if (error) { message.textContent = error; return; }
  const series = data.series.map(item=>Object.fromEntries(Object.entries(item).filter(([key])=>!['date_bucket','remaining_owned','remaining_total','progress_percent'].includes(key))));
  const url = URL.createObjectURL(new Blob([JSON.stringify({version:1,series},null,2)],{type:'application/json'}));
  const a = document.createElement('a'); a.href = url; a.download = 'edited-series-dashboard.json'; a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
  message.textContent = 'Downloaded a new input. Your original file is unchanged.';
});
renderEntries();</script></html>"""
    )
