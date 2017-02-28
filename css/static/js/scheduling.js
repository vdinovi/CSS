/* *** GLOBALS *** */
const filter_types = ["course", "faculty", "room", "time"];
var filters = {"course":{"logic":"and", "filters":[]}, "faculty":{"logic":"and", "filters":[]}, "room":{"logic":"and", "filters":[]}, "time":{"logic": "and", "filters":{"MWF":[], "TR":[]}}}

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

// Compare two time strings
// Returns 0 if equal, -1 if A < B, and 1 if A > B
function compareTime(timeA, timeB) {
    var startTimeParse = timeA.split(":");
    var endTimeParse = timeB.split(":");
    var firstHour = parseInt(startTimeParse[0]);
    var firstMinute = parseInt(startTimeParse[1]);
    var secondHour = parseInt(endTimeParse[0]);
    var secondMinute = parseInt(endTimeParse[1]);
    if (firstHour == secondHour) {
        if (firstMinute == secondMinute)
            return 0;
        if (firstMinute < secondMinute)
            return -1
        return 1
    }
    else {
        if (firstHour < secondHour)
            return -1
        return 1
    }
}

// Convert Military formatted time to standard
function toStandardTime(time) {
    //@TODO convert from military to standard
    // -- Buggy, fix this
    var timeParse = timeA.split(":");
    var hour = parseInt(startTimeParse[0]);
    var minute = parseInt(startTimeParse[1]);
    var half;
    if (hour >= 12)
        half = "PM";
    else {
        half = "AM";
        if (hour == 0)
            hour = 12
    }
    var paddedHour;
    var paddedMinute;
    if (hour < 10)
        paddedHour = "0"+hour;
    if (minute < 10)
        paddedMinute = "0"+minute
    var stdTime = "{0}:{1} {2}";
    return stdTime.format(paddedHour, paddedMinute, half);
}

// Convert Standard formmated time to military 
function toStandardTime(time) {
    //@TODO convert from standard to military
}

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
        for (var i = 0; i < filter_types.length; ++i) {
            var btnName = filter_types[i] + "-filter-btn";
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
                optionFrame = $("#option-frame");
                optionFrame.empty();
                // Filter Type is time
                if (filterType == "time-options") {
                    var optionFormatString = 
                        "<div id=\"time-option-window\" class=\"time-option-window\">\n" +
                        "  <div class=\"btn-group\" role=\"group\" aria-label=\"...\">\n" +
                        "    <div class=\"col-xs-12\"style=\"margin-top:30px;\">\n" +
                        "      <button id=\"mwf-btn\" type=\"button\" class=\"btn btn-primary\" value=\"active\" onclick=\"selectDay('mwf')\" style=\"display:inline-block;\">MWF</button>\n" +
                        "      <button id=\"th-btn\" type=\"button\" class=\"btn btn-default\" value=\"inactive\" onclick=\"selectDay('th')\" style=\"display:inline-block;\">TH</button>\n" +
                        "    </div>\n" +
                        "    <div class=\"col-xs-12\" style=\"margin-top:30px;\">\n" +
                        "      <label for=\"start-time\">Start Time:</label>\n" +
                        "      <input id=\"start-time\" type=\"time\" name=\"start-time\"></input>\n" +
                        "    </div>\n" +
                        "    <div class=\"col-xs-12\" style=\"margin-top:30px;\">\n" +
                        "      <label for=\"end-time\">End Time:</label>\n" +
                        "      <input id=\"end-time\" type=\"time\" name=\"end-time\"></input>\n" +
                        "    </div> \n" +
                        "    <div class=\"col-xs-12\" style=\"text-align:center; margin-top:30px;\">\n" +
                        "      <button class=\"btn btn-primary\" onclick=\"selectTime('{0}', '{1}')\">Save</button>\n" +
                        "    </div>\n" +
                        "  </div>\n" + 
                        "</div>";
                    //@NOTE Currently gets start and end time as miliatry time
                    //optionFrame.append(optionFormatString.format(toStandardTime(data.start_time), toStandardTime(data.end_time)));
                    optionFrame.append(optionFormatString.format(data.start_time, data.end_time));
                }
                // Filter Type is course, faculty, or room
                else {
                    var optionFormatString =
                        "<div id=\"option-{0}\" class=\"input-group\">\n" +
                        "  <span class=\"input-group-addon\">\n" +
                        "    <input id=\"option-checkbox\" type=\"checkbox\" onclick=\"selectOption(this)\">\n" +
                        "  </span>\n" +
                        "  <p class=\"form-control\">{0}</p>\n" +
                        "</div>\n";
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
                }
            },
            error: function(err) {
                console.log('error: ' + err)
            }
        });
    }
}

// OnClick for day group buttons in time option window
function selectDay(dayGroup) {
    // Check if button is already selected
    if ($("#"+dayGroup+"-btn")[0].value == "active") {
        // Button is already selected
        return false;
    }
    if (dayGroup == "mwf") {
        $("#th-btn")[0].value = "inactive"; 
        $("#th-btn")[0].className = "noselect btn btn-default";
        $("#mwf-btn")[0].className = "noselect btn btn-primary";
    }
    else {
        $("#mwf-btn")[0].value = "inactive"; 
        $("#mwf-btn")[0].className = "noselect btn btn-default";
        $("#th-btn")[0].className = "noselect btn btn-primary"; 
    }
}

// Validate and Get the time from the time option window
// returned time object of form:
// {
//   "day": "mwf",
//   "startTime": "8:00:00",
//   "endTime": "20:00:00"
// }
function selectTime(minTime, maxTime) {
    var time = {};
    if ($("#mwf-btn")[0].value == "active")
        time.day = "mwf";
    else
        time.day = "th";
    var startTime = $("#start-time").val();
    var endTime = $("#end-time").val();
    if ((compareTime(startTime, minTime)) < 1 || (compareTime(startTime, maxTime) > 0)) {
        //@TODO implement and use toStandardTime
        sweetAlert("Invalid Start Time", "Department Hours: "+minTime+" - "+maxTime);
        return false;
    }
    if ((compareTime(endTime, minTime) < 1) || (compareTime(endTime, maxTime) > 0)) {
        //@TODO implement and use toStandardTime
        sweetAlert("Invalid End Time", "Department Hours: "+minTime+" - "+maxTime);
        return false;
    }
    //@TODO Verify start comes before end
    time.startTime = startTime;
    time.endTime = endTime;
    //@TODO conver tto standard time
    var optionId = (time.day+"-"+time.startTime+"-"+time.endTime).replace(/:/g, '-');
    var optionText = time.day+": "+time.startTime+" - "+time.endTime;
    var timeOptionFormatString = 
        "<div id=\"{0}\"class=\"selected-option\">\n" +
        "  <button onclick=\"unselectSelectedTime('{0}')\">x</button>\n" +
        "  <li class=\"filter-options\">{1}</li>\n" +
        "</div>"; 
    $("#time-options").append(timeOptionFormatString.format(optionId, optionText));
}

function unselectSelectedTime(id) {
    $("#"+id).remove();
}

// OnClick function for an option checkbox
// * If a new option is checked
//    - Populates filter window with option under its respetive type
// * If a an option is unchecked
//    - Removes option from filter window
function selectOption(element) {
    var filterType;
    // Get correct filter type (where to put selected option)
    for (var i = 0; i < filter_types.length; ++i) {
        if ($("#"+filter_types[i]+"-filter-btn")[0].value == "active") {
            filterType = $("#"+filter_types[i]+"-options");
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
    for (var i = 0; i < filter_types.length; ++i) {
        $("#"+filter_types[i]+"-options").children("div").each(function(index, value) {
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
    $("#filter-type-window").children("div").each(function (index, value) {
        var arr = [];
        // Iterate over each selected option type
        for (var i = 0; i < value.children.length; ++i) {
            arr.push(value.children[i].id); 
        }
        var name = filter_types[f++];
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

// Get the filters JSON object with correct filters to apply using getSelectedOptions
function updateFilters() {
    filtersToApply = getSelectedOptions();  
    scheduleToApply = getSelectedSchedule();
    $('.logic-checkbox').each(function (index, value) {        
        timeMWFarr = []
        timeTRarr = []
        otherArr = []
        filterType = value.id; 
        if (value.checked == true) {
            console.log(filterType + " isChecked");
            for (var t=0;t<filtersToApply[filterType].length;t++) {
                timeArr = filtersToApply[filterType][t].split("-");
                startTime = timeArr[1] + ":" + timeArr[2];
                endTime = timeArr[3] + ":" + timeArr[4];
                if (filtersToApply[filterType][t].includes('mwf') == true) { timeMWFarr.push(new Array(startTime, endTime)); }
                else if (filtersToApply[filterType][t].includes('tr') == true) { timeTRarr.push(new Array(startTime, endTime)); }
            } 
            otherArr = filtersToApply[filterType]       
            $('#'+filterType).parent('label').addClass("checked");
        } else {      
            $('#'+filterType).parent('label').removeClass("checked");
        }
        if (filterType == "time") {
            filters[filterType]['filters']['MWF'] = timeMWFarr
            filters[filterType]['filters']['TR'] = timeTRarr
        } else {
            filters[filterType]['filters'] = otherArr
        }
    }); 
}

// OnClick function for a filter logic checkbox
// - Makes the and/or radio button enabled
function updateFilterLogic() {
    selectedFilters = getSelectedFilters();
    numSelected = 0;
    // always set first selected filter to have 'and'
    if (selectedFilters.length != 0) {
        filters[selectedFilters[0]]['logic'] = "and";
    }
    // for each filter type that is checked, either disable or enable the AND/OR box accordingly
    $('.logic-checkbox').each(function (index, value) {
        if (value.checked == true && ++numSelected < selectedFilters.length) {
            // console.log("can use " + value.id);
            $("#"+value.id).parent().next().removeProp("disabled");    
        } else {
            // console.log(value.id + " is disabled");
            $("#"+value.id).parent().next().prop("disabled", true);
        }
    }); 
}

// OnClick function that adds the logic for this filter
function addLogic(element) {

}

/* *** HELPER FUNCTIONS FOR LOGIC *** */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Retrieves sections
function getFilteredSections(e) {
    updateFilters(); 
    $.ajax({
        type: "POST",
        url: "sections",
        data: JSON.stringify(filters),
        dataType: "json",
        success: function(response) {
            console.log(response.sections);
            data = response.sections;
            sectionFrame = $("#section-frame");
            sectionFrame.empty();
            var sectionFormatString =
                "<div id=\"section-{0}\" class=\"input-group\">\n" +
                "  <span class=\"input-group-addon\">\n" +
                "    <input id=\"option-checkbox\" type=\"checkbox\">\n" +
                "  </span>\n" +
                "  <p class=\"form-control\">{0}</p>\n" +
                "</div>\n";
            for (var i in data) {
                // Add to section window 
                sectionFrame.append(sectionFormatString.format(data[i].name));
                // Check if already in selected
                // $("#"+filterType).children("div").each(function(index, value) {
                //     if (value.id == data.sections[i].name) {
                //         $("#option-"+data.sections[i].name).children("span").children("input").prop("checked", true);
                //     }

                // });
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

// Updates the filters JSON object to have correct logic for filter_type
function setLogic(element) {
    selectedFilters = getSelectedFilters(); // get selected filter types
    filterType = element.id.split("-")[0]; // get the filter type of checked element (course, faculty, room or time)
    // iterate through selected filters - 1 and set the chosen logic AND/OR for next item that is selected
    for (var i=0;i<selectedFilters.length-1;i++) {
        if (selectedFilters[i] == filterType) {
            filters[selectedFilters[i+1]]['logic'] = element.options[element.selectedIndex].value;
            // console.log(element.options[element.selectedIndex].value + " chosen for " + selectedFilters[i+1]);
        }
    }
}

// gets all the currently selected filter types to be applied with logic
function getSelectedFilters() {
    var selectedFilters = [];
    $('.logic-checkbox').each(function (index, value) {
        if (value.checked == true) { selectedFilters.push(value.id); }
    });
    return selectedFilters;
}

// OnClick function to set the days for a new section
function setDays(element, form) {
    form.days=element.id;
    form.save();
}
