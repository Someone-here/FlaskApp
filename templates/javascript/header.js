window.onscroll = function () { scrollFunction() };
const nav = document.querySelector('#navbar');
const logo = document.querySelector('#logo');
const anc = document.querySelectorAll('#navbar a')
if (screen.width <= 500) {
  logo.style.width = '4.25rem';
  logo.style.height = '3.75rem';
}
else {
    logo.style.width = '5.5rem';
    logo.style.height = '4.75rem';
}

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    nav.classList.add("nav-move");
    if (screen.width <= 500) {
        logo.style.width = '3.75rem';
        logo.style.height = '3.33rem';
        logo.style.marginLeft = "1rem";
        logo.style.marginRight = "1rem";
        logo.style.padd
        anc.forEach((e) => { e.style.fontSize = "0.8em" });
    }
    else {
        logo.style.width = '4.25rem';
        logo.style.height = '4rem';
        anc.forEach((e) => { e.style.fontSize = "0.8em" });
    }
    }
    else {
    nav.classList.remove("nav-move");
    if (screen.width <= 500) {
        logo.style.width = '4.25rem';
        logo.style.height = '3.75rem';
        anc.forEach((e) => { e.style.fontSize = "1em" });
    }
    else {
        logo.style.width = '5.5rem';
        logo.style.height = '4.75rem';
        anc.forEach((e) => { e.style.fontSize = "1em" });
    }
    }
}