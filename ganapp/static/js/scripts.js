// Retrieve CSRF token from cookies
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

// Set CSRF token for AJAX requests
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
    console.log("Image ID: ", imageId);

    // Store the reference to the current element
    var $imageElement = $(this).closest('.col');

    $.ajax({
        url: '/delete_image/' + imageId + '/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            if (response.success) {
                // Remove the image element immediately
                $imageElement.remove();
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

    if (loadingOverlay && fileInput && styleSelect && uploadButton) {
        uploadButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission

            if (fileInput.files.length > 0) {
                loadingOverlay.style.display = 'block';
                uploadButton.disabled = true;

                var formData = new FormData();
                formData.append('image', fileInput.files[0]);
                formData.append('selectOption', styleSelect.value);

                $.ajax({
                    url: '/home/',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        console.log(response); // Log the response to check its structure

                        // Check if the response indicates success or failure
                        if (response && response.hasOwnProperty('success') && response.success) {
                            console.log('Art generated successfully');
                            // Redirect to the result page or perform any other necessary actions
                            window.location.href = '/result/';
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
    }
});


$(document).ready(function () {
    $('.nav-link').click(function (e) {
        if ($(this).attr('data-bs-toggle') === 'tab') {
            e.preventDefault();
            $('.nav-link').removeClass('active');
            $(this).addClass('active');
            $('.tab-pane').removeClass('show active');

            var target = $($(this).attr('href'));
            target.addClass('show active');
        }
    });




    // Change password form submission
    $('#change-password-form').on('submit', function (e) {
        e.preventDefault();
        var oldPassword = $('#current-password').val();
        var newPassword1 = $('#new-password').val();
        var newPassword2 = $('#confirm-new-password').val();

        $.ajax({
            type: "POST",
            url: "/change_password/",
            data: {
                'old_password': oldPassword,
                'new_password1': newPassword1,
                'new_password2': newPassword2
            },
            success: function (response) {
                // Handle success
                if (response.success) {
                    console.log("Password successfully changed.");
                } else {
                    console.log("Password change failed: ", response.message);
                }
            },
            error: function (response) {
                // Handle error
                console.log("Error occurred while changing password.", response);
            }
        });
    });


    // Delete account form submission
    $('#delete-account-form').on('submit', function (e) {
        e.preventDefault();
        var password = $('#confirm-password').val();

        $.ajax({
            type: "POST",
            url: "/delete_account/",
            data: {
                'confirm_password': password
            },
            success: function (response) {
                console.log("Account successfully deleted.");
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error occurred while deleting account.");
                console.log(jqXHR, textStatus, errorThrown);
            }
        });
    });

    // Send suggestion form submission
    $('#send-suggestion-form').on('submit', function (e) {
        e.preventDefault();
        var suggestion = $('#suggestion').val();

        $.ajax({
            type: "POST",
            url: "/send_suggestion/",
            data: {
                'suggestion': suggestion
            },
            success: function (response) {
                console.log("Suggestion successfully sent.");
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error occurred while sending suggestion.");
                console.log(jqXHR, textStatus, errorThrown);
            }
        });
    });
});