document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('cadastro-form');
  const nomeInput = document.getElementById('nome');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const cpfInput = document.getElementById('cpf');
  const telefoneInput = document.getElementById('telefone');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
      nome: nomeInput.value.trim(),
      email: emailInput.value.trim(),
      senha: senhaInput.value.trim(),
      cpf: cpfInput.value.trim(),
      telefone: telefoneInput.value.trim()
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/auth/cadastrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Cadastro realizado com sucesso!');
        window.location.href = '/frontend/src/html/home.html';
      } else {
        alert(data.erro || 'Erro no cadastro');
      }
    } catch (error) {
      console.error(error);
      alert('Erro na conexão com o servidor.');
    }
  });
});
