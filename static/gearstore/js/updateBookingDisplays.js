function updateBookingDisplays(statuses, clickedStatus, orderID, section){
    let orderTag = '#booking-section-' + orderID;
    let sectionTag = section + '-bookings';
    let buttonStatusMap = Object.create(null);
    statuses.forEach((status) => {
        var id = '#booking-filter-button-' + status;
        buttonStatusMap[status] = document.getElementById(sectionTag).querySelector(orderTag).querySelector(id);
    });

    let divStatusMap = Object.create(null);
    statuses.forEach((status) => {
        let id = '#bookings-view-' + status;
        divStatusMap[status] = document.getElementById(sectionTag).querySelector(orderTag).querySelector(id);
    });

    let colourStatusMap = Object.create(null);
    colourStatusMap['Active'] = "#b2bda6";
    colourStatusMap['Requested'] = "#e8d9b7";
    colourStatusMap['Accepted'] = "#b5c9c6";
    colourStatusMap['Denied'] = "#d6bcb8";
    colourStatusMap['Returned'] = "#dacfe3";
    colourStatusMap['Unreturned'] = "#c9c7c7";

    if (clickedStatus === "All") {
        statuses.forEach((status) => {
            if (status != "All") {
                divStatusMap[status].style.display = "flex";
                buttonStatusMap[status].style.background= "";
            }
        });
        buttonStatusMap["All"].classList.add("rainbow-anim");
    }
    else {
        statuses.forEach((status) => {
            if (status != "All") {
                divStatusMap[status].style.display = "none";
                buttonStatusMap[status].style.background= "";
            }
        });
        buttonStatusMap["All"].classList.remove("rainbow-anim");
        divStatusMap[clickedStatus].style.display = "flex";
        buttonStatusMap[clickedStatus].style.background = colourStatusMap[clickedStatus];

    }
}