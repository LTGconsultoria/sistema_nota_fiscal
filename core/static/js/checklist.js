//Setor para Local
$('#setorSelect').change(function() {
    selectedSector = parseInt($(this).val());
    var options = '';
    data = cleanString('localJson')
    options += '<option value=" " selected>Selecione o tipo</option>';

    for (var i = 0; i < data.length; i++) {
        var item = data[i];
        var id = item.id
        var nome = item.local
        localSetor = item.setor
    
    
        if (selectedSector == localSetor) {
            options += '<option value="' + id + '">' + nome + '</option>';
        }
    }

    $('#localSelect').html(options);
    options += '<option value=" " selected>Selecione o problema</option>';
});
    

//Local para Item 
$('#localSelect').change(function() {
    selectedSector = parseInt($(this).val());
    var options = '';
    var localId = document.getElementById('localSelect').value;
    var item_local = 0

    data = cleanString('tipoProbJson')
    options += '<option value=" " selected>Selecione o tipo</option>';

    for (var i = 0; i < data.length; i++) {
        var item = data[i];
        var id = item.id
        var nome = item.nome
        item_local = item.local_id
        
        if (localId == item_local) {
            options += '<option value="' + id + '">' + nome + '</option>';
        }
    }

    $('#itemSelect').html(options);
    options += '<option value=" " selected>Selecione o problema</option>';
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