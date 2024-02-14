var modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('modal_global'), {
    backdrop: 'static',
    keyboard: false,
});
document.body.addEventListener("close-modal", () => modal.hide());
document.body.addEventListener("reload-page", () => location.reload());
