function copyMeasurementForm(e) {
    let formset = document.getElementById('measurement-formset-unique')
    let form = document.getElementById('measurement-form-last');
    let newForm = form.cloneNode(true);
    form.removeAttribute('id');
    // process newForm - increment id by one
    let children = newForm.childNodes;
    let array = [ ...children];
    for (let i=0; i<array.length; i++) {
        if(array[i].tagName === 'DIV') {
            let name = array[i].children[0].name.split('-')[2]
            let newId = Number(array[i].children[0].name.split('-')[1]) + 1
            let stringResult = `measurements-${newId}-${name}`;
            array[i].children[0]['id'] = `id_${stringResult}`;
            array[i].children[0]['name'] = stringResult;
            array[i].children[0]['value'] = '';
        }
    }
    // add newForm to DOM
    formset.appendChild(newForm);
    // update management formset django
    updateManagementForm('add');

}

function removeLastMeasurementForm(e) {
    // remove last form from formset
    let formset = document.getElementById('measurement-formset-unique');
    let form = document.getElementById('measurement-form-last');
    if (form.previousElementSibling != null) {
        form.previousElementSibling.id = 'measurement-form-last';
        formset.removeChild(form);
        updateManagementForm('remove');
    }
}

function updateManagementForm(action) {
    let management_form = document.getElementById('id_measurements-TOTAL_FORMS')
    if (action === 'add') {
        management_form.value = parseInt(management_form.value) + 1
    }
    else if (action === 'remove') {
        management_form.value = parseInt(management_form.value) - 1
    }
}

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    copyMeasurementForm(e);
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    removeLastMeasurementForm(e);
    return false;
});
