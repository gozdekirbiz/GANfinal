function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(".delete-image").click(function () {
    var imageId = $(this).data("id");
    console.log("Image ID: ", imageId);  // Add this line

    $.ajax({
        url: '/delete_image/' + imageId + '/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            if (response.success) {
                $('#image-' + imageId).remove();
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    console.log('BurayaGiriyor');

    var loadingOverlay = document.getElementById('loading-overlay');
    var fileInput = document.getElementById('file-input');
    var styleSelect = document.getElementById('style');
    var uploadButton = document.getElementById('upload-button');

    uploadButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission

        if (fileInput.files.length > 0) {
            loadingOverlay.style.display = 'block';
            uploadButton.disabled = true;

            var formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('selectOption', styleSelect.value);  // changed from 'style' to 'selectOption'

            $.ajax({
                url: '/home/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response.success) {
                        console.log('Art generated successfully');
                        location.reload();
                    } else {
                        console.log('Error occurred');
                    }
                    loadingOverlay.style.display = 'none';
                    uploadButton.disabled = false;
                },
                error: function () {
                    console.log('Error occurred');
                    loadingOverlay.style.display = 'none';
                    uploadButton.disabled = false;
                }
            });
        }
    });

    loadingOverlay.style.display = 'none';
});


