$(document).ready(function() {
    var selectedSector
  
    $('#setor').change(function() {
        selectedSector = parseInt($(this).val());
        var options = '';
        data = cleanString('tipoProbJson')
        options += '<option value=" " selected>Selecione o tipo</option>';
  
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            var id = item.id
            var tipoProb = item.tipoProb
            var setorId = item.setorId
    
            if(setorId == selectedSector){
            options += '<option value="' + id + '">' + tipoProb + '</option>';
            }
        }
    
        $('#tipoProblema').html(options);
        options += '<option value=" " selected>Selecione o problema</option>';
    });
  
  
    $('#tipoProblema').change(function() {
      idSelected = parseInt($(this).val());
      var options = '';
  
      options += '<option value=" " selected>Selecione o problema</option>';
      dataProb = cleanString('probJson')
  
      for (var i = 0; i < dataProb.length; i++) {
        var item = dataProb[i];
        var id = item.id
        var problema = item.problema
        var tProblema = item.tipoProblema
        /* console.log(idSelected, tProblema) */
  
        if (idSelected == tProblema) {
          options += '<option value="' + id + '">' + problema + '</option>';
        }
  
      }
      console.log(options)
      
      $('#probSelect').html(options);
    
    });
  
    $('#setorLocalSelect').change(function() {
      idSelected = parseInt($(this).val());
      var options = '';
  
      options += '<option value=" " selected>Selecione o problema</option>';
      dataProb = cleanString('localJson')
  
      for (var i = 0; i < dataProb.length; i++) {
        var item = dataProb[i];
        var id = item.id
        var problema = item.local
        var tProblema = item.setor
        console.log(idSelected, tProblema)
  
        if (idSelected == tProblema) {
          options += '<option value="' + id + '">' + problema + '</option>';
        }
  
      }
      /* console.log(options) */
      $('#localChamadoSelect').html(options);
    
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