async function fetchSessions(limit=50){
  const res = await fetch(`/sessions?limit=${encodeURIComponent(limit)}`);
  if(!res.ok){ throw new Error("Sessions fetch failed: "+res.status); }
  return res.json();
}

function riskBadge(score){
  if(score === null || score === undefined) return '<span class="badge">—</span>';
  if(score < -0.2) return '<span class="badge risk-high">Yüksek</span>';
  if(score < 0.0)  return '<span class="badge risk-med">Orta</span>';
  return '<span class="badge risk-low">Düşük</span>';
}

function renderRows(list){
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = list.map(r => {
    const va = `${Number(r.voltaj).toFixed(0)}/${Number(r.akim).toFixed(1)}`;
    return `<tr>
      <td>${r.id}</td>
      <td>${r.userId}</td>
      <td>${Number(r.enerji).toFixed(2)}</td>
      <td>${r.sure}</td>
      <td>${va}</td>
      <td>${riskBadge(r.riskScore)} <small>${r.riskScore!=null?Number(r.riskScore).toFixed(3):""}</small></td>
      <td>${r.created_at}</td>
      <td><button data-id="${r.id}" class="stopBtn">Seansı Durdur</button></td>
    </tr>`;
  }).join("");
  // dummy action
  tbody.querySelectorAll(".stopBtn").forEach(btn => {
    btn.addEventListener("click", (e)=>{
      const id = e.currentTarget.getAttribute("data-id");
      alert("Seansı durdur (dummy): ID="+id+" — BE endpoint eklendiğinde gerçek çağrı yapılacak.");
    });
  });
}

async function refresh(){
  try{
    const limit = Number(document.getElementById("limitInput").value || 50);
    const data = await fetchSessions(limit);
    renderRows(data.sessions || []);
  }catch(err){
    console.error(err);
    alert("Yüklenirken hata: "+err.message);
  }
}

document.getElementById("refreshBtn").addEventListener("click", refresh);
window.addEventListener("load", refresh);
