
const formulario = document.getElementById("formComanda");
const mensagem = document.getElementById("mensagem");
const corpoTabela = document.getElementById("corpoTabela");


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

        // Validação básica
        if (Number(quantidade) <= 0) {
            mostrarMensagem("A quantidade deve ser maior que zero.", false);
            return;
        }

        if (Number(valor) <= 0) {
            mostrarMensagem("Informe um valor válido.", false);
            return;
        }

        const novaComanda = {
            cliente: cliente,
            mesa: mesa,
            pedido: pedido,
            quantidade: quantidade,
            valor: valor
        };

        try {
            // Envia para o Backend (Flask)
            const response = await fetch('/api/comandas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novaComanda)
            });

            if (response.ok) {
                mostrarMensagem("Comanda cadastrada com sucesso!", true);
                formulario.reset();
                atualizarTabela();
            } else {
                mostrarMensagem("Erro ao cadastrar comanda.", false);
            }
        } catch (error) {
            console.error("Erro:", error);
            mostrarMensagem("Erro de conexão com o servidor.", false);
        }
    });
}

async function atualizarTabela() {
    try {
        const response = await fetch('/api/comandas');
        const comandas = await response.json();
        
        corpoTabela.innerHTML = "";

        comandas.forEach(function (comanda) {
            corpoTabela.innerHTML += `
            <tr>
                <td>${comanda.cliente}</td>
                <td>${comanda.mesa}</td>
                <td>${comanda.pedido}</td>
                <td>${comanda.quantidade}</td>
                <td>R$ ${Number(comanda.valor).toFixed(2)}</td>
                <td>R$ ${Number(comanda.total).toFixed(2)}</td>
                <td>
                    <button style="padding: 8px 12px; font-size: 14px;" onclick="removerComanda(${comanda.id})">
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


async function removerComanda(id) {
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