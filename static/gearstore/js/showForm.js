function showHiddenForm() {
    var form = document.getElementById("account-change-form");
    var button = document.getElementById("action-button");
    if (form.style.display != "flex") {
        form.style.display = "flex";
        button.innerHTML = "Hide Account Manager"
    }
    else {
        form.style.display = "none";
         button.innerHTML = "Manage Account";
    }
}

function showCommentForm() {
    var form = document.getElementById("add-comment-form");
    var button = document.getElementById("action-button");
    if (form.style.display != "block") {
        form.style.display = "block";
        button.innerHTML = "Hide Comment Prompt"
    }
    else {
        form.style.display = "none";
         button.innerHTML = "Add Comment";
    }
}

function setBorrowMenu(menu){
    const user_bookings = document.getElementById("user-bookings");
    const all_bookings = document.getElementById("all-bookings");
    const user_bookings_title = document.getElementById("user-bookings-title");
    const all_bookings_title = document.getElementById("all-bookings-title");
    if (menu == "user"){
        user_bookings.style.display = "block";
        all_bookings.style.display = "none";
        user_bookings_title.classList.add("rainbow-anim");
        all_bookings_title.classList.remove("rainbow-anim");
    }
    else if (menu == "all"){
        all_bookings.style.display = "block";
        user_bookings.style.display = "none";
        all_bookings_title.classList.add("rainbow-anim");
        user_bookings_title.classList.remove("rainbow-anim");
    }
}