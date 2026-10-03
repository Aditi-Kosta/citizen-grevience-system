const BASE='http://127.0.0.1:8000/api/v1';
async function request(path,options={}){const r=await fetch(BASE+path,options);if(!r.ok){const t=await r.text();throw new Error(t||'Request failed')}return r.json()}
export const api={
 overview:()=>request('/analytics/overview'),
 complaints:()=>request('/complaints?page=1&page_size=100'),
 clusters:()=>request('/clusters'),
 predict:(text)=>request('/predictions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})}),
 create:(text)=>request('/complaints',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})}),
 batch:(form)=>request('/complaints/batch',{method:'POST',body:form}),
 health:()=>request('/health')
};
