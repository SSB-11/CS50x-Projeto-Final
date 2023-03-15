import { materias, notas, pesos, checar_notas, checar_pesos } from "./module.mjs";

// Calcular média simples
function calcularMediaSimples() {
    let somaNotas = 0;
    let somaMaterias = 0;
    for (let materia of materias) {
        somaNotas += notas[materia];
        somaMaterias++;
    }
    return (Math.round(somaNotas * 100 / somaMaterias) / 100).toFixed(2);
}

// Calcular média ponderada
function calcularMediaPonderada() {
    let somaNotas = 0;
    let somaPesos = 0;
    for (let materia of materias) {
        somaNotas += notas[materia] * pesos[materia];
        somaPesos += pesos[materia];
    }
    return (Math.round(somaNotas * 100 / somaPesos) / 100).toFixed(2);
}

// Calcular média quanto o botão for clicado
document.getElementById("calculadora").addEventListener("submit", function(e){

    // Prevenir que a página recarrege
    e.preventDefault();

    // Checar e salvar valores
    if (checar_notas() == false) {
        limparResult();
        return;
    } else if (checar_pesos() == false) {
        limparResult();
        return;
    }
    let mediaSimples = calcularMediaSimples();
    let mediaPonderada = calcularMediaPonderada();

    // Mostrar média final e botão de salvar resultado
    document.getElementById("resultado-simples").innerHTML = `Média simples: ${mediaSimples}`;
    document.getElementById("resultado-ponderado").innerHTML = `Média ponderada: ${mediaPonderada}`;
    document.getElementById("salvar-resultado").classList.remove("d-none");
    
    // Salvar média final para o usuário poder salvar o resultado
    document.querySelector("form[action='/resultados'] input[name='simples']").value = mediaSimples;
    document.querySelector("form[action='/resultados'] input[name='ponderado']").value = mediaPonderada;

    // Atualizar valor de notas e pesos conforme digitado na calculadora
    for (let materia of materias) {
        document.getElementById(`nota_${materia}`).value = notas[materia];
        document.getElementById(`peso_${materia}`).value = pesos[materia];
    }

    return;
});

// Limpar tudo (notas e pesos)
document.getElementById("limpar").addEventListener("click", function() {
    window.location.replace("/");
    return;
});

// Nomear resultado
document.getElementById("salvar-resultado").addEventListener("click", function(e) {
    let nome = undefined;
    do {
        nome = prompt("Como gostaria de nomear resultado?");
    } while (!nome);

    document.querySelector("form[action='/resultados'] input[name='nome']").value = nome;
    return;
});
