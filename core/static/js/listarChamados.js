
  $(document).ready(function() {
    //Pega a atividade de todos os botões com os id's listados
    $('#geral, #aberto, #agendado, #finalizado, #andamento, #validacao, #esclarecimento').click(function() {
      
      
      //Botão que foi selecionado
      var statusSelected = $(this).attr('id');

      //Tabela de chamados
      var tableBody = $('#tableBody');
      tableBody.empty();

      //Input que esta no template de listar-chamado contendo o json dos chamados
      var inputElement = document.getElementById('jsonInput');
      var data = inputElement.value;

      // Troca os none da string para null e aspas simples '' para aspas duplas ""
      var cleanedString = data.replace(/None/g, 'null').replace(/'/g, '"');
      
      // Transforma string em json para manipulação
      data = JSON.parse(cleanedString)

      for (var i = 0; i < data.length; i++) {
        var item = data[i];
        const currentURL = window.location.href;
        const urlToKeep = currentURL.substring(0, currentURL.length - 15);

        //Condicao para tratar os links para usuarios e tecnicos
        if (currentURL.includes("usuario")) {
          var href = urlToKeep + `editar_chamado_usuario/${item.id}`

        } else {
          var href = urlToKeep + `editar_chamado/${item.id}`
        }

        // Executa a logica de deixar os chamados com a cor vermelha ou não
        if(item.updated_at  == "passou") {
          style = "background-color: lightcoral; color: white;"
        } else {
          style = style=""
        }

        //Troca o numero do status pelo nome
        if(item.status == 1) {
          status = '<td style="' + style + '"><span class="badge bg-success">Aberto</span></td>';

        } else if(item.status == 2) {
          status = '<td style="' + style + '"><span class="badge bg-danger">Finalizado</span></td>';
        
        } else if (item.status == 3) {
          status = '<td style="' + style + '"><span class="badge bg-warning">Em progresso</span></td>';
        
        } else if (item.status == 4) {
          status = '<td style="' + style + '"><span class="badge bg-info">Agendado</span></td>'; 

        } else if (item.status == 5) {
          status = '<td style="' + style + '"><span class="badge bg-secondary">Ag.Esclarecimento</span></td>'; 
        
        } else if (item.status == 6) {
          status = '<td style="' + style + '"><span class="badge bg-secondary">Ag.Validação</span></td>'; 
        }

        //Troca a cor da bedge de acordo com a prioridade
        if (item.prioridade == 'alta') {
          prioridade = '<td style="' + style + '"><span class="badge bg-danger">Alta</span></td>';
        } else if (item.prioridade == 'media') {
          prioridade = '<td style="' + style + '"><span class="badge bg-warning">Media</span></td>';
        } else if (item.prioridade == 'baixa') {
          prioridade = '<td style="' + style + '"><span class="badge bg-success">Baixa</span></td>';
        }

        // Condicoes para listar de acordo com o status, apenas chamados abertos, finalizados...
        if(statusSelected == 'aberto') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados abertos';

          if (item.status == 1){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }
        
        } else if (statusSelected == 'finalizado') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados finalizados';

          if (item.status == 2){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          } 

        } else if (statusSelected == 'andamento') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados em andamento';

          if (item.status == 3){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }

        } else if (statusSelected == 'agendado') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados agendados';

          if (item.status == 4){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }
        
        } else if (statusSelected == 'esclarecimento') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados em esclarecimento';
          
          if (item.status == 5){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }
        
        } else if(statusSelected == 'validacao') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados em validação';

          if (item.status == 6){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }

        } else if (statusSelected == 'geral') {
          var heading = document.getElementById("tituloListar");
          heading.textContent = 'Chamados gerais';

          var row = '<tr>' +
          '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
          '<td style="' + style + '">' + item.titulo + '</td>' +
          '<td style="' + style + '">' + item.problema + '</td>' +
          '<td style="' + style + '">' + item.setor_recebe + '</td>' +
          status +
          prioridade +
          '<td style="' + style + '">' + item.created_at + '</td>' +
          '<td style="' + style + '">' + item.m_sla + '</td>' +
          '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
        }
      }
    });
  });