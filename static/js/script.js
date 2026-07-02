const formulario = document.getElementById("formComanda");
const mensagem = document.getElementById("mensagem");
const corpoTabela = document.getElementById("corpoTabela");
const btnCadastrar = document.getElementById("btnCadastrar");
const btnCancelarEdicao = document.getElementById("btnCancelarEdicao");

let idEmEdicao = null;
let comandasAtuais = []; 


if (corpoTabela) {
    atualizarTabela();
}


if (formulario) {
    formulario.addEventListener("submit", async function (event) {
        event.preventDefault();

        const cliente = document.getElementById("cliente").value.trim();
        const mesa = document.getElementById("mesa").value;
        const pedido = document.getElementById("pedido").value.trim();
        const quantidade = document.getElementById("quantidade").value;
        const valor = document.getElementById("valor").value;

        if (Number(quantidade) <= 0) {
            mostrarMensagem("A quantidade deve ser maior que zero.", false);
            return;
        }

        if (Number(valor) <= 0) {
            mostrarMensagem("Informe um valor válido.", false);
            return;
        }

        const dadosComanda = {
            cliente: cliente,
            mesa: mesa,
            pedido: pedido,
            quantidade: quantidade,
            valor: valor
        };

        try {
            let response;
            
            if (idEmEdicao === null) {
                response = await fetch('/api/comandas', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dadosComanda)
                });
            } else {
                response = await fetch(`/api/comandas/${idEmEdicao}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dadosComanda)
                });
            }

            if (response.ok) {
                if (idEmEdicao === null) {
                    mostrarMensagem("Comanda cadastrada com sucesso!", true);
                } else {
                    mostrarMensagem("Comanda atualizada com sucesso!", true);
                    resetarEstadoFormulario();
                }
                formulario.reset();
                atualizarTabela();
            } else {
                mostrarMensagem("Erro ao salvar comanda.", false);
            }
        } catch (error) {
            console.error("Erro:", error);
            mostrarMensagem("Erro de conexão com o servidor.", false);
        }
    });
}

if (btnCancelarEdicao) {
    btnCancelarEdicao.addEventListener("click", function() {
        resetarEstadoFormulario();
        formulario.reset();
    });
}


async function atualizarTabela() {
    try {
        const response = await fetch('/api/comandas');
        comandasAtuais = await response.json(); // Alimenta o cache local
        
        corpoTabela.innerHTML = "";

        comandasAtuais.forEach(function (comanda) {
            corpoTabela.innerHTML += `
            <tr>
                <td>${comanda.cliente}</td>
                <td>${comanda.mesa}</td>
                <td>${comanda.pedido}</td>
                <td>${comanda.quantidade}</td>
                <td>R$ ${Number(comanda.valor).toFixed(2)}</td>
                <td>R$ ${Number(comanda.total).toFixed(2)}</td>
                <td>
                    <button style="padding: 8px 12px; font-size: 14px; background: #2980b9; margin-right: 5px;" onclick="prepararEdicao(${comanda.id})">
                        Editar
                    </button>
                    <button style="padding: 8px 12px; font-size: 14px; background: #8B0000;" onclick="removerComanda(${comanda.id})">
                        Excluir
                    </button>
                </td>
            </tr>
            `;
        });
    } catch (error) {
        console.error("Erro ao buscar comandas:", error);
    }
}


function prepararEdicao(id) {
    // Procura a comanda correspondente no cache local
    const comanda = comandasAtuais.find(c => c.id === id);
    if (!comanda) return;

    document.getElementById("cliente").value = comanda.cliente;
    document.getElementById("mesa").value = comanda.mesa;
    document.getElementById("pedido").value = comanda.pedido;
    document.getElementById("quantidade").value = comanda.quantidade;
    document.getElementById("valor").value = comanda.valor;

    idEmEdicao = id;
    btnCadastrar.textContent = "Salvar Alterações";
    btnCancelarEdicao.style.display = "inline-block";

    document.getElementById("cliente").focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetarEstadoFormulario() {
    idEmEdicao = null;
    btnCadastrar.textContent = "Cadastrar Comanda";
    btnCancelarEdicao.style.display = "none";
}


async function removerComanda(id) {
    if (idEmEdicao === id) {
        alert("Não pode excluir uma comanda que está a ser editada neste momento!");
        return;
    }

    if(confirm("Tem certeza que deseja excluir esta comanda?")) {
        try {
            const response = await fetch(`/api/comandas/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                mostrarMensagem("Comanda removida com sucesso!", true);
                atualizarTabela();
            } else {
                mostrarMensagem("Erro ao remover comanda.", false);
            }
        } catch (error) {
            console.error("Erro ao excluir:", error);
        }
    }
}


function mostrarMensagem(texto, sucesso) {
    if (!mensagem) return;

    mensagem.style.display = "block";
    mensagem.textContent = texto;

    if (sucesso) {
        mensagem.className = "sucesso";
    } else {
        mensagem.className = "erro";
    }

    setTimeout(function () {
        mensagem.style.display = "none";
    }, 3000);
}