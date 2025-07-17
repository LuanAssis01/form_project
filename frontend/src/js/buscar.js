const form = document.getElementById("form-busca");
const tbody = document.getElementById("resultado-tbody");
const noResults = document.getElementById("no-results");

console.log(form);
console.log(tbody);
console.log(noResults);

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // tbody.innerHTML = "";
    // noResults.classList.add("hidden");

    console.log("testando");

    const termo = document.getElementById("busca").value.trim();
    if (!termo) {
        alert("Por favor, digite um termo de busca.");
        return;
    }

    try {
        const res = await fetch(`http://127.0.0.1:5000/servidores/cpf/${termo}`, {
            method: "GET",
            // credentials: "include",
            headers: {
                "Accept": "application/json"
            }
        });

        if (res.status === 401) {
            throw new Error("Você precisa estar logado para acessar esta informação");
        }
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.erro || "Erro ao buscar servidor");
        }

        const data = await res.json();
        console.log("JSON bruto recebido do back:", data);
        const servidores = Array.isArray(data) ? data : [data];

        if (servidores.length === 0) {
            noResults.classList.remove("hidden");
            return;
        }

        servidores.forEach((s) => {
            const tr = document.createElement("tr");
            try {
                tr.innerHTML = `
      <td>${s.dados_pessoais?.nome ?? "Não informado"}</td>
      <td>${s.dados_funcionais?.matricula ?? "Não informado"}</td>
      <td>${s.dados_sensiveis?.cpf ?? "Não informado"}</td>
      <td>${s.dados_funcionais?.cargo ?? "Não informado"}</td>
      <td class="actions-column">
        <button class="btn-edit"   data-id="${s.id}">✏️</button>
        <button class="btn-delete" data-id="${s.id}">🗑️</button>
      </td>`;
                tbody.appendChild(tr);
            } catch (err) {
                console.error("Erro ao montar linha:", err, s);
            }
        });

    } catch (error) {
        console.error("Erro na busca:", error);
        alert(`Erro: ${error.message}`);
        noResults.classList.remove("hidden");
    }
});
