$(document).ready(function() {
    var flag = true
    
    $('#localSetor').change(function() {
        var selectedSector = parseInt($(this).val());
        console.log(selectedSector)
        
        if(flag === true) {
            var options = '';
            data = cleanString('localJson')
            options += '<option value=" " selected>Selecione o local</option>';
            options += '<option value="0">Voltar</option>';
    
            for(var i = 0; i < data.length; i++) {
                var item = data[i];
                var localSetorId = item.setor
                var localId = item.id
                var localName = item.local
    
                if(localSetorId == selectedSector) {
                    options += '<option value="' + localId + '">' + localName + '</option>';
                }
            }

            $('#localSetor').html(options);
            flag = false
        }
        
        if(selectedSector == 0) {
            flag = true
            dataSetor = cleanString('setoresJson')
            options += '<option value=" " selected>Selecione o setor</option>';

            for(var i = 0; i < dataSetor.length; i++) {
                var item = dataSetor[i];
                var setorId = item.id
                var setorName = item.name
                options += '<option value="' + setorId + '">' + setorName + '</option>';
            }

            $('#localSetor').html(options);
        }
    });

    function cleanString(elementId) {
        // Troca os none da string para null e aspas simples '' para aspas duplas ""
        // Transforma string em json para manipulação
        var inputElement = document.getElementById(elementId);
        var data = inputElement.value;
        var cleanedString = data.replace(/'/g, '"');
        var cleanedString = data.replace(/None/g, 'null').replace(/'/g, '"');
        data = JSON.parse(cleanedString)
        return data
    }
});