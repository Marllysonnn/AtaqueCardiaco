document.getElementById("preverForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const idade = document.getElementById("idade").value;
    const sexo = document.getElementById("sexo").value;
    const pressao_arterial = document.getElementById("pressao_arterial").value;
    const colesterol = document.getElementById("colesterol").value;
    const resultados_eletrocardiograficos = document.getElementById("eletro").value;
    const acucar_sanguineo = document.getElementById("acucar").value;
    const tipo_dor_toracica = document.getElementById("dor").value;
    
    console.log({
        idade: idade,
        sexo: sexo,
        tipo_dor_toracica: tipo_dor_toracica,
        pressao_arterial: pressao_arterial,
        colesterol: colesterol,
        resultados_eletrocardiograficos: resultados_eletrocardiograficos,
        acucar_sanguineo: acucar_sanguineo,
    });

    const response = await fetch("/prever", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            idade: Number(idade),
            sexo: Number(sexo),
            tipo_dor_toracica: Number(tipo_dor_toracica),
            pressao_arterial: Number(pressao_arterial),
            colesterol: Number(colesterol),
            resultados_eletrocardiograficos: Number(resultados_eletrocardiograficos),
            acucar_sanguineo: Number(acucar_sanguineo),
        }),
    
    });

    const mais = document.getElementById("mais");
    const menos = document.getElementById("menos");
    mais.style.display = "none";
    menos.style.display = "none";

    const result = await response.json();
    if (result.previsao !== undefined) {
        if (result.previsao === 1) {
            mais.style.display = "block";
        } else {
            menos.style.display = "block";
        }
    } else {
        document.getElementById("resultado").innerText = "Erro: " + result.erro;
    }
});
