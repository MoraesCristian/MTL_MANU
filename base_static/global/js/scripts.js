document.addEventListener('DOMContentLoaded', function() {
    const abrirChamadoBtn = document.getElementById('abrirChamadoBtn');
    const chamadoDialog = document.getElementById('chamadoDialog');
    const passos = document.querySelectorAll('.passo');
    let passoAtual = 0;

    abrirChamadoBtn.addEventListener('click', function() {
        const hoje = new Date().toLocaleDateString();
        const numeroOrdem = '12345'; // Pode ser gerado dinamicamente

        document.getElementById('numeroOrdem').textContent = numeroOrdem;
        document.getElementById('dataAbertura').textContent = hoje;
        
        chamadoDialog.style.display = 'flex';
        atualizarPasso();
    });

    document.getElementById('empresa').addEventListener('change', function() {
        irParaProximoPasso();
    });

    document.getElementById('localizacaoAtv').addEventListener('change', function() {
        irParaProximoPasso();
    });

    document.getElementById('tipoManutencao').addEventListener('change', function() {
        const tipo = this.value;
        const detalhesDiv = document.getElementById('detalhesManutencao');
        detalhesDiv.innerHTML = ''; // Limpa os campos adicionais

        if (tipo === 'preventiva') {
            detalhesDiv.innerHTML = '<p>Relatório padrão para manutenção preventiva</p>';
        } else if (tipo === 'emergencial') {
            const select = document.createElement('select');
            select.name = 'tipoEmergencial';
            select.id = 'tipoEmergencial';
            select.innerHTML = `
                <option value="" selected disabled>Selecione</option>
                <option value="eletrica">Elétrica</option>
                <option value="hidraulica">Hidráulica</option>
                <option value="civil">Civil</option>
            `;
            detalhesDiv.appendChild(select);

            select.addEventListener('change', function() {
                const subTipo = this.value;
                const subDetalhesDiv = document.getElementById('subDetalhesManutencao');

                if (subDetalhesDiv) {
                    subDetalhesDiv.remove(); // Remove o div existente se houver
                }

                const novoSubDetalhesDiv = document.createElement('div');
                novoSubDetalhesDiv.id = 'subDetalhesManutencao';
                detalhesDiv.appendChild(novoSubDetalhesDiv);

                if (subTipo === 'eletrica') {
                    novoSubDetalhesDiv.innerHTML = `
                        <label for="tipoEletrica">Tipo de Elétrica:</label>
                        <select id="tipoEletrica" name="tipoEletrica">
                            <option value="" selected disabled>Selecione</option>
                            <option value="lampadas">Lâmpadas</option>
                            <option value="fios">Fios</option>
                            <!-- Adicione outras opções conforme necessário -->
                        </select>
                    `;
                }
                // Adicione outros subTipos aqui conforme necessário
            });
        } else if (tipo === 'corretiva') {
            detalhesDiv.innerHTML = '<p>Relatório padrão para manutenção corretiva</p>';
        }

        detalhesDiv.style.display = 'block';
        document.getElementById('gerarRelatorioBtn').style.display = 'block';
        irParaProximoPasso();
    });

    function irParaProximoPasso() {
        if (passoAtual < passos.length - 1) {
            passos[passoAtual].classList.remove('passo-ativo');
            passoAtual++;
            atualizarPasso();
        }
    }

    function atualizarPasso() {
        passos[passoAtual].classList.add('passo-ativo');
        document.getElementById('passosNav').innerHTML = '';
        passos.forEach((passo, index) => {
            const button = document.createElement('button');
            button.textContent = `Passo ${index + 1}`;
            button.disabled = index === passoAtual;
            button.addEventListener('click', function() {
                passos[passoAtual].classList.remove('passo-ativo');
                passoAtual = index;
                atualizarPasso();
            });
            document.getElementById('passosNav').appendChild(button);
        });

        if (passoAtual === passos.length - 1) {
            mostrarResumo();
        }
    }

    function mostrarResumo() {
        const resumoDiv = document.getElementById('resumoChamado');
        const empresa = document.getElementById('empresa').value;
        const localizacao = document.getElementById('localizacaoAtv').value;
        const tipoManutencao = document.getElementById('tipoManutencao').value;
        const tipoEmergencial = document.getElementById('tipoEmergencial') ? document.getElementById('tipoEmergencial').value : '';
        const tipoEletrica = document.getElementById('tipoEletrica') ? document.getElementById('tipoEletrica').value : '';

        resumoDiv.innerHTML = `
            <p><strong>Empresa/Filial:</strong> ${empresa}</p>
            <p><strong>Localização da Atividade:</strong> ${localizacao}</p>
            <p><strong>Tipo de Manutenção:</strong> ${tipoManutencao}</p>
            ${tipoEmergencial ? `<p><strong>Tipo Emergencial:</strong> ${tipoEmergencial}</p>` : ''}
            ${tipoEletrica ? `<p><strong>Tipo de Elétrica:</strong> ${tipoEletrica}</p>` : ''}
        `;
        resumoDiv.style.display = 'block';
    }

    document.getElementById('fecharBtn').addEventListener('click', function() {
        chamadoDialog.style.display = 'none';
        passos.forEach(passo => passo.classList.remove('passo-ativo'));
        passoAtual = 0;
    });

    document.getElementById('abrirChamadoBtnDialog').addEventListener('click', function() {
        // Lógica para criar o chamado
        alert('Chamado criado com sucesso!');
        chamadoDialog.style.display = 'none';
        passos.forEach(passo => passo.classList.remove('passo-ativo'));
        passoAtual = 0;
    });
});
