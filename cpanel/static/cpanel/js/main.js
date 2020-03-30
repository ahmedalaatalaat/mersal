$('#add_form').submit(function (e) {
    e.preventDefault();
    if ($('#add_form').parsley().isValid()) {
        $.ajax({
            method: 'POST',
            url: window.location.href,
            data: new FormData(this),
            contentType: false,
            processData: false,
            success: function (data) {
                if ((window.location.href).includes('/ar')) {
                    $.growl.notice({ title: "اشعار", message: "تم حفظ البيانات بنجاح", location: 'tl' });
                } else {
                    $.growl.notice({ title: "Add Notice", message: "New data has been added successfully" });
                }
                if ((window.location.href).includes('_add')) {
                    document.getElementById("add_form").reset();
                    $('#image_label').html('Choose Image');
                }
            },
            error: function (error_data) {
                var message = error_data.responseText
                if ((window.location.href).includes('/ar')) {
                    $.growl.error({ title: "إشعار بخطأ", message: message, location: 'tl' });
                } else{
                    $.growl.error({ title: "Error Notice", message: message });
                }
            }
        });
    }

});


function delete_item(id) {
    swal({
        title: "Are you sure",
        text: "Do you want to delete " + id,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        $.ajax({
            method: 'POST',
            url: window.location.href,
            data: {
                id: id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                type: 'delete'
            },
            success: function (data) {
                $('#' + id).remove();
                swal("Deleted!", id + " has been deleted.", "success");
            }
        });

    });
}

function image_upload() {
    if ($('#customFile').val() != "") {
        $('#image_label').html($('#customFile').val());
    }
}

function to_english() {
    var loc = window.location.href;
    window.location.href = loc.slice(0, loc.search('/ar')) + loc.slice(loc.search('/ar') + 3);
}

function to_arabic() {
    var loc = window.location.href;
    window.location.href = loc.slice(0, loc.search('/cpanel')) + '/cpanel/ar' + loc.slice(loc.search('/cpanel') + 7);
}
