function updateOrderSections(orders, inputOrder, section) {
    let sectionTag = section + '-bookings';
    for (const [order, id] of Object.entries(orders)) {
        let viewID = '#booking-section-' + id;
        let buttonID = '#order-filter-button-' + id;
        if (inputOrder === id) {
            document.getElementById(sectionTag).querySelector(viewID).style.display = "block";
            document.getElementById(sectionTag).querySelector(buttonID).classList.add('rainbow-anim');
        }
        else {
            document.getElementById(sectionTag).querySelector(viewID).style.display = "none";
            document.getElementById(sectionTag).querySelector(buttonID).classList.remove('rainbow-anim');
        }
    }

}