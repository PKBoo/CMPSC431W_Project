
$(document).ready(function() {
    $('.delete-user').on('click', function() {
        var user = $(this).attr('data-user');
        var deleteRequest = $.ajax({
            method: 'DELETE',
            url: '/api/users/' + user
        });
        deleteRequest.then(function(data) {
            $('#user-' + user).remove();
        });

    });
});