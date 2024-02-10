function showSpinner(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = "";
    element.classList.add("spinner-border");
}

let hideSpinnerTimeout1 = null;
let hideSpinnerTimeout2 = null;
function hideSpinner(elementId) {
    clearTimeout(hideSpinnerTimeout1);
    const element = document.getElementById(elementId);
    hideSpinnerTimeout1 = setTimeout(() => {
        clearTimeout(hideSpinnerTimeout2);
        element.classList.remove("spinner-border");
        element.innerHTML = "✔";
        hideSpinnerTimeout2 = setTimeout(() => {
            if (element.innerHTML === "✔") {
                element.innerHTML = "✏️";
            }
        }, 1500);
    }, 300);
}

function showLoadingSpinner(element) {
    console.log('showing loading spinner\nelement.id:', element.id);
    document.getElementById(element.id + "-loading").style.display = "block";
}

function hideLoadingSpinner(element) {
    console.log('hiding loading spinner\nelement.id:', element.id, '\nevent: ', event);
    document.getElementById(element.id + "-loading").style.display = "none";
    element.value = event.detail.xhr.responseText;
}