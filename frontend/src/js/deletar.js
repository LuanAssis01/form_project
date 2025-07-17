let formularioId = null;

document.getElementById("form-busca").addEventListener("submit", async function (e) {
  e.preventDefault();
  const cpf = document.getElementById("cpfBusca").value.trim();

  try {
    const resposta = await fetch(`http://127.0.0.1:5000/servidores/cpf/${cpf}`, {
      method: "GET",
      // credentials: "include",
    });

    if (!resposta.ok) throw new Error("Servidor não encontrado.");

    const dados = await resposta.json();

    formularioId = dados.id;

    document.getElementById("nome-servidor").textContent = dados.dados_pessoais?.nome || "Desconhecido";
    document.getElementById("cpf-servidor").textContent = dados.dados_sensiveis?.cpf || "Não informado";
    document.getElementById("matricula-servidor").textContent = dados.dados_funcionais?.matricula || "Não informado";

    document.getElementById("dados-servidor").style.display = "block";
  } catch (error) {
    alert(error.message);
  }
});

document.getElementById("btn-deletar").addEventListener("click", async function () {
  if (!formularioId) return alert("ID da ficha não encontrado.");

  if (!confirm("Tem certeza que deseja excluir este servidor?")) return;

  try {
    const resposta = await fetch(`http://127.0.0.1:5000/servidores/${formularioId}`, {
      method: "DELETE",
      credentials: "include",
    });

    if (!resposta.ok) throw new Error("Erro ao excluir servidor.");

    alert("Servidor excluído com sucesso.");
    document.getElementById("dados-servidor").style.display = "none";
    formularioId = null;
  } catch (error) {
    alert(error.message);
  }
});
