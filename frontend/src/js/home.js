document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logout-btn");

    logoutBtn.addEventListener("click", async function () {
        try {
            const response = await fetch("http://127.0.0.1:5000/auth/logout", {
                method: "POST",
                credentials: "include", // envia o cookie da sessão
            });

            if (response.ok) {
                window.location.href = "login.html";
            } else {
                alert("Erro ao fazer logout. Tente novamente.");
            }
        } catch (error) {
            console.error("Erro ao desconectar:", error);
            alert("Erro na conexão com o servidor.");
        }
    });
});
