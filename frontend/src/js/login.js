document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    errorMessage.textContent = '';

    const payload = {
      email: emailInput.value.trim(),
      senha: senhaInput.value.trim()
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'include'
      });

      if (response.ok) {
        // login bem-sucedido, redireciona
        window.location.href = '/frontend/src/html/home.html';
        alert(`Login realizado com sucesso!`);
      } else {
        const data = await response.json();
        errorMessage.textContent = data.erro || 'Erro no login';
      }
    } catch (error) {
      console.error('Erro ao conectar com o servidor:', error);
      errorMessage.textContent = 'Falha de rede, tente novamente';
    }
  });
});