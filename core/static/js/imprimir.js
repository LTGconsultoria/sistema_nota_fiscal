document.addEventListener("DOMContentLoaded", function() {
    var btnImprimir = document.getElementById("btnImprimir");
    btnImprimir.addEventListener("click", function() {
      window.print();
    });
  });