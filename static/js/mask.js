// Este código roda DEPOIS do jQuery e do Plugin Mask terem carregado

$(document).ready(function(){
    
    // Máscara de CPF (000.000.000-00)
    $('#id_cpf').mask('000.000.000-00', {reverse: true});

    // Máscara de RG (exemplo: 00.000.000-0)
    $('#id_rg').mask('00.000.000-0');

    // Máscara de Data (DD/MM/YYYY)
    $('#id_data_nascimento').mask('00/00/0000');
    $('#id_validade_cnh').mask('00/00/0000'); 
    
    // Máscara de Telefone Fixo ( (XX) XXXX-XXXX )
    $('#id_telefone').mask('(00) 0000-0000');

    // Máscara de Celular ( (XX) X.XXXX-XXXX )
    $('#id_celular').mask('(00) 0.0000-0000');
    
    // Campos Adicionais (que você pediu)
    $('#id_condutor_cpf').mask('000.000.000-00', {reverse: true});
    $('#id_condutor_rg').mask('00.000.000-0');
    $('#id_condutor_telefone').mask('(00) 0.0000-0000');
    $('#id_telefone_comercial').mask('(00) 0000-0000');
    $('#id_cep_residencial').mask('00.000-000');
    $('#id_cep_comercial').mask('00.000-000');

    // Futuramente: Adicionaremos a validação de CPF aqui.

});