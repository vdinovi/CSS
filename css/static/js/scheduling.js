/* *** GLOBALS *** */
const filters = ["course", "faculty", "room", "time"];

/* *** UTILITY *** */
// String format function. 
// Replaces {n} in format string with n-th positional arg.
String.prototype.format = function()
{
    var content = this;
    for (var i=0; i < arguments.length; i++)
    {
        var replacement = '{' + i + '}';
        var x;
        // Can't wrap var 'replacement' with regex in order to do global replace.
        // Instead iterate until once pass completes with no replacements.
        while (content != (x = content.replace(replacement, arguments[i])))
            content = x;
    }
    return content;
};

/* *** FRAME *** */
// OnClick function for new section frame
// - Toggles between new section frame and filter frame
function switchFrame(firstFrame, secondFrame) {
    $("#"+firstFrame).hide();
    $("#"+secondFrame).show();
}

// Populate 'view-term' modal with all terms
$('#view-term-modal').on('show.bs.modal', function () {
    getSchedules();
});
$('#delete-term-modal').on('show.bs.modal', function (e) {
    var academicTerm = $(e.relatedTarget).data('name');
    $("#delete-term-modal-body").find("form").children("h3").remove();
    $("#delete-term-modal-body").find("form").children("button").remove();
    $("#delete-term-modal-body").find("form").append(
        "<h3>Are you sure you want to delete the schedule for " + academicTerm + "?</h3>\n" +
        "<input type=\"hidden\" name=\"academic-term\" value=\""+ academicTerm + "\"></input>" +
        "<button type=\"submit\" name=\"delete-schedule\" class=\"btn\">\n" +
        "Yes I want to delete this schedule!</button>"
    );
}); 
$('#approve-term-modal').on('show.bs.modal', function (e) {
    var academicTerm = $(e.relatedTarget).data('name');
    $("#approve-term-modal-body").find("form").children("h3").remove();
    $("#approve-term-modal-body").find("form").children("button").remove();
    $("#approve-term-modal-body").find("form").append(
        "<h3>Are you sure you want to approve the schedule for " + academicTerm + "?</h3>\n" +
        "<input type=\"hidden\" name=\"academic-term\" value=\""+ academicTerm + "\"></input>" +
        "<button type=\"submit\" name=\"approve-schedule\" class=\"btn\">\n" +
        "Yes I want to approve this schedule!</button>"
    );
}); 

/* *** TERM *** */
// OnClick function for view term
// * When clicked
//    - modal pops up and shows all existing schedules not currently selected
function getSchedules() {
    $.ajax({
        type: "GET",
        url: "schedules",
        success: function(response) {
            data = JSON.parse(response);
            list = $("#view-term-modal-body").children("div");
            var scheduleFormatString = "<button class=\"list-group-item\" onclick=\"addSchedule('{0}')\">{0}</button>\n";
            list.empty();
            for (var i = 0; i < data.active.length; ++i) {
                list.append(scheduleFormatString.format(data.active[i].academic_term));
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

// OnClick function function for adding a schedule 
// * Adds selected schedule to term bar
function addSchedule(name) {
    // Id field to use for dropdown button (for easy querying). Replaces all ' ' with '-'.
    var scheduleId = name.replace(/ /g, '-');
    var scheduleFormatString = 
        "<li class=\"dropdown\">\n" +
        "  <a id=\"{0}\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">{1}<b class=\"caret\"></b></a>\n" +
        "  <ul class=\"dropdown-menu\">\n" +
        "    <li><a href=\"#\" onclick=\"selectSchedule('{0}')\">Select Schedule</a></li>\n" +
        "    <li><a href=\"#\" data-toggle=\"modal\" data-name=\"{1}\" data-target=\"#approve-term-modal\">Approve Schedule</a></li>\n" +
        "    <li><a href=\"#\" onclick=\"closeSchedule('{0}')\">Close Tab</a></li>\n" +
        "    <li><a href=\"#\" data-toggle=\"modal\" data-name=\"{1}\" data-target=\"#delete-term-modal\">Delete Schedule</a></li>\n" +
        "  </ul>\n" +
        "</li>\n";
    var alreadyPresent = false;
    // Check if tab is already open
    $("#open-terms").children("li").children("a").each(function (index, value) {
        if (name == value.innerText) {
            alreadyPresent = true;
        }
    });
    if (!alreadyPresent) {
        // If not already in list, add to front
        $("#open-terms").prepend(scheduleFormatString.format(scheduleId, name)); 
        // Activate dropdown
        $("#"+scheduleId).dropdown();
    }
}

// Select a schedule from tab
function selectSchedule(name) {
    // De-select existing active schedule
    $("#open-terms").children("li").each(function (index, value) {
        value.className = "";
    });
    $("#"+name).parent().addClass("active-schedule");
}

// Gets the currently selected term. If none, returns false
function getSelectedSchedule() {
    terms = $("#open-terms").children("li");
    for (var i = 0; i < terms.length; ++i) {
        if (terms[i].className.includes("active-schedule")) {
            return terms[i].childNodes[1].innerText;
        }
    }
    return false;
}

// Close a schedule
function closeSchedule(name) {
    $("#"+name).parent().empty();
}

// Approve a schedule
function approveSchedule(name) {
    //@TODO
    console.log("approveSchedule<NYI>");
}

/* *** FILTER / OPTIONS *** */ 

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
        // Unselect other filter types
        for (var i = 0; i < filters.length; ++i) {
            var btnName = filters[i] + "-filter-btn";
            if (element.id != btnName) {
                $("#"+btnName)[0].value = "inactive" 
                $("#"+btnName)[0].className = "noselect filter-type"; 
            }
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
function selectOption(element) {
    var filterType;
    // Get correct filter type (where to put selected option)
    for (var i = 0; i < filters.length; ++i) {
        if ($("#"+filters[i]+"-filter-btn")[0].value == "active") {
            filterType = $("#"+filters[i]+"-options");
            break;
        }
    }
   // Add option to selected option list
    if (element.checked) {
        var optionFormatString = 
                    "<div id=\"{0}\"class=\"selected-option\">\n" +
                    "  <button onclick=\"unselectSelectedOption('{0}')\">x</button>\n" +
                    "  <li class=\"filter-options\">{0}</li>\n" +
                    "</div>"; 
        var text = element.parentNode.parentNode.innerText;
        filterType.append(optionFormatString.format(text));
    }
    // Remove option from selected option list
    else {
        filterType.children("div").each(function(index, value) {
            if (value.id == element.parentNode.parentNode.innerText)
                value.remove();
        });
    }
}

// Unselect all selected options
function unselectAllSelectedOptions() {
    for (var i = 0; i < filters.length; ++i) {
        $("#"+filters[i]+"-options").children("div").each(function(index, value) {
            unselectSelectedOption(value.id);
        });
    }
}

// OnClick function for removing a selected option
// * If a the selected options button is pressed
//    - Remove it from the selected options list
//    - Unselect option from options window
function unselectSelectedOption(name) {
    $("#option-frame").children("div").each(function(index, value) {
        if (name == value.children[1].innerHTML) {
            value.children[0].children[0].checked = false;
        }
    });
    $("#"+name).remove();
}

// Retreive all currently selected options as a struct 4 named arrays
// {
//    "course": [...],
//    "faculty": [...],
//    "room": [...],
//    "time": [...],
// }
function getSelectedOptions() {
    var selectedOptions = {};
    // Iterate over each filter types option list
    var f = 0;
    $("#filter-type-window").children("span").each(function (index, value) {
        var arr = [];
        // Iterate over each selected option type
        for (var i = 0; i < value.children.length; ++i) {
            arr.push(value.children[i].id); 
        }
        var name = filters[f++];
        selectedOptions[name] = arr;
    });
    return selectedOptions;
 
}

/* *** FILTER LOGIC / SECTIONS *** */

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


// OnClick function to set the days for a new section
function setDays(element, form) {
    form.days=element.id;
    form.save();
}
