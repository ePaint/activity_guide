var logo_element = document.getElementById('site-logo');
var max_size = 7;
var size_unit = 'rem';

function resizeLogo(page_y_offset) {
    var progress = Math.min(page_y_offset, 50) / 50;

    var shrink_factor = progress * 5;
    var new_size = max_size - shrink_factor;
    logo_element.style.width = new_size + size_unit;
    logo_element.style.height = new_size + size_unit;
    logo_element.style.marginLeft = `calc(50% - ${(new_size / 2)}${size_unit})`;
    logo_element.style.marginTop = 0.5 - 0.25 * progress + size_unit;
}

resizeLogo(window.pageYOffset);
window.onscroll = () => resizeLogo(window.pageYOffset);