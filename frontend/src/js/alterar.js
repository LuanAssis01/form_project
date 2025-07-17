document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("form-busca").addEventListener("submit", async function (e) {
    e.preventDefault();

    const cpf = document.getElementById("cpfBusca").value.trim();

    try {
      const resposta = await fetch(`http://127.0.0.1:5000/servidores/cpf/${cpf}`, {
        method: "GET",
        // credentials: "include",
      });

      if (!resposta.ok) {
        throw new Error("Servidor não encontrado.");
      }

      const dados = await resposta.json();

      document.getElementById("nome").value = dados.nome_completo || "";
      document.getElementById("nome_social").value = dados.nome_social || "";
      document.getElementById("cpf").value = dados.cpf || "";
      document.getElementById("data_nascimento").value = dados.data_nascimento || "";
      document.getElementById("sexo").value = dados.sexo || "";
      document.getElementById("estado_civil").value = dados.estado_civil || "";
      document.getElementById("telefone").value = dados.telefone || "";
      document.getElementById("email").value = dados.email || "";

      document.getElementById("form-alterar").style.display = "block";
    } catch (error) {
      alert(error.message);
      document.getElementById("form-alterar").style.display = "none";
    }
  });

  document.getElementById("form-alterar").addEventListener("submit", async function (e) {
    e.preventDefault();

    const cpf = document.getElementById("cpf").value;
    const payload = {
      nome_completo: document.getElementById("nome").value,
      nome_social: document.getElementById("nome_social").value,
      data_nascimento: document.getElementById("data_nascimento").value,
      sexo: document.getElementById("sexo").value,
      estado_civil: document.getElementById("estado_civil").value,
      telefone: document.getElementById("telefone").value,
      email: document.getElementById("email").value
    };

    try {
      const resposta = await fetch(`http://127.0.0.1:5000/servidor/${cpf}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!resposta.ok) {
        throw new Error("Erro ao atualizar.");
      }

      alert("Dados atualizados com sucesso!");
    } catch (error) {
      alert(error.message);
    }
  });

  document.getElementById("btn-cancelar").addEventListener("click", function () {
    document.getElementById("form-alterar").style.display = "none";
    document.getElementById("form-alterar").reset();
  });
});
