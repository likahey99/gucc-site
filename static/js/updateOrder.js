function updateOrderSections(orders, inputOrder) {
    console.log(inputOrder)
    for (const [order, id] of Object.entries(orders)) {
        let viewID = 'booking-section-' + id;
        let buttonID = 'order-filter-button-' + id;
        console.log(order)
        if (inputOrder === id) {
            document.getElementById(viewID).style.display = "block";
            document.getElementById(buttonID).classList.add('rainbow-anim');
        }
        else {
            document.getElementById(viewID).style.display = "none";
            document.getElementById(buttonID).classList.remove('rainbow-anim');
        }
    }

}