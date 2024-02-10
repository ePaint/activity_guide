const scrollToTop = () => window.scrollTo({top: 0, behavior: 'smooth'});

const scrollToElementId = (element_id) => {
    if (!element_id) return scrollToTop();
    const element = document.getElementById(element_id);
    if (!element) return;
    const header_height = document.getElementById('site-header').offsetHeight;
    const y = element.getBoundingClientRect().top + window.scrollY - header_height;
    window.scroll({top: y, behavior: 'smooth'});
}

document.addEventListener('htmx:afterRequest', function(evt) {
    if (evt.detail.successful != true) return;
    
    switch (evt.detail.target.id) {
        case 'main-content':
            scrollToElementId(evt.detail.requestConfig.parameters.scrollTo);
            break;
        default:
            break;
    }
});

const notOnHomepage = () => {
    console.log(window.location.pathname);
    return window.location.pathname != '/';
}

function disableScroll() {
    window.removeEventListener('scroll', handleScroll);
    if ($(document).height() > $(window).height()) {
        const scroll_top = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop();
        $('html').addClass('noscroll').css('top',-scroll_top);         
    }
}

function enableScroll() {
    window.addEventListener('scroll', handleScroll);
    const scroll_top = parseInt($('html').css('top'));
    $('html').removeClass('noscroll');
    window.scrollTo({top: -scroll_top, behavior: 'instant'});
}