$(document).ready(function() {

    $('#addTag').on('click', function() {
        var selectedTagId = $('#alltags').val();
        var selectedTagName = $("#alltags option[value='" + selectedTagId + "']").text()

        if (!tagExists(selectedTagId)) {
            addTag(selectedTagId);
            var newListElement = $('<li>' + selectedTagName +
                ' <span id="remove-tag' + selectedTagId + '" class="remove-tag" data-tagid="' + selectedTagId + '"><span class="glyphicon glyphicon-remove text-danger"></span></span></li>');

            $('#current-tags').append(newListElement);

            $('#remove-tag'+selectedTagId).on('click', function() {
                removeTag($(this).attr('data-tagid'));
                $(this).parent().remove();
            });
        } else {

        }
    });

    $('#createTag').on('click', function() {

    });

});

function tagExists(tagId) {
    var currentTags = $('#currentTags').val().split(',');
    for (var i = 0; i < currentTags.length; i++) {
        if (currentTags[i] === tagId) {
            return true;
        }
    }

    return false;
}

function addTag(tagId) {
    var currentTags = $('#currentTags').val();

    if (currentTags === '') {
        $('#currentTags').val(tagId);
    } else {
        $('#currentTags').val(currentTags + ',' + tagId);
    }
}

function removeTag(tagId) {
    var currentTags = $('#currentTags').val().split(',');

    for (var i = 0; i < currentTags.length; i++) {
        if (currentTags[i] === tagId) {
            currentTags.splice(i, 1);

        }
    }

    $('#currentTags').val(currentTags.join(','));
}

