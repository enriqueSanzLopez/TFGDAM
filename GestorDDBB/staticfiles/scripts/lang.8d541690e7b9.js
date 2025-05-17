let cookies = document.cookie.split("; ");
let langCookie = cookies.find(cookie => cookie.startsWith("lang="));
let langValue = langCookie ? langCookie.split("=")[1] : "es";
let langSelect = document.getElementById("lang");
if (langSelect) {
    langSelect.value = langValue;
}

document.getElementById('lang').addEventListener('change', () => {
    document.cookie = "lang=" + document.getElementById('lang').value + "; path=/";
    window.location.href = window.location.href;
});