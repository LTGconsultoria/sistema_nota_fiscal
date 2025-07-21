$('#setoresJson').change(function() {
    selectedSector = parseInt($(this).val());
    var options = '';
    data = cleanString('itensJson')
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

    $('#itensJson').html(options);
    options += '<option value=" " selected>Selecione o problema</option>';
});