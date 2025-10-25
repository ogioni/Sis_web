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

// --- FUNÇÃO DE VALIDAÇÃO DE DATA (Completo) ---
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

// --- FUNÇÃO DE FEEDBACK VISUAL (Validação no 'blur') ---
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
    
    // 1. DATA DE NASCIMENTO (FORÇANDO PREENCHIMENTO COMPLETO E VALIDAÇÃO)
    $('#id_data_nascimento').mask('00/00/0000', {selectOnFocus: true});
    $('#id_validade_cnh').mask('00/00/0000', {selectOnFocus: true});
    $('#id_condutor_data_nasc').mask('00/00/0000', {selectOnFocus: true});
    $('#id_condutor_validade_cnh').mask('00/00/0000', {selectOnFocus: true});
    
    // 2. CELULAR (FORÇANDO PREENCHIMENTO COMPLETO - Digito 9 obrigatório)
    $('#id_celular').mask('(00) 0.0000-0000', {
        selectOnFocus: true,
        onKeyPress: function(cel, e, field, options) {
            // Pega o valor atual, remove caracteres e vê o tamanho
            var masks = ['(00) 0.0000-0000', '(00) 0.0000-0000'];
            var mask = (cel.length > 14) ? masks[1] : masks[0];
            $('#id_celular').mask(mask, options);
        }
    });
    $('#id_condutor_telefone').mask('(00) 0.0000-0000', {selectOnFocus: true});
    
    // Telefone Fixo (FORÇANDO PREENCHIMENTO COMPLETO)
    $('#id_telefone').mask('(00) 0000-0000', {selectOnFocus: true}); 
    $('#id_telefone_comercial').mask('(00) 0000-0000', {selectOnFocus: true});

    $('#id_cep_residencial').mask('00000-000', {selectOnFocus: true});
    $('#id_cep_comercial').mask('00000-000', {selectOnFocus: true});

    // --- VALIDAÇÕES (Ao sair do campo) ---
    
    // Validação de CPF
    setupValidation('#id_cpf', '#cpf_validation_message', validarCPF, 'CPF Inválido!', 'CPF Válido');
    
    // Validação de Data
    setupValidation('#id_data_nascimento', '#data_nasc_validation_message', validarData, 'Data incompleta ou inválida!', '');

    // Validação de Email
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
});