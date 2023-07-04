function show_popup(popup_type, comment_id, extra_param) {
    let popup_id = popup_type + "_comment_form";
    let popup = document.getElementById(popup_id);
    let popup_hidden_id = "#" + popup_type + "_id";
    let popup_id_input = popup.querySelector(popup_hidden_id);

    popup_id_input.value = comment_id;
    popup.style.display = "block";

    starred_status_text = popup.querySelector("#starred_status_text");
    if (starred_status_text) {
        starred_status_text.innerText = "This action will set the starred status to " + !(extra_param) + ".";
    }

    edit_comment_box = popup.querySelector("#edit_comment_box");
    if (edit_comment_box) {
        edit_comment_box.value = extra_param;
    }
}

function hide_popup(popup_type) {
    let popup_id = popup_type + "_comment_form";
    let popup = document.getElementById(popup_id);
    let popup_hidden_id = "#" + popup_type + "_id";
    let popup_id_input = popup.querySelector(popup_hidden_id);

    popup.style.display = "none";
    popup_id_input.value = "";

    edit_comment_box = popup.querySelector("#edit_comment_box");
    if (edit_comment_box) {
        edit_comment_box.value = "";
    }

    password_box = popup.querySelector("#password");
    if (password_box) {
        password_box.value = "";
    }

}