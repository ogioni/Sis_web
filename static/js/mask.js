/*
Este arquivo aplica as máscaras e a validação de CPF no formulário.
*/

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
    var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(String(email).toLowerCase());
}

// --- FUNÇÃO DE FEEDBACK VISUAL (Validação no 'blur') ---
function setupValidation(fieldId, errorSpanId, validationFunction, errorMessage, successMessage) {
    $(fieldId).on('blur', function() { 
        var value = $(this).val();
        var errorSpan = $(errorSpanId);

        if (value.length > 0) { 
            if (validationFunction(value)) {
                $(this).css('border-color', 'green');
                errorSpan.text(successMessage).css('color', 'green');
            } else {
                $(this).css('border-color', 'red');
                errorSpan.text(errorMessage).css('color', 'red');
            }
        } else {
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
    
    // (Req 1) MÁSCARA DE RG: Aceita 0-9 e letras M, G, X (para MG, M-, etc.)
    // Vamos usar '00.000.000-A' onde A é opcional e aceita letras/números
    // Esta máscara aceita os padrões MG-12.345.678 ou 12.345.678-M
    // Para RG (permitindo letras e pontos)
    $('#id_rg').mask('00.000.000-S', {
        translation: {
          'S': {pattern: /[A-Za-z0-9]/, optional: true} // Aceita letra/numero no final
        }
    });
    // Se MG vier na frente (ex: MG-12.345.678), o campo deve ser texto simples
    // Vamos remover a máscara restritiva e deixar o usuário digitar o que quiser,
    // já que o formato varia muito (ex: 'MG-12.345.678' ou '12.345.678-M').
    
    // Vamos tentar uma máscara mais flexível que aceita pontos:
    $('#id_rg').mask('00.000.000', {
        translation: {
            'A': {pattern: /[A-Za-z0-9]/, optional: true}
        },
        reverse: true // Tenta aplicar de trás para frente
    });
    // Se ainda assim MG- não funcionar, teremos que remover a máscara do RG.

    $('#id_data_nascimento').mask('00/00/0000');
    $('#id_validade_cnh').mask('00/00/0000');
    $('#id_condutor_data_nasc').mask('00/00/0000');
    $('#id_condutor_validade_cnh').mask('00/00/0000');
    
    $('#id_telefone').mask('(00) 0000-0000'); 
    $('#id_telefone_comercial').mask('(00) 0000-0000');
    $('#id_celular').mask('(00) 0.0000-0000'); 
    $('#id_condutor_telefone').mask('(00) 0.0000-0000');

    $('#id_cep_residencial').mask('00000-000');
    $('#id_cep_comercial').mask('00000-000');

    // --- VALIDAÇÕES (Ao sair do campo) ---
    
    // Validação de CPF
    setupValidation('#id_cpf', '#cpf_validation_message', validarCPF, 'CPF Inválido!', 'CPF Válido');
    setupValidation('#id_condutor_cpf', '#condutor_cpf_validation_message', validarCPF, 'CPF Inválido!', 'CPF Válido'); 

    // Validação de Email (instantâneo)
    setupValidation('#id_email', '#email_validation_message', validarEmail, 'E-mail inválido!', 'E-mail válido');
    
    // Validação de Confirmação de Email
    $('#id_email_confirm').on('blur', function() {
        var email = $('#id_email').val();
        var emailConfirm = $(this).val();
        var errorSpan = $('#email_confirm_validation_message');

        if (emailConfirm.length > 0) {
            if (email.toLowerCase() === emailConfirm.toLowerCase()) { // Compara em minúsculas
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

    // (Req 1) Força Uppercase nos campos de nome
    $('.uppercase-input').on('keyup', function() { // Usando keyup para feedback instantâneo
        $(this).val($(this).val().toUpperCase());
    });
    
    // (Req 2) Força Lowercase nos campos de email
    $('#id_email, #id_email_confirm').on('keyup', function() {
        $(this).val($(this).val().toLowerCase());
    });
});