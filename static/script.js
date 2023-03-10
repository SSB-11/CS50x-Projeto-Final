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

// Limpar resultado
function limparResult() {
    document.getElementById("resultado-simples").innerHTML = "";
    document.getElementById("resultado-ponderado").innerHTML = "";
    document.getElementById("salvar-resultado").classList.add("d-none");
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
    
    return;
});

// Limpar tudo (notas e pesos)
document.getElementById("limpar").addEventListener("click", function() {
    limparResult();
})
