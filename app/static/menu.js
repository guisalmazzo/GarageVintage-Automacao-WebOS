document.addEventListener('DOMContentLoaded', function() {
    let btnMenu = document.getElementById('btn-menu');
    let menuMobile = document.getElementById('menu-mobile');
    let btnFecharMenu = document.getElementById('btn-fechar-menu');
    let overlayMenu = document.getElementById('overlay-menu');
    let linksMenuMobile = document.querySelectorAll('.menu-mobile-content ul li a');

    btnMenu.addEventListener('click', () => {
        console.log('Botão Menu clicado');
        menuMobile.classList.add('abrir-menu');
        overlayMenu.style.display = 'block';
    });

    btnFecharMenu.addEventListener('click', () => {
        console.log('Botão Fechar Menu clicado');
        menuMobile.classList.remove('abrir-menu');
        overlayMenu.style.display = 'none';
    });

    overlayMenu.addEventListener('click', () => {
        console.log('Overlay clicado');
        menuMobile.classList.remove('abrir-menu');
        overlayMenu.style.display = 'none';
    });

    linksMenuMobile.forEach(link => {
        link.addEventListener('click', () => {
            console.log('Link do Menu Móvel clicado');
            menuMobile.classList.remove('abrir-menu');
            overlayMenu.style.display = 'none';
        });
    });
});


