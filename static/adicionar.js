import { checar_notas, checar_pesos } from "./module.mjs";

// Checar valores enviados
document.getElementById("adicionar").addEventListener("submit", function(e) {
    let selecionado = document.getElementById("salvar").value;

    // Checar "nomear como"
    if (!document.getElementById("name").value) {
        alert('Favor preencha o campo "Nomear como".');
        e.preventDefault();
        return;
    }

    // Se enviado notas
    if (selecionado == "Notas") {
        if (checar_notas() == false) {
            e.preventDefault();
            return;
        }
    }

    // Se enviado pesos
    if (selecionado == "Pesos") {
        if (checar_pesos() == false) {
            e.preventDefault();
            return;
        }
    }

    return;
})
