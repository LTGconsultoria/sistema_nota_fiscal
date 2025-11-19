$(document).ready(function() {
    var selectedOption

    $('#coluna').change(function() {
        selectedOption = $(this).val();
        var options = '';
    
        if (selectedOption == 'setor_local' || selectedOption == 'setor_recebe') {
            console.log("ENTROU AQUI")
    
            data = cleanString('setoresJson')
            options += '<select class="form-select form-select-solid" data-control="select2" data-placeholder="Selecione o item" name="" id="itensSelect"><option value="" selected disabled>Selecione o tipo</option></select>';
            
            for (var i = 0; i < data.length; i++) {
              var item = data[i];
              var id = item.id
              var setor = item.setor + ' ' + item.unidade_nome
              //var setorId = item.setorId
        
              options += '<option value="' + id + '">' + setor + '</option>';
              
            }
        
            $('#itensSelect').html(options);
            options += '<option value=" " selected>Selecione o problema</option>';
    
        } else if (selectedOption == 'usuario' || selectedOption == 'usuario_atendime') {

            data = cleanString('usuariosJson')
            options += '<select class="form-select form-select-solid" data-control="select2" data-placeholder="Selecione o item" name="" id="itensSelect"><option value="" selected disabled>Selecione o tipo</option></select>';
            
            for (var i = 0; i < data.length; i++) {
              var item = data[i];
              var id = item.id
              var nome = item.nome
              //var setorId = item.setorId
              options += '<option value="' + id + '">' + nome + '</option>';
            }
        
            $('#itensSelect').html(options);
            options += '<option value=" " selected>Selecione o problema</option>';

        }
    });

    // Troca os none da string para null e aspas simples '' para aspas duplas ""
    // Transforma string em json para manipulação
    function cleanString(elementId) {
    var inputElement = document.getElementById(elementId);
    var data = inputElement.value;
    var cleanedString = data.replace(/'/g, '"');
    var cleanedString = data.replace(/None/g, 'null').replace(/'/g, '"');
    data = JSON.parse(cleanedString)
    return data
    }
});


