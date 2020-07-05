
function copyForm(e) {
    let formset = document.getElementById('measurement-formset-unique')
    let form = document.getElementById('measurement-form-last');
    let newForm = form.cloneNode(true);
    form.removeAttribute('id');
    // process newForm - increment id by one
    let children = newForm.childNodes;
    let array = [ ...children];
    for (let i=0; i<array.length; i++) {
        if(array[i].tagName === 'INPUT') {
            let name = array[i].name.split('-')[2]
            let newId = Number(array[i].name.split('-')[1]) + 1
            let stringResult = `measurements-${newId}-${name}`;
            array[i]['id'] = `id_${stringResult}`;
            array[i]['name'] = stringResult;
        }
    }
    // add newForm to DOM
    formset.appendChild(newForm);
}

function removeLastForm(e) {
    // remove last form from formset
    let formset = document.getElementById('measurement-formset-unique')
    let form = document.getElementById('measurement-form-last');
    if (form.previousElementSibling != null) {
        form.previousElementSibling.id = 'measurement-form-last'
        formset.removeChild(form);
    }
}
//Tworzymy handlery:
// dla wybranego zdarzenia (arg 1)
// elementow html o pasujacych selektorach (2 arg),
// implementacja obslugi wywolania handlera (3 arg)
$(document).on('click', '.add-form-row', function(e){
    // zabezpieczamy się przed wykonaniem domyślnych akcji dla zdarzenia e - chcemy tylko wykonac nasze
    e.preventDefault();
    copyForm(e);
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    removeLastForm(e);
    return false;
});
