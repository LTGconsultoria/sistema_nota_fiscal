document.addEventListener("DOMContentLoaded", function() {
    const loadingEl = document.querySelector("#loading-overlay");

    if (loadingEl) {
        console.log("Loading overlay found");
        // Mostrar a sobreposição de carregamento ao carregar a página
        loadingEl.classList.remove("hidden");

        // Ocultar a sobreposição após um pequeno atraso para garantir que o conteúdo seja carregado
        setTimeout(function() {
            loadingEl.classList.add("hidden");
            console.log("Loading overlay hidden");
        }, 1000); // Ajuste o tempo conforme necessário
    } else {
        console.log("Loading overlay not found");
    }
});
