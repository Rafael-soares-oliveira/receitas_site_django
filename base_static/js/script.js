function confirm_delete(params) {
    const forms = document.querySelectorAll(".form-delete");
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure you want to delete?')
            if (confirmed) {
                form.submit();
            }
        });
    }
}
confirm_delete()

function unpublish_recipe() {
    const forms = document.querySelectorAll(".form-unpublish");
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure you want to unpublish?')
            if (confirmed) {
                form.submit();
            }
        });
    }
}
unpublish_recipe()