function shareOnFacebook(path) {
    window.open('https://www.facebook.com/sharer/sharer.php?u=' + path, '_blank');
}

function shareOnTwitter(path) {
    window.open('https://twitter.com/intent/tweet?text=' + path, '_blank');
}

const shareByCopyIds = {};

function shareByCopy(element, path, new_src) {
    const img = element.querySelector('img');
    const old_src = img.src;
    navigator.clipboard.writeText(path);
    img.src = new_src;
    setTimeout(() => {
        img.src = old_src;
    }, 3000);
}