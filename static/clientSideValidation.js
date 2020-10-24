(function () {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            ['keyup', 'submit'].forEach(function(e) {
                form.addEventListener(e, function(event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    // measurement pallet uniqueness logic check
                    let palletNumberInputs = document.getElementsByClassName("measurements-pallet_number");
                    if (palletNumberInputs.length > 0) {
                        let array = [...palletNumberInputs];
                        let palletNumberValues = [];
                        for (let i=0; i<array.length; i++) {
                            let palletNumber = array[i].value;
                            if (palletNumberValues.includes(palletNumber)) {
                                palletNumberInputs[i].style.color = 'red';
                            }
                            else {
                                palletNumberInputs[i].style.color = '';
                            }
                            palletNumberValues.push(array[i].value);
                        }
                        if (new Set(palletNumberValues).size !== palletNumberValues.length) {
                            event.preventDefault();
                            event.stopPropagation();
                        }
                    }
                    form.classList.add('was-validated');
                })
            }, false);
        });
    }, false);
})(
);