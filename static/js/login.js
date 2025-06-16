var bntSingin = document.querySelector("#singin");
var bntSingup = document.querySelector("#singup");
var body = document.querySelector("body");

bntSingin.addEventListener("click", function () {
  body.className = 'sing-in-js';
});

bntSingup.addEventListener("click", function () {
  body.className = 'sing-up-js';
});

function togglePassword(id) {
    const passwordInput = document.getElementById(id);
    const icon = passwordInput.nextElementSibling;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

document.addEventListener("DOMContentLoaded", function () {
  const formLogin = document.querySelector('form[action*="login"]');
  if (!formLogin) return;

  const emailInput = document.querySelector("#emailLogin");
  const senhaInput = document.querySelector("#senhaLogin");

  const mostrarErro = (input, mensagem) => {
    let feedback = input.nextElementSibling;
    if (!feedback || !feedback.classList.contains('feedback')) {
      feedback = document.createElement('small');
      feedback.className = 'feedback';
      input.parentNode.appendChild(feedback);
    }
    feedback.innerHTML = mensagem;
    feedback.style.color = '#d32f2f';
    input.classList.add('is-invalid');
  };

  const limparErro = (input) => {
    let feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('feedback')) {
      feedback.textContent = '';
    }
    input.classList.remove('is-invalid');
  };

  formLogin.addEventstener('submit', (e) => {
    let valido = true;

    if (!emailInput.value.includes("@")) {
      mostrarErro(emailInput, 'Digite um e-mail válido.');
      valido = false;
    } else {
      limparErro(emailInput);
    }

    if (senhaInput.value.length < 3) {
      mostrarErro(senhaInput, 'Senha inválida ou muito curta.');
      valido = false;
    } else {
      limparErro(senhaInput);
    }

    if (!valido) e.preventDefault();
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('form[action*="cadastro"]');
  const senhaInput = form.querySelector('input[name="senha"]');
  const confirmaSenhaInput = form.querySelector('input[name="confirmaSenha"]');
  const telefoneInput = form.querySelector('input[name="telefone"]');
  const cpfInput = form.querySelector('input[name="cpf"]');


  const erroExibido = {
    cpf: false,
    senha: false,
    confirmaSenha: false,
  };
  
  const mostrarErro = (input, mensagem) => {
    let feedback = input.nextElementSibling;

    if (!feedback || !feedback.classList.contains('feedback')) {
        feedback = document.createElement('small');
        feedback.className = 'feedback';
        input.parentNode.appendChild(feedback);
    }

    if (!erroExibido[input.name]) {
        feedback.innerHTML = mensagem;
        feedback.style.color = '#d32f2f';
        input.classList.add('is-invalid');
        erroExibido[input.name] = true;
    }
};

  const limparErro = (input) => {
    let feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('feedback')) {
        feedback.textContent = '';
    }
    input.classList.remove('is-invalid');
    erroExibido[input.name] = false;
};

  telefoneInput.addEventListener('input', () => {
    let v = telefoneInput.value.replace(/\D/g, '');
    if (v.length > 2) v = '(' + v.slice(0, 2) + ') ' + v.slice(2);
    if (v.length > 9) v = v.slice(0, 9) + '-' + v.slice(9);
    telefoneInput.value = v.slice(0, 14);
  });


  cpfInput.addEventListener('input', () => {
    let valor = cpfInput.value.replace(/\D/g, '');

    if (valor.length <= 11) {
      valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
      valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
      valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    } else {
      valor = valor.replace(/^(\d{2})(\d)/, '$1.$2');
      valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
      valor = valor.replace(/\.(\d{3})(\d)/, '.$1/$2');
      valor = valor.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    }

    cpfInput.value = valor.slice(0, 18);
  });

  
  form.addEventListener('submit', (e) => {
    let valido = true;

    const cpf = cpfInput.value.replace(/\D/g, '');
    if (cpf.length !== 11 && cpf.length !== 14) {
      mostrarErro(cpfInput, 'Insira um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.');
      valido = false;
    } else {
      limparErro(cpfInput);
    }

    const senha = senhaInput.value;
    const senhaForte = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\[\]{}|\\:;"',.<>\/?`~]).{8,}$/;
    if (!senhaForte.test(senha)) {
      mostrarErro(senhaInput, 'A senha precisa ter no mínimo 8 caracteres, 1 letra maiúscula, 1 número e 1 caractere especial.');
      valido = false;
    } else {
      limparErro(senhaInput);
    }

    if (senha !== confirmaSenhaInput.value) {
      mostrarErro(confirmaSenhaInput, 'As senhas não coincidem!');
      valido = false;
    } else {
      limparErro(confirmaSenhaInput);
    }

    if (!valido) {
      e.preventDefault();
    }
  });

  
  const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
  requiredFields.forEach(field => {
    field.addEventListener('invalid', function () {
      this.setCustomValidity(`Por favor, preencha o campo "${getFieldLabel(this)}" corretamente.`);
      this.classList.add('is-invalid');
    });

    field.addEventListener('input', function () {
      this.setCustomValidity('');
      this.classList.remove('is-invalid');
    });
  });

  function getFieldLabel(input) {
    const label = document.querySelector(`label[for="${input.id}"]`);
    return label ? label.innerText.replace(/:$/, '') : 'obrigatório';
  }

  
  const urlParams = new URLSearchParams(window.location.search);
  const erro = urlParams.get('erro');

  if (erro === 'email') {
    Swal.fire({
      icon: 'error',
      title: 'Erro!',
      text: 'Este e-mail já está cadastrado. Tente outro!',
      confirmButtonText: 'Entendi',
      confirmButtonColor: '#00796B'
    });
  } else if (erro === 'perfil') {
    Swal.fire({
      icon: 'error',
      title: 'Erro!',
      text: 'Erro ao definir perfil. Tente novamente.',
      confirmButtonText: 'Entendi',
      confirmButtonColor: '#00796B'
    });
  } else if (urlParams.get('sucesso') === 'true') {
    Swal.fire({
      icon: 'success',
      title: 'Cadastro realizado!',
      text: 'Seu cadastro foi concluído com sucesso.',
      confirmButtonText: 'Entendi',
      confirmButtonColor: '#00796B'
    });
  } 
});

document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const erro = urlParams.get('erro');

    if (erro === 'validacao') {
        Swal.fire({
            icon: 'error',
            title: 'Erro!',
            text: 'Email ou senha incorretos',
            confirmButtonText: 'Entendi',
            confirmButtonColor: '#00796B'
        });
    }

    const formLogin = document.querySelector('form[action*="login"]');
    if (!formLogin) return;

    const emailInput = document.querySelector("#emailLogin");
    const senhaInput = document.querySelector("#senhaLogin");

    const mostrarErro = (input, mensagem) => {
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('feedback')) {
            feedback = document.createElement('small');
            feedback.className = 'feedback';
            input.parentNode.appendChild(feedback);
        }
        feedback.innerHTML = mensagem;
        feedback.style.color = '#d32f2f';
        input.classList.add('is-invalid');
    };

    const limparErro = (input) => {
        let feedback = input.nextElementSibling;
        if (feedback && feedback.classList.contains('feedback')) {
            feedback.textContent = '';
        }
        input.classList.remove('is-invalid');
    };

    formLogin.addEventListener('submit', (e) => {
        let valido = true;

        if (!emailInput.value.includes("@")) {
            mostrarErro(emailInput, 'Digite um e-mail válido.');
            valido = false;
        } else {
            limparErro(emailInput);
        }

        if (senhaInput.value.length < 3) {
            mostrarErro(senhaInput, 'Senha inválida ou muito curta.');
            valido = false;
        } else {
            limparErro(senhaInput);
        }

        if (!valido) e.preventDefault();
    });
});
