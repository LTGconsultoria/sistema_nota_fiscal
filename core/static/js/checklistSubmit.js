//Gera o submit do form quando a avaliação for finalizada
document.addEventListener("DOMContentLoaded", function() {
    var modalButton = document.getElementById("confirmaChecklistBtn");

    modalButton.addEventListener("click", function() {
        document.getElementById("checklistForm").submit();
    });
});

//Gera o submit do form quando escolhido outro lugar para ser avaliado
document.addEventListener("DOMContentLoaded", function() {
    var modalButton = document.getElementById("localSubmitBtn");

    modalButton.addEventListener("click", function() {
        document.getElementById("checklistForm").submit();
    });
});