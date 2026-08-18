(function(){
  var CACHE_KEY = 'ysCryptoTickerCacheV1';
  var TTL_MS = 5 * 60 * 1000;                 // 5 min fresh
  var STALE_FALLBACK_MS = 24 * 60 * 60 * 1000;// 24h stale fallback on error
  var REFRESH_MS = 5 * 60 * 1000 + Math.floor(Math.random()*30000); // jitter
  var API = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=15&page=1&sparkline=false&price_change_percentage=24h';
  var trackEl = document.getElementById('ys-ct-track');
  var loadEl  = document.getElementById('ys-ct-loading');
  if(!trackEl) return;

  function fmtPrice(n){
    if(n == null || isNaN(n)) return '-';
    if(n >= 1000) return '$'+n.toLocaleString('en-US',{maximumFractionDigits:0});
    if(n >= 1)    return '$'+n.toLocaleString('en-US',{maximumFractionDigits:2});
    if(n >= 0.01) return '$'+n.toFixed(4);
    return '$'+n.toPrecision(2);
  }
  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];});}

  function render(coins){
    if(!coins || !coins.length) return;
    var html = '';
    for(var i=0;i<coins.length;i++){
      var c = coins[i];
      var chg = (c.price_change_percentage_24h == null) ? 0 : c.price_change_percentage_24h;
      var dir = chg >= 0 ? 'ys-ct-up' : 'ys-ct-dn';
      var arrow = chg >= 0 ? '▲' : '▼';
      html += '<span class="ys-ct-item">' +
              '<img src="'+esc(c.image)+'" alt="'+esc(c.symbol)+'" loading="lazy" width="20" height="20"/>' +
              '<span class="ys-ct-sym">'+esc(c.symbol)+'</span>' +
              '<span class="ys-ct-price">'+esc(fmtPrice(c.current_price))+'</span>' +
              '<span class="ys-ct-chg '+dir+'">'+arrow+' '+Math.abs(chg).toFixed(2)+'%</span>' +
              '</span>';
    }
    // Duplicate for seamless marquee loop
    trackEl.innerHTML = html + html;
    trackEl.style.display = 'inline-flex';
    if(loadEl) loadEl.style.display = 'none';
  }

  function readCache(){
    try{
      var raw = localStorage.getItem(CACHE_KEY);
      if(!raw) return null;
      var obj = JSON.parse(raw);
      if(!obj || !obj.t || !obj.d) return null;
      return obj;
    }catch(e){ return null; }
  }
  function writeCache(data){
    try{ localStorage.setItem(CACHE_KEY, JSON.stringify({t:Date.now(),d:data})); }catch(e){}
  }

  function fetchFresh(){
    if(typeof fetch !== 'function') return;
    fetch(API, {cache:'default', mode:'cors'})
      .then(function(r){ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
      .then(function(data){
        if(!Array.isArray(data) || !data.length) throw new Error('Empty');
        var slim = data.map(function(c){return{
          id:c.id, symbol:c.symbol, image:c.image,
          current_price:c.current_price,
          price_change_percentage_24h:c.price_change_percentage_24h
        };});
        writeCache(slim);
        render(slim);
      })
      .catch(function(){
        // Fallback: keep any cached render, or show stale up to 24h
        var c = readCache();
        if(c && (Date.now()-c.t) < STALE_FALLBACK_MS){
          render(c.d);
        } else if(loadEl){
          loadEl.textContent = 'Crypto prices temporarily unavailable.';
        }
      });
  }

  function boot(){
    var c = readCache();
    if(c){
      render(c.d); // instant paint from cache
      if((Date.now() - c.t) < TTL_MS) return scheduleNext(TTL_MS - (Date.now()-c.t));
    }
    fetchFresh();
    scheduleNext(REFRESH_MS);
  }
  function scheduleNext(delay){
    setTimeout(function(){ fetchFresh(); scheduleNext(REFRESH_MS); }, Math.max(30000, delay));
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();