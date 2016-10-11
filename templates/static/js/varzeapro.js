function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {
    $('.datepicker').daterangepicker({
        singleDatePicker: true,
        locale: {
            format: "DD/MM/YYYY",
            daysOfWeek: [
                "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"
            ],
            monthNames: [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]
        },
        maxDate: new Date()
    });

    $('.datepicker').mask('00/00/0000');

    $(".select2_single").select2({
        placeholder: "Selecione uma cidade",
        allowClear: true,
        language: {
            noResults: function() {
                return "Nenhuma cidade encontrada";
            }
        }
    });

    $(".upload-from-image").click(function() {
        $(".auto-upload").click();
    });

    $(".auto-upload").on('change', function() {
        var elem = $(this);
        var fd = new FormData(elem.parents('form')[0]);
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: '/upload-file',
            type: 'POST',
            data: fd,
            processData: false,
            contentType: false,
            success: function(response) {
                $("#"+elem.data('target-input-id')).val(response['file']);
                $("img.upload-from-image").attr('src', response['thumbnail']);
            }
        });
    });
});
