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
</style><h1>Unfinished series editor</h1><p>Edit local records and download a new input. Dates and sources remain your own assertions.</p>
<label><input id="stale" type="checkbox"> Show dates needing review</label><div id="entries"></div>
<button id="download">Download edited dashboard</button><p id="status" role="status"></p>
<script type="application/json" id="data">"""
        + payload
        + """</script><script>
const data=JSON.parse(document.getElementById('data').textContent);const cards=[];
function refresh(){for(const [item,card,bar,caption] of cards){const total=Number(item.total_volumes)||0,done=Number(item.completed_volumes)||0;
bar.max=total||1;bar.value=Math.min(done,total);caption.textContent=total?`${done} of ${total} completed`:'Total volumes unknown';
const stale=item.next_release&&item.next_release<data.as_of;
card.hidden=document.getElementById('stale').checked&&!stale;
}document.getElementById('status').textContent=`Review as of ${data.as_of}. Past release dates need verification; no dates were looked up.`;}
for(const item of data.series){const card=document.createElement('section');const title=document.createElement('h2');title.textContent=item.title;card.append(title);
const bar=document.createElement('progress');bar.setAttribute('aria-label',`Reading progress: ${item.title}`);const caption=document.createElement('p');card.append(bar,caption);
const fields=document.createElement('div');fields.className='fields';
for(const [key,labelText,type] of [['title','Title','text'],['completed_volumes','Completed volumes','number'],['total_volumes','Total volumes','number'],['owned_volumes','Owned volumes','number'],['next_release','Next release date (blank means unknown)','date'],['publisher','Publisher','text']]){
const label=document.createElement('label');label.textContent=labelText;const input=document.createElement('input');input.type=type;input.value=item[key]??'';
if(type==='number'){input.min='0';input.step='1';}input.addEventListener('input',()=>{if(type==='number'){if(input.value==='')delete item[key];else item[key]=Number(input.value);}else item[key]=type==='date'?(input.value||null):input.value;refresh();});label.append(input);fields.append(label);}
const label=document.createElement('label');label.textContent='Publication status';const select=document.createElement('select');
for(const status of ['incomplete','abandoned','delayed','still-writing','complete']){const option=document.createElement('option');option.value=status;option.textContent=status;select.append(option);}select.value=item.status;select.addEventListener('change',()=>item.status=select.value);label.append(select);fields.append(label);card.append(fields);
const noteLabel=document.createElement('label');noteLabel.textContent='Source and verification notes';const notes=document.createElement('textarea');notes.rows=3;notes.value=item.source_notes??'';notes.addEventListener('input',()=>item.source_notes=notes.value);noteLabel.append(notes);card.append(noteLabel);
cards.push([item,card,bar,caption]);document.getElementById('entries').append(card);}
document.getElementById('stale').addEventListener('change',refresh);document.getElementById('download').addEventListener('click',()=>{
for(const input of document.querySelectorAll('input')){if(!input.checkValidity()){input.reportValidity();return;}}
if(data.series.some(item=>!item.title||!item.title.trim())){document.getElementById('status').textContent='Every series needs a title.';return;}
const series=data.series.map(item=>Object.fromEntries(Object.entries(item).filter(([key])=>!['date_bucket','remaining_owned','remaining_total','progress_percent'].includes(key))));
const url=URL.createObjectURL(new Blob([JSON.stringify({version:1,series},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='edited-series-dashboard.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
document.getElementById('status').textContent='Downloaded a new input. Your original file is unchanged.';});refresh();</script></html>"""
    )
