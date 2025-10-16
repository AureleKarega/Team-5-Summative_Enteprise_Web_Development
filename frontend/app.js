/* global Chart */
document.addEventListener('DOMContentLoaded', () => {
  const hourlyCtx = document.getElementById('chart-hourly');
  const scatterCtx = document.getElementById('chart-scatter');
  const heatmapCanvas = document.getElementById('heatmap');

  const runBtn   = document.getElementById('run');
  const resetBtn = document.getElementById('reset');

  const fromEl   = document.getElementById('from');
  const toEl     = document.getElementById('to');
  const hourEl   = document.getElementById('hour');
  const minFareEl= document.getElementById('minFare');
  const maxFareEl= document.getElementById('maxFare');

  // chart handles to destroy/redraw
  let hourlyChart = null;
  let scatterChart = null;

  // ---------- utilities ----------
  const randInt   = (n) => Math.floor(Math.random() * n);
  const randRange = (a, b) => a + Math.random() * (b - a);

  function mergeSort(arr){
    if(arr.length<=1) return arr.slice();
    const mid=Math.floor(arr.length/2);
    const L=mergeSort(arr.slice(0,mid)), R=mergeSort(arr.slice(mid));
    const out=[]; let i=0,j=0;
    while(i<L.length && j<R.length){ out.push(L[i]<=R[j]?L[i++]:R[j++]); }
    while(i<L.length) out.push(L[i++]);
    while(j<R.length) out.push(R[j++]);
    return out;
  }
  function percentile(sorted, p){ if(!sorted.length) return 0; const idx=Math.floor(p*(sorted.length-1)); return sorted[idx]; }

  // ---------- zero state ----------
  function zeroKPIs(){
    document.getElementById('kpi-trips').textContent = '0';
    document.getElementById('kpi-avg-speed').textContent = '0';
    document.getElementById('kpi-avg-fare').textContent  = '0';
    document.getElementById('kpi-p95-speed').textContent = '0';
  }

  function drawEmptyHourly(){
    if (hourlyChart) hourlyChart.destroy();
    const zeroes = Array(24).fill(0);
    hourlyChart = new Chart(hourlyCtx, {
      type:'bar',
      data:{
        labels:[...Array(24).keys()],
        datasets:[
          {label:'Trips', data: zeroes, backgroundColor:'#ffca28aa', borderRadius:4},
          {label:'Avg Speed (km/h)', type:'line', data: zeroes, borderColor:'#90caf9', tension:0.35}
        ]
      },
      options:{ plugins:{legend:{labels:{color:'#ddd'}}}, scales:{x:{ticks:{color:'#bbb'}}, y:{ticks:{color:'#bbb'}}} }
    });
  }

  function drawEmptyScatter(){
    if (scatterChart) scatterChart.destroy();
    scatterChart = new Chart(scatterCtx, {
      type:'scatter',
      data:{ datasets:[{ label:'Tip % vs Distance', data: [], backgroundColor:'#ffca28' }] },
      options:{
        plugins:{legend:{labels:{color:'#ddd'}}},
        scales:{
          x:{ title:{display:true,text:'Distance (km)',color:'#ddd'}, ticks:{color:'#aaa'}, grid:{color:'#333'} },
          y:{ title:{display:true,text:'Tip %',color:'#ddd'}, ticks:{color:'#aaa'}, grid:{color:'#333'} }
        }
      }
    });
  }

  function drawEmptyHeatmap(){
    const ctx = heatmapCanvas.getContext('2d');
    const W = heatmapCanvas.clientWidth || 600, H = 200;
    heatmapCanvas.width = W; heatmapCanvas.height = H;
    ctx.clearRect(0,0,W,H);
    // subtle empty grid
    const cols=12, rows=7, cw=W/cols, ch=H/rows;
    ctx.strokeStyle = '#2c2c2c';
    for(let i=0;i<=cols;i++){ ctx.beginPath(); ctx.moveTo(i*cw,0); ctx.lineTo(i*cw,H); ctx.stroke(); }
    for(let j=0;j<=rows;j++){ ctx.beginPath(); ctx.moveTo(0,j*ch); ctx.lineTo(W,j*ch); ctx.stroke(); }
    ctx.fillStyle='#9aa0a6'; ctx.font='12px system-ui'; ctx.fillText('No data – press Run to generate demo', 10, H-10);
  }

  function renderZeroState(){
    zeroKPIs();
    drawEmptyHourly();
    drawEmptyScatter();
    drawEmptyHeatmap();
  }

  // ---------- demo data render ----------
  function renderDemo(){
    // hourly trips + speeds
    const trips = Array.from({length:24}, () => 250 + randInt(300));
    const speeds = Array.from({length:24}, () => randRange(20, 45));
    const fares = Array.from({length:24}, () => randRange(10, 20));

    // KPIs derived from arrays (not arbitrary)
    const totalTrips = trips.reduce((a,b)=>a+b,0);
    const avgSpeed = speeds.reduce((a,b)=>a+b,0) / speeds.length;
    const avgFare = fares.reduce((a,b)=>a+b,0) / fares.length;
    const p95 = percentile(mergeSort(speeds), 0.95);

    document.getElementById('kpi-trips').textContent = totalTrips.toLocaleString();
    document.getElementById('kpi-avg-speed').textContent = avgSpeed.toFixed(1);
    document.getElementById('kpi-avg-fare').textContent  = avgFare.toFixed(1);
    document.getElementById('kpi-p95-speed').textContent = p95.toFixed(1);

    // redraw hourly
    if (hourlyChart) hourlyChart.destroy();
    hourlyChart = new Chart(hourlyCtx, {
      type:'bar',
      data:{
        labels:[...Array(24).keys()],
        datasets:[
          {label:'Trips', data: trips, backgroundColor:'#ffca28aa', borderRadius:4},
          {label:'Avg Speed (km/h)', type:'line', data: speeds, borderColor:'#90caf9', tension:0.35}
        ]
      },
      options:{ plugins:{legend:{labels:{color:'#ddd'}}}, scales:{x:{ticks:{color:'#bbb'}}, y:{ticks:{color:'#bbb'}}} }
    });

    // scatter points
    const pts = Array.from({length:120}, ()=>({x:randRange(0.2,30), y:randRange(5,30)}));
    if (scatterChart) scatterChart.destroy();
    scatterChart = new Chart(scatterCtx, {
      type:'scatter',
      data:{ datasets:[{ label:'Tip % vs Distance', data: pts, backgroundColor:'#ffca28' }] },
      options:{
        plugins:{legend:{labels:{color:'#ddd'}}},
        scales:{
          x:{ title:{display:true,text:'Distance (km)',color:'#ddd'}, ticks:{color:'#aaa'}, grid:{color:'#333'} },
          y:{ title:{display:true,text:'Tip %',color:'#ddd'}, ticks:{color:'#aaa'}, grid:{color:'#333'} }
        }
      }
    });

    // heatmap colored
    const ctx = heatmapCanvas.getContext('2d');
    const W = heatmapCanvas.clientWidth || 600, H = 200;
    heatmapCanvas.width = W; heatmapCanvas.height = H;
    ctx.clearRect(0,0,W,H);
    const cols=12, rows=7, cw=W/cols, ch=H/rows;
    for(let i=0;i<cols;i++){
      for(let j=0;j<rows;j++){
        const v = Math.random();
        ctx.fillStyle = `rgba(${200*v+55}, ${100+100*v}, ${50+150*v}, 0.9)`;
        ctx.fillRect(i*cw+1, j*ch+1, cw-2, ch-2);
      }
    }
    ctx.fillStyle='#ccc'; ctx.font='12px system-ui'; ctx.fillText('Demo Heatmap (no live data)', 10, H-10);
  }

  // ---------- filters ----------
  function initFiltersToBlank(){
    // Hour options
    hourEl.innerHTML = '<option value="">All</option>' + Array.from({ length: 24 }, (_, i) => `<option value="${i}">${i}</option>`).join('');
    // Clear values (so you truly see blank/zero on load/reset)
    fromEl.value = '';
    toEl.value = '';
    hourEl.value = '';
    minFareEl.value = '';
    maxFareEl.value = '';
  }

  // ---------- button bindings ----------
  runBtn.addEventListener('click', (e) => {
    e.preventDefault();
    renderDemo();
  });

  resetBtn.addEventListener('click', (e) => {
    e.preventDefault();
    initFiltersToBlank();
    renderZeroState();
  });

  // ---------- boot ----------
  initFiltersToBlank();   // blank inputs
  renderZeroState();      // zeros and empty visuals
});
