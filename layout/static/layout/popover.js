function initializePopover(element_id) {
    var element = document.getElementById(element_id);
    deletePopover(element);
    return new bootstrap.Popover(element, {
        trigger: 'hover',
    });
}

function deletePopover(element) {
    var popover = bootstrap.Popover.getInstance(element);
    if (popover) popover.dispose();
}