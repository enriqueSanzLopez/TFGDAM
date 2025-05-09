document.getElementById('lang').addEventListener('change', ()=>{
    document.cookie="lang="+document.getElementById('lang').value+"; path=/";
    window.location.href=window.location.href;
});