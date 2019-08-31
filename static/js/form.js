function new_header() {
    if (typeof new_header.counter == 'undefined') {
        new_header.counter = 0;
    }

    if (new_header.counter === 0) {
        $("<div class=\"row\"><div class=\"col-5\"><label>Header Tags</label></div><div class=\"col-6\"><label>Header Values</label></div>").appendTo("#headers");
    }

    new_header.counter++;

    let row = $("<div class='row'></div>");
    row.attr("id", "row" + new_header.counter).appendTo("#headers");

    let tag_col = $("<div class='col-5'></div>");
    tag_col.attr("id", "htc" + new_header.counter).appendTo("#row" + new_header.counter);

    let value_col = $("<div class='col-6'></div>");
    value_col.attr("id", "hvc" + new_header.counter).appendTo("#row" + new_header.counter);

    let delete_col = $("<div class='col-1'></div>");
    delete_col.attr("id", "delc" + new_header.counter).appendTo("#row" + new_header.counter);

    let tag = $("<input type='text' name='tag' class='form-control' required/><br>");
    let value = $("<input type='text' name='value' class='form-control' required/><br>");

    let delete_button = $("<button type='button' class='btn btn-danger'><i class='fa fa-times'></i></button>").attr("onclick", "delete_header(" + new_header.counter + ")");
    delete_button.attr("id", "del" + new_header.counter);

    tag.attr("placeholder", "Tag").appendTo("#htc" + new_header.counter);
    value.attr("placeholder", "Value").appendTo("#hvc" + new_header.counter);
    delete_button.appendTo("#delc" + new_header.counter);
}

function new_edit_header() {
    if (typeof new_edit_header.counter == 'undefined') {
        new_edit_header.counter = $("#headers > div").length;
    }

    if (new_edit_header.counter === 0) {
        $("<div class=\"row\"><div class=\"col-5\"><label>Header Tags</label></div><div class=\"col-6\"><label>Header Values</label></div>").appendTo("#headers");
    }

    new_edit_header.counter++;

    let row = $("<div class='row'></div>");
    row.attr("id", "row" + new_edit_header.counter).appendTo("#headers");

    let tag_col = $("<div class='col-5'></div>");
    tag_col.attr("id", "htc" + new_edit_header.counter).appendTo("#row" + new_edit_header.counter);

    let value_col = $("<div class='col-6'></div>");
    value_col.attr("id", "hvc" + new_edit_header.counter).appendTo("#row" + new_edit_header.counter);

    let delete_col = $("<div class='col-1'></div>");
    delete_col.attr("id", "delc" + new_edit_header.counter).appendTo("#row" + new_edit_header.counter);

    let tag = $("<input type='text' name='tag' class='form-control' required/><br>");
    let value = $("<input type='text' name='value' class='form-control' required/><br>");

    let delete_button = $("<button type='button' class='btn btn-danger'><i class='fa fa-times'></i></button>").attr("onclick", "delete_header(" + new_edit_header.counter + ")");
    delete_button.attr("id", "del" + new_edit_header.counter);

    tag.attr("placeholder", "Tag").appendTo("#htc" + new_edit_header.counter);
    value.attr("placeholder", "Value").appendTo("#hvc" + new_edit_header.counter);
    delete_button.appendTo("#delc" + new_edit_header.counter);
}

function toggle_headers() {
    let default_headers = $("#default_headers");
    if (default_headers.is('[hidden]')) {
        default_headers.removeAttr("hidden");
        $("#toggle_button").text("Hide Standard Headers ").append($("<i class='fa fa-edit'></i>"));
    } else {
        default_headers.attr("hidden", "");
        $("#toggle_button").text("Edit Standard Headers ").append($("<i class='fa fa-edit'></i>"));
    }
}

function toggle_users() {
    let user_permissions = $("#user_permissions");
    if (user_permissions.is('[hidden]')) {
        user_permissions.removeAttr("hidden");
        $("#toggle_users_button").text("Hide User Permissions ").append($("<i class='fa fa-edit'></i>"));
    } else {
        user_permissions.attr("hidden", "");
        $("#toggle_users_button").text("Edit User Permissions ").append($("<i class='fa fa-edit'></i>"));
    }
}

function delete_header(counter) {
    $("#row" + counter).remove();
}
