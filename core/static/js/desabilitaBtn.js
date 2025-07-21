/* Desabilita o botão do projeto ao realizar um submit */
document.addEventListener("DOMContentLoaded", function() {
    var forms = document.getElementsByClassName("getForm");
    for (var i = 0; i < forms.length; i++) {
        forms[i].addEventListener("submit", function() {
            var button = this.getElementsByClassName("disableOnSubmit")[0];
            if (button) {
                button.disabled = true;
            }
        });
    }
  });
  
  /* Desabilita o link ao clicar nele */
  document.addEventListener('DOMContentLoaded', function() {
    var links = document.querySelectorAll('.disableOnRedirect');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function(event) {
        var link = this;
        setTimeout(function() {
          link.classList.add('disabled');
          link.removeAttribute('href');
        }, 100);
      });
    }
  });

