var logo_element = document.getElementById('site-logo');
var logo_max_size = 7;
var logo_min_size = 2;
var logo_size_unit = 'rem';

function resizeLogo(page_y_offset) {
    var progress = Math.min(page_y_offset, 50) / 50;
    var shrink_factor = progress * (logo_max_size - logo_min_size);
    var logo_new_size = logo_max_size - shrink_factor;
    logo_element.style.width = logo_new_size + logo_size_unit;
    logo_element.style.height = logo_new_size + logo_size_unit;
    logo_element.style.marginLeft = `calc(50% - ${(logo_new_size / 2)}${logo_size_unit})`;
    logo_element.style.marginTop = 0.5 - 0.25 * progress + logo_size_unit;
}

var header_element = document.getElementById('site-header');
var header_max_size = 4.5;
var header_min_size = 0;
var header_size_unit = 'rem';
var prev_page_y_offset = 0;

function resizeHeader(page_y_offset) {
    window.onscroll = () => {};
    var distance = page_y_offset - prev_page_y_offset;
    
    if (distance > 0) {
        header_element.style.top = '-4.5rem';
    } else {
        header_element.style.top = '0';
    }

    prev_page_y_offset = page_y_offset;
    window.onscroll = () => handleScroll();
}

function handleScroll() {
    if (window.innerWidth > 575) {
        resizeLogo(window.pageYOffset);
    } else {
        resizeHeader(window.pageYOffset);
    }
}

resizeLogo(window.pageYOffset);
window.onscroll = () => handleScroll();