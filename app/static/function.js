document.addEventListener('DOMContentLoaded', function () {
    let clickCount = 0; 

  
    document.getElementById('increaseFontBtn').addEventListener('click', function () {
        var bodyStyle = window.getComputedStyle(document.body, null).getPropertyValue('font-size');
        var currentSize = parseFloat(bodyStyle);

        if (clickCount < 3) {
           
            document.body.style.fontSize = (currentSize + 2) + 'px';
            clickCount++;
        } else {
          
            document.body.style.fontSize = ''; 
            clickCount = 0; 
        }
    });

    // Função para alternar para o modo escuro
    document.getElementById('darkModeBtn').addEventListener('click', function () {
        document.body.classList.toggle('dark-mode'); // Alterna a classe "dark-mode"
    });
});
