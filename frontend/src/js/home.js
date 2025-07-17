document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logout-btn");

    if (logoutBtn) { 
        logoutBtn.addEventListener("click", async function () {
            try {
                const response = await fetch("http://127.0.0.1:5000/auth/logout", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                const data = await response.json();  

                if (response.ok) {
                    localStorage.removeItem('authState');
                    sessionStorage.removeItem('sessionData');
                    
                    alert(`Login realizado com sucesso!`);
                    window.location.href = "login.html";
                } else {
                    console.error("Erro no logout:", data);
                    alert(`Erro ao fazer logout: ${data.erro || 'Erro desconhecido'}`);
                }
            } catch (error) {
                console.error("Erro na requisição de logout:", error);
                alert("Falha na comunicação com o servidor. Verifique sua conexão.");
            }
        });
    } else {
        console.warn("Botão de logout não encontrado no DOM");
    }
});