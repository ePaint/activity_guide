function disableContactForm() {
    document.getElementById("contact-form-spinner").classList.remove("d-none");
    document.getElementById("contact-form-submit").disabled = true;
    document.getElementById("contact-form-fieldset").disabled = true;
}