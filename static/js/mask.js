// --- FUNÇÃO DE VALIDAÇÃO DE CPF (Algoritmo Padrão Brasileiro) ---
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g,''); // Remove caracteres não numéricos
    if(cpf == '') return false;
    if (cpf.length != 11 || 
        cpf == "00000000000" || cpf == "11111111111" || cpf == "22222222222" || 
        cpf == "33333333333" || cpf == "44444444444" || cpf == "55555555555" || 
        cpf == "66666666666" || cpf == "77777777777" || cpf == "88888888888" || 
        cpf == "99999999999")
        return false;
    let add = 0;
    for (let i=0; i < 9; i ++) add += parseInt(cpf.charAt(i)) * (10 - i);
    let rev = 11 - (add % 11);
    if (rev == 10 || rev == 11) rev = 0;
    if (rev != parseInt(cpf.charAt(9))) return false;
    add = 0;
    for (let i = 0; i < 10; i ++) add += parseInt(cpf.charAt(i)) * (11 - i);
    rev = 11 - (add % 11);
    if (rev == 10 || rev == 11) rev = 0;
    if (rev != parseInt(cpf.charAt(10))) return false;
    return true;
}

// --- FUNÇÃO DE VALIDAÇÃO DE EMAIL (Regex simples) ---
function validarEmail(email) {
    var re = /^[a-zA-Z0m9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(String(email).toLowerCase());
}

// --- FUNÇÃO DE VALIDAÇÃO DE DATA (Formato) ---
function validarData(data) {
    // Checa se o formato DD/MM/AAAA foi totalmente preenchido
    if (data.length !== 10) return false;

    var partes = data.split('/');
    var dia = parseInt(partes[0], 10);
    var mes = parseInt(partes[1], 10);
    var ano = parseInt(partes[2], 10);

    // Checa se os números estão em faixas razoáveis
    if (mes < 1 || mes > 12) return false;
    if (dia < 1 || dia > 31) return false;

    return true; // Se a máscara for completa, assumimos que é válida para o frontend
}

// --- FUNÇÃO DE VALIDAÇÃO DE CELULAR (11 dígitos) ---
function validarCelular(celular) {
    // Remove todos os caracteres não numéricos (parênteses, traço, espaço, ponto)
    var digitos = celular.replace(/[^\d]/g, '');
    
    // Verifica se tem exatamente 11 dígitos (2 de DDD + 9 do número)
    return digitos.length === 11;
}

// --- FUNÇÃO DE VALIDAÇÃO DE IDADE (Maior ou igual a 18) ---
function isMaisDe18(data) {
    // Checa se a data tem o formato completo (DD/MM/AAAA)
    if (data.length !== 10) return false;

    // Converte a string "DD/MM/AAAA" para um objeto Date
    var partes = data.split('/');
    var dia = parseInt(partes[0], 10);
    var mes = parseInt(partes[1], 10) - 1; // Mês é 0-indexado no JS (Jan=0, Fev=1, etc.)
    var ano = parseInt(partes[2], 10);
    
    var dataNasc = new Date(ano, mes, dia);
    var dataHoje = new Date();

    // Calcula a idade
    var idade = dataHoje.getFullYear() - dataNasc.getFullYear();
    var m = dataHoje.getMonth() - dataNasc.getMonth();
    
    // Ajusta a idade se o aniversário deste ano ainda não chegou
    if (m < 0 || (m === 0 && dataHoje.getDate() < dataNasc.getDate())) {
        idade--;
    }
    
    return idade >= 18;
}

// --- FUNÇÃO MESTRE (Verifica se o formulário está pronto para enviar) ---
function checkFormValidity() {
    
    // --- GRUPO 1: CAMPOS COM VALIDAÇÃO COMPLEXA ---
    
    // 1. Validar Data de Nascimento (Formato E Idade)
    var dataNasc = $('#id_data_nascimento').val();
    var dataNascValida = validarData(dataNasc) && isMaisDe18(dataNasc);
    
    // 2. Validar CPF
    var cpf = $('#id_cpf').val();
    var cpfValido = validarCPF(cpf);
    
    // 3. Validar Celular
    var celular = $('#id_celular').val();
    var celularValido = validarCelular(celular);
    
    // 4. Validar Emails (formato e se batem)
    var email = $('#id_email').val();
    var emailConfirm = $('#id_email_confirm').val();
    var emailValido = validarEmail(email) && (email.toLowerCase() === emailConfirm.toLowerCase());

    
    // --- GRUPO 2: CAMPOS OBRIGATÓRIOS (SÓ PRECISAM ESTAR PREENCHIDOS) ---
    // Criamos uma função simples para checar se o valor não está vazio
    function isPreenchido(selector) {
        var valor = $(selector).val();
        return valor && valor.trim().length > 0;
    }
    
    // 5. Validar Campos de Texto
    var nomeCompletoValido = isPreenchido('#id_nome_completo');
    var rgValido = isPreenchido('#id_rg');
    var orgaoExpValido = isPreenchido('#id_rg_orgao_expeditor');
    var nomeMaeValido = isPreenchido('#id_nome_mae');
    
    // 6. Validar Campos de Seleção (Select)
    var ufRgValido = isPreenchido('#id_rg_uf');
    var estadoCivilValido = isPreenchido('#id_estado_civil');
    
    // (Campos opcionais 'id_nome_pai' e 'id_telefone' não são checados)


    // --- A LÓGICA FINAL (AGORA VERIFICA TUDO) ---
    if (
        // Grupo 1
        dataNascValida && 
        cpfValido && 
        celularValido && 
        emailValido &&
        
        // Grupo 2
        nomeCompletoValido &&
        rgValido &&
        orgaoExpValido &&
        nomeMaeValido &&
        ufRgValido &&
        estadoCivilValido
    ) {
        // Se TUDO for válido, habilita o botão
        $('#submit_button').prop('disabled', false).css('opacity', '1.0');
    } else {
        // Se QUALQUER COISA for inválida, desabilita
        $('#submit_button').prop('disabled', true).css('opacity', '0.5');
    }
}

// --- FUNÇÃO DE FEEDBACK VISUAL (Validação no 'blur') ---
// (Usada para CPF, Email e Celular)
function setupValidation(fieldId, errorSpanId, validationFunction, errorMessage, successMessage) {
    $(fieldId).on('blur', function() { 
        var value = $(this).val();
        var errorSpan = $(errorSpanId);

        if (value.length > 0) { 
            if (validationFunction(value)) {
                // Válido
                $(this).css('border-color', 'green');
                errorSpan.text(successMessage).css('color', 'green');
            } else {
                // Inválido
                $(this).css('border-color', 'red');
                errorSpan.text(errorMessage).css('color', 'red');
            }
        } else {
            // Limpa o feedback se o campo estiver vazio
            $(this).css('border-color', '#ccc');
            errorSpan.text('');
        }
    });
}

// --- APLICAÇÃO DAS MÁSCARAS E VALIDAÇÃO ---
$(document).ready(function(){
    
    // Desabilita o botão ao carregar a página
    $('#submit_button').prop('disabled', true).css('opacity', '0.5');

    // --- MÁSCARAS ---
    $('#id_cpf').mask('000.000.000-00', {reverse: true});
    $('#id_condutor_cpf').mask('000.000.000-00', {reverse: true});
    
    // MÁSCARA RG (Sem máscara rígida)
    $('#id_rg').mask('00.000.000-A', {
        translation: { 'A': {pattern: /[A-Za-z0-9]/, optional: true} },
        reverse: true,
        placeholder: "00.000.000-0"
    });
    $('#id_condutor_rg').mask('00.000.000-A', {
        translation: { 'A': {pattern: /[A-Za-z0-9]/, optional: true} },
        reverse: true,
        placeholder: "00.000.000-0"
    });
    
    // DATAS
    $('#id_data_nascimento').mask('00/00/0000', {selectOnFocus: true});
    $('#id_validade_cnh').mask('00/00/0000', {selectOnFocus: true});
    $('#id_condutor_data_nasc').mask('00/00/0000', {selectOnFocus: true});
    $('#id_condutor_validade_cnh').mask('00/00/0000', {selectOnFocus: true});
    
    // CELULAR (com lógica para 8 ou 9 dígitos - embora a validação obrigue 9)
   $('#id_celular').mask('(00) 0.0000-0000', {selectOnFocus: true});

    $('#id_condutor_telefone').mask('(00) 0.0000-0000', {selectOnFocus: true});
    
    // TELEFONES FIXOS
    $('#id_telefone').mask('(00) 0000-0000', {selectOnFocus: true}); 
    $('#id_telefone_comercial').mask('(00) 0000-0000', {selectOnFocus: true});

    // CEP
    $('#id_cep_residencial').mask('00000-000', {selectOnFocus: true});
    $('#id_cep_comercial').mask('00000-000', {selectOnFocus: true});

    // --- VALIDAÇÕES (Ao sair do campo) ---
    
    // Validação de CPF
    setupValidation('#id_cpf', '#cpf_validation_message', validarCPF, 'CPF Inválido!', 'CPF Válido');
    
    // Validação customizada de Data de Nascimento (Formato + Idade)
    $('#id_data_nascimento').on('blur', function() {
        var valor = $(this).val();
        var errorSpan = $('#data_nasc_validation_message');
        
        if (valor.length === 0) {
            // Limpa se o campo estiver vazio
            $(this).css('border-color', '#ccc');
            errorSpan.text('');
        }
        else if (!validarData(valor)) {
            // Erro 1: Formato inválido
            $(this).css('border-color', 'red');
            errorSpan.text('Data incompleta ou inválida!').css('color', 'red');
        } 
        else if (!isMaisDe18(valor)) {
            // Erro 2: Menor de idade
            $(this).css('border-color', 'red');
            errorSpan.text('Você deve ter pelo menos 18 anos.').css('color', 'red');
        } 
        else {
            // Sucesso!
            $(this).css('border-color', 'green');
            errorSpan.text('').css('color', 'green'); // Não mostra "DATA OK"
        }
    });

    // Validação de Email (instantâneo)
    setupValidation('#id_email', '#email_validation_message', validarEmail, 'E-mail inválido!', 'E-mail válido');
    
    // Validação de Celular
    setupValidation('#id_celular', '#celular_validation_message', validarCelular, 'Celular incompleto!', '');
    
    // Validação de Confirmação de Email (compara os campos)
    $('#id_email_confirm').on('blur', function() {
        var email = $('#id_email').val();
        var emailConfirm = $(this).val();
        var errorSpan = $('#email_confirm_validation_message');

        if (emailConfirm.length > 0) {
            if (email.toLowerCase() === emailConfirm.toLowerCase()) {
                $(this).css('border-color', 'green');
                errorSpan.text('E-mails conferem.').css('color', 'green');
            } else {
                $(this).css('border-color', 'red');
                errorSpan.text('E-mails não conferem!').css('color', 'red');
            }
        } else {
            $(this).css('border-color', '#ccc');
            errorSpan.text('');
        }
    });

    // Força Uppercase nos campos de nome
    $('.uppercase-input').on('keyup', function() {
        $(this).val($(this).val().toUpperCase());
    });
    
    // Força Lowercase nos campos de email
    $('.lowercase-input').on('keyup', function() {
        $(this).val($(this).val().toLowerCase());
    });
    
    // --- MASTER CHECK (Dispara a validação mestre) ---
    // Define TODOS os campos que devem ser checados
    var camposValidados = '#id_data_nascimento, #id_cpf, #id_celular, #id_email, #id_email_confirm, #id_nome_completo, #id_rg, #id_rg_orgao_expeditor, #id_nome_mae, #id_rg_uf, #id_estado_civil';
    
    // Roda a checagem mestre sempre que o usuário sair (blur) ou digitar (keyup) ou mudar (change) em QUALQUER um desses campos
    $(camposValidados).on('blur keyup change', function() {
        checkFormValidity();
    });
});