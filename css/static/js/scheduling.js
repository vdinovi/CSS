// OnClick function for new section frame
// - Toggles between new section frame and filter frame
function switchFrame(firstFrame, secondFrame) {
    $("#"+firstFrame).hide();
    $("#"+secondFrame).show();
}

// String format function
String.prototype.format = function()
{
    var content = this;
    for (var i=0; i < arguments.length; i++)
    {
        var replacement = '{' + i + '}';
        var x;
        // Using a global replace with a var is annoying, simple workaround
        while (content != (x = content.replace(replacement, arguments[i])))
            content = x;
    }
    return content;
};

// Onclick func for filter type button
//  * If a new filter-type is selected:
//     - Unchecks any previousely selected filter types
//     - Populates the option window with all opions for selected filter type
//     - Checks all options that have already been selected for this filter type
//  * A filter type may not be un-selected
//     - Only set to inactive if another is selected
function selectFilter(element, filterType) {
    if (element.value == "inactive") {
        element.value = "active";
        element.className = "noselect filter-type-active";
        if (element.id != "course-filter-btn") {
            $("#course-filter-btn")[0].value = "inactive";
            $("#course-filter-btn")[0].className = "noselect filter-type";
        }
        if (element.id != "faculty-filter-btn") {
            $("#faculty-filter-btn")[0].value = "inactive";
            $("#faculty-filter-btn")[0].className = "noselect filter-type";
        }
        if (element.id != "room-filter-btn") {
            $("#room-filter-btn")[0].value = "inactive";
            $("#room-filter-btn")[0].className = "noselect filter-type";
        }
        if (element.id != "time-filter-btn") {
            $("#time-filter-btn")[0].value = "inactive";
            $("#time-filter-btn")[0].className = "noselect filter-type";
        }
        // Get options for this filter type
        $.ajax({
            type: "GET",
            url: "options",
            data: {type: element.innerHTML},
            success: function(response) {
                data = JSON.parse(response)
                var optionFormatString =
                    "<div id=\"option-{0}\" class=\"input-group\">\n" +
                    "  <span class=\"input-group-addon\">\n" +
                    "    <input id=\"option-checkbox\" type=\"checkbox\" onclick=\"selectOption(this)\">\n" +
                    "  </span>\n" +
                    "  <p class=\"form-control\">{0}</p>\n" +
                    "</div>\n";
                optionFrame = $("#option-frame");
                optionFrame.empty();
                for (var i in data.options) {
                    // Add to option window 
                    optionFrame.append(optionFormatString.format(data.options[i].name));
                    // Check if already in selected
                    $("#"+filterType).children("div").each(function(index, value) {
                        if (value.id == data.options[i].name) {
                            $("#option-"+data.options[i].name).children("span").children("input").prop("checked", true);
                        }

                    });
                }
            },
            error: function(err) {
                console.log('error: ' + err)
            }
        });
    }
}

// OnClick function for an option checkbox
// * If a new option is checked
//    - Populates filter window with option under its respetive type
// * If a an option is unchecked
//    - Removes option from filter window
//
// @TODO In order to determine the active filter type, it iterates through all
//       filter type and checks if active. 
//       This is not a very elegant way of doing this.
function selectOption(element) {
    var filterType;
    if ($("#course-filter-btn")[0].value == "active") 
        filterType = $("#course-options");
    else if ($("#faculty-filter-btn")[0].value == "active") 
        filterType = $("#faculty-options");
    else if ($("#room-filter-btn")[0].value == "active") 
        filterType = $("#room-options");
    else
        filterType = $("#time-options"); 
    // Add option to selected option list
    if (element.checked) {
        var optionFormatString = 
                    "<div id=\"{0}\"class=\"selected-option\">\n" +
                    "  <button onclick=\"unselectOption('{0}')\">x</button>\n" +
                    "  <li class=\"filter-options\">{0}</li>\n" +
                    "</div>"; 
        var text = element.parentNode.parentNode.innerText;
        filterType.append(optionFormatString.format(text));
    }
    // Remove option to selected option list
    else {
        filterType.children("div").each(function(index, value) {
            if (value.id == element.parentNode.parentNode.innerText)
                value.remove();
        });
    }
}

// OnClick function for removing a selected option
// * If a the selected options button is pressed
//    - Remove it from the selected options list
//    - Unselect option from options window
function unselectOption(name) {
    $("#option-frame").children("div").each(function(index, value) {
        if (name == value.children[1].innerHTML) {
            value.children[0].children[0].checked = false;
        }
    });
    $("#"+name).remove();
}

// OnClick function for a section checkbox
//  - Adds the section to the section detail
function selectSection(element) {
    //@TODO everything :(
    return true;
}

// OnClick function for a filter logic checkbox
// - Makes the and/or radio button enabled
function enableLogic(element) {

}

// OnClick function that adds the logic for this filter
function addLogic(element) {

}

