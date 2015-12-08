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
        var newTag = $('#newTag').val().trim();
        if (newTag !== '' && newTag.indexOf(' ') === -1) {
            if (!customTagExists(newTag)) {
                console.log('add new valid tag');
                addCustomTag(newTag);
                var newListElement = $('<li>' + newTag +
                    ' <span id="remove-tag' + newTag + '" class="remove-tag" data-tagid="' + newTag + '"><span class="glyphicon glyphicon-remove text-danger"></span></span></li>');
                $('#current-tags').append(newListElement);
                $('#remove-tag'+newTag).on('click', function() {
                    removeCustomTag($(this).attr('data-tagid'));
                    $(this).parent().remove();
                });
                $('#newTag').val('');
            } else {
                alert('Tag has already been added.');
            }
        } else {
            alert('Tag must have no spaces.')
        }
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

function addCustomTag(tag) {
    var currentCustomTags = $('#customTags').val();
    if (currentCustomTags === '') {
        $('#customTags').val(tag);
    } else {
        $('#customTags').val(currentCustomTags + ',' + tag);
    }
}

function removeCustomTag(tag) {
    var currentCustomTags = $('#customTags').val().split(',');

    for (var i = 0; i < currentCustomTags.length; i++) {
        if (currentCustomTags[i] === tag) {
            currentCustomTags.splice(i, 1);

        }
    }

    $('#customTags').val(currentCustomTags.join(','));
}

function customTagExists(tag) {
    var currentCustomTags = $('#customTags').val().split(',');
    for (var i = 0; i < currentCustomTags.length; i++) {
        if (currentCustomTags[i] === tag) {
            return true
        }
    }

    return false;
}



