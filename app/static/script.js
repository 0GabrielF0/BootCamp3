const formulario = document.getElementById("form-validacao");
const campoPlaca = document.getElementById("placa");
const botaoValidar = document.getElementById("btn-validar");

const resultado = document.getElementById("resultado");
const resultadoTitulo = document.getElementById("resultado-titulo");
const resultadoStatus = document.getElementById("resultado-status");
const resultadoMensagem = document.getElementById("resultado-mensagem");
const resultadoPlaca = document.getElementById("resultado-placa");
const resultadoPadrao = document.getElementById("resultado-padrao");

function exibirResultado(dados) {
    const valida = dados.valida === true;

    resultado.classList.remove("hidden", "valid", "invalid");
    resultado.classList.add(valida ? "valid" : "invalid");

    resultadoTitulo.textContent = valida
        ? "Placa válida"
        : "Placa inválida";

    resultadoStatus.textContent = valida
        ? "APROVADA"
        : "REPROVADA";

    resultadoMensagem.textContent =
        dados.mensagem || "Não foi possível validar a placa.";

    resultadoPlaca.textContent =
        dados.placa_normalizada || "Não identificada";

    resultadoPadrao.textContent =
        dados.padrao || "Não identificado";

    resultado.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}

function exibirErro(mensagem) {
    resultado.classList.remove("hidden", "valid");
    resultado.classList.add("invalid");

    resultadoTitulo.textContent = "Não foi possível validar";
    resultadoStatus.textContent = "ERRO";
    resultadoMensagem.textContent = mensagem;
    resultadoPlaca.textContent = "—";
    resultadoPadrao.textContent = "—";
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const placa = campoPlaca.value.trim();

    if (!placa) {
        exibirErro("Digite uma placa para realizar a validação.");
        campoPlaca.focus();
        return;
    }

    botaoValidar.disabled = true;
    botaoValidar.textContent = "Validando...";

    resultado.classList.add("hidden");

    try {
        const resposta = await fetch("/validar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                placa: placa
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            const detalhes = dados.erro?.detalhes || [];

            const mensagem = detalhes.length > 0
                ? detalhes.map(item => item.problema).join(" ")
                : dados.erro?.mensagem || "Ocorreu um erro na requisição.";

            exibirErro(mensagem);
            return;
        }

        exibirResultado(dados);

    } catch (erro) {
        exibirErro(
            "Não foi possível conectar à API. Verifique se o servidor está funcionando."
        );

    } finally {
        botaoValidar.disabled = false;
        botaoValidar.textContent = "Validar placa";
    }
});