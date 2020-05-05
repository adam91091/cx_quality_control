
function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElements = $(selector).clone(true);
    //update management form total value
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    console.log("TOTAL"+total)
    console.log(newElements.find('input'))
    //update name and ids attributes - increment for 1
    newElements.find('input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-2) + '-', '-' + (total-1) + '-');
        var id = 'id_' + name;
        console.log(name)
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    console.log(newElements.find('input'))
    //update labels for inputs - optional for work, TODO
    // newElements.find('label').each(function() {
    //     var forValue = $(this).attr('for');
    //     if (forValue) {
    //       forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
    //       $(this).attr({'for': forValue});
    //     }
    // });
    //remove ids from newElement
    newElements.each(function() {
       $(this).attr({'id': '-'});
    });
    //add new element into each row
    newElements.each(function(i, el) {
        console.log(i)
        $("#"+i).after(el);
    })
    // clear previous last elements
    newElements.each(function(i, el) {
        $("#"+i).attr({'id': '-', 'class': '-'})
    })
    //set ids newly added elements
    newElements.each(function(i, el) {
        $(this).attr({'id': i})
    })

    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');
    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
$(document).on('click', '#add-form-row', function(e){
    e.preventDefault();
    cloneMore('.to-copy', 'measurements');
    return false;
});
$(document).on('click', '#remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});
