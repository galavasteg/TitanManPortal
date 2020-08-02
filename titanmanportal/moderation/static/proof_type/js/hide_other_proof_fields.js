(function($) {
    $(() => {
        const selectField = $('#id_proofs-0-type'),
              proofTypeMap = {
                image: $('.field-proof_image'),
                link: $('.field-proof_link'),
                text: $('.field-proof_text'),
              },
              proofFields = new Set(Object.values(proofTypeMap));

        const toggleProofFieldsHide = (value) => {
            if (value) {
                const toShowField = proofTypeMap[value],
                      toHideFields = new Set(
                        [...proofFields].filter(x => x !== toShowField));
                toShowField.show();
                toHideFields.forEach(x => x.hide());
            } else {
                proofFields.forEach(x => x.hide());
            }
        };

        // show/hide on load based on pervious value of selectField
        toggleProofFieldsHide(selectField.val());
        // show/hide on change
        selectField.change(function() {
            toggleProofFieldsHide($(this).val());
        });
    });
})(django.jQuery);
