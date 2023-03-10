// Matérias do ENEM
export const materias = ["lin", "hum", "nat", "mat", "red"];

// Objetos para guardar notas e pesos
export const notas = {};
export const pesos = {};

// Checar se as notas estão preenchidas corretamente e salvar notas
export function checar_notas() {
    for (let materia of materias) {
        notas[materia] = parseFloat(document.getElementById(`nota-${materia}`).value);    
        if (Number.isNaN(notas[materia]) || notas[materia] < 0 || notas[materia] > 1000) {
            alert("Há notas inválidas ou em branco!\nCada nota deve ser um número entre 0 e 1000.");
            return false;
        }
    }
    return true;
}

// Checar se os pesos estão preenchidos corretamente e salvar pesos
export function checar_pesos() {
    for (let materia of materias) {
        pesos[materia] = parseFloat(document.getElementById(`peso-${materia}`).value);
        if (Number.isNaN(pesos[materia]) || pesos[materia] < 1 || pesos[materia] > 10) {
            alert("Há pesos inválidos ou em branco!\nCada peso deve ser um número entre 1 e 10.");
            return false;
        }
    }
    return true;
}
