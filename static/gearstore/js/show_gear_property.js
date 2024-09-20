function updateGearView(property, property_type) {
    let buttonClassName = 'gear-filter-' + property_type + '-button';

    let buttons = document.getElementsByClassName(buttonClassName);
    let buttonClickedID = 'gear-filter-' + property_type + '-button-' + property;
    Array.from(buttons).forEach((button) => {
        button.classList.remove("rainbow-anim")
    });
    document.getElementById(buttonClickedID).classList.add('rainbow-anim');

    let gear_hidden_class = property_type + '-card-link-hidden';
    let gear_property_class = 'menu-card-' + property_type + '-' + property;

    let gear_items = document.getElementsByClassName('menu-card-link')
    if (property === "all") {
        Array.from(gear_items).forEach((gear) => {
            gear.classList.remove(gear_hidden_class);
        });
    }
    else {
        Array.from(gear_items).forEach((gear) => {
            if (!(gear.classList.contains("add-menu-card"))) {
                console.log(gear_property_class);
                if (gear.classList.contains(gear_property_class)) {
                    gear.classList.remove(gear_hidden_class);
                }
                else {
                    gear.classList.add(gear_hidden_class);
                }
            }
        });
    }
}