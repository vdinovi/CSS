/* *** GLOBALS *** */
const filter_types = ["schedule", "course", "faculty", "room", "time"];
var filters = {"schedule":{"logic":"and", "filters":[]}, "course":{"logic":"and", "filters":[]}, "faculty":{"logic":"and", "filters":[]}, "room":{"logic":"and", "filters":[]}, "time":{"logic": "and", "filters":{"MWF":[], "TR":[]}}}; //
var filteredSections = [];
var sectionDetails = [{"name":"cpe101-01", "term":"fall2016", "course":"cpe101", "type":"lecture", "faculty":"kearns", "room":"14-256", "days":"mwf", "start_time":"10:00AM", "end_time":"12:00PM"}];

/* *** UTILITY *** */
// String format function. 
// Replaces {n} in format string with n-th positional arg.
String.prototype.format = function() {
    var content = this;
    for (var i=0; i < arguments.length; i++) {
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
    var timeParse = time.split(":");
    var hour = parseInt(timeParse[0]);
    var minute = parseInt(timeParse[1]);
    var half;
    if (hour > 12) {
        if (hour == 24) {
            half = "AM"
            hour = 12
        }
        else {
            half = "PM";
            hour -= 12;
        }
    }
    else {
        half = "AM";
        if (hour == 0)
            hour = 12
    }
    if (hour < 10)
        hour = "0"+hour;
    if (minute < 10)
        minute = "0"+minute
    var stdTime = "{0}:{1} {2}";
    return stdTime.format(hour, minute, half);
}

// Convert Military formatted time to standard
function toMilitaryTime(time) {
    var timeParse = time.split(" ");
    var half = timeParse[1]
    var timeParse2 = timeParse[0].split(":");
    var milTime = "{0}:{1}";
    var hour = parseInt(timeParse2[0]);
    if (hour >= 24)
        hour = 0 
    if (half == 'PM') {
        if (hour != 12)
            hour += 12  
    }
    else {
        if (hour == 12)
            hour = 0 
    }
    return milTime.format(hour, timeParse2[1])
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
    /*$("#open-terms").children("li").each(function (index, value) {
        value.className = "";
    });*/
    $("#"+name).parent().addClass("active-schedule");
}

// Gets the currently selected term. If none, returns false
function getSelectedSchedules() {
    var arr = []
    $("#open-terms").children("li").each( function(index, value) {
        if ($(value).hasClass("active-schedule"))
            arr.push($(value).children("a").text());
    });
    for (var i = 0; i < arr.length; ++i) {
        if (arr[i] == "")
            arr.splice(i, 1);
    }
    return arr;
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
                    optionFrame.append(optionFormatString.format(data.start_time, data.end_time));
                }
                // Filter Type is course, faculty, or room
                else {
                    var optionFormatString =
                        "<div id=\"option-{0}\" class=\"input-group\">\n" +
                        "  <span class=\"input-group-addon\">\n" +
                        "    <input id=\"option-{0}-checkbox\" type=\"checkbox\" onclick=\"selectOption(this)\">\n" +
                        "  </span>\n" +
                        "  <p class=\"form-control\" style=\"max-width: 100%; white-space: nowrap\">{1}</p>\n" +
                        "</div>\n";
                    for (var i in data.options) {
                        // Add to option window 
                        var name = data.options[i].name
                        optionFrame.append(optionFormatString.format(name.replace(/ /g, '-'), name));
                        // Check if already in selected
                        $("#"+filterType).children("div").each(function(index, value) {
                            if (value.id == data.options[i].name.replace(/ /g, '-')) {
                                $("#option-"+data.options[i].name.replace(/ /g, '-')).children("span").children("input").prop("checked", true);
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
        sweetAlert("Invalid Start Time", "Department Hours: "+toStandardTime(minTime)+" - "+toStandardTime(maxTime));
        return false;
    }
    if ((compareTime(endTime, minTime) < 1) || (compareTime(endTime, maxTime) > 0)) {
        sweetAlert("Invalid End Time", "Department Hours: "+toStandardTime(minTime)+" - "+toStandardTime(maxTime));
        return false;
    }
    if (compareTime(startTime, endTime) >= 0) {
        sweetAlert("Start time must come before end time");
        return false; 
    }
    time.startTime = startTime;
    time.endTime = endTime;
    var optionId = (time.day+"-"+time.startTime+"-"+time.endTime).replace(/[: ]/g, '-');
    var optionText = time.day+": "+toStandardTime(time.startTime)+" - "+toStandardTime(time.endTime);
    var timeOptionFormatString = 
        "<div id=\"{0}\"class=\"selected-option\">\n" +
        "  <button onclick=\"unselectSelectedTime('{0}')\">x</button>\n" +
        "  <li class=\"filter-options\">{1}</li>\n" +
        "</div>"; 
    $("#time-options").append(timeOptionFormatString.format(optionId, optionText));
    $("#"+optionId).data("data", time);
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
    if (filterType = "#time-options")
        return;
    if (element.checked) {
        var optionFormatString = 
                    "<div id=\"{0}\"class=\"selected-option\">\n" +
                    "  <button onclick=\"unselectSelectedOption('{0}')\">x</button>\n" +
                    "  <li class=\"filter-options\">{1}</li>\n" +
                    "</div>"; 
        var text = element.parentNode.parentNode.innerText;
        var optionAlreadySelected = false;
        filterType.children("div").each( function(index, value) {
            if ($(value).prop('id').replace(/-/g, ' ') == text)
                optionAlreadySelected = true;
        });
        if (!optionAlreadySelected) {
            // Add to option list
            filterType.append(optionFormatString.format(text.replace(/ /g, '-'), text));
            // Set data field
            $("#"+text.replace(/ /g, '-')).data("data", text);
        }
    }
    // Remove option from selected option list
    else {
        filterType.children("div").each(function(index, value) {
            if (value.id.replace(/-/g, ' ') == element.parentNode.parentNode.innerText)
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
        if (name.replace(/-/g, ' ') == $(value).children("p").text()) {
            $(value).children("span").children("input").prop("checked", false);
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
    selectedOptions["schedule"] = getSelectedSchedules(); 
    $("#filter-type-window").children("div").each(function (index, value) {
        var arr = [];
        $(value).children("div").each( function (i, v) {
            arr.push($(v).data("data"));
        });
        var name = filter_types[f++];
        selectedOptions[name] = arr;
    });
    return selectedOptions;
}

// Selects all sections in filtered Section window
function selectAllOptions() {
    $("#option-frame").children("div").each(function(index, value) { 
        if ($("#"+value.id+"-checkbox").prop("checked") == false) {
            $("#"+value.id+"-checkbox").prop("checked", true);
            selectOption($("#"+value.id+"-checkbox")[0]);
        }
    });
}

// Unselects all sections in filtered Section window
function unselectAllOptions() {
    $("#option-frame").children("div").each(function(index, value) { 
        if ($("#"+value.id+"-checkbox").prop("checked") == true) {
            $("#"+value.id+"-checkbox").prop("checked", false);
            selectOption($("#"+value.id+"-checkbox")[0]);
        }
    });
}

/* *** FILTER LOGIC / SECTIONS *** */

// returns strings with underscores as spaces
function underscoreToSpaces(string) {
    return string.split("_").join(" ");
}

// returns strings with spaces as underscores
function spacesToUnderscores(string) {
    return string.split(" ").join("_");
}


// Get the filters JSON object with correct filters to apply using getSelectedOptions
function updateFilters() {
    filtersToApply = getSelectedOptions();  
    $('.logic-checkbox').each(function (index, value) {        
        timeMWFarr = []
        timeTRarr = []
        otherArr = []
        filterType = value.id; 
        console.log(filterType);
        if (value.checked) {
            for (var t=0;t<filtersToApply[filterType].length;t++) {
                timeArr = filtersToApply[filterType][t].split("-");
                startTime = timeArr[1] + ":" + timeArr[2];
                endTime = timeArr[3] + ":" + timeArr[4];
                if (filtersToApply[filterType][t].includes('mwf')) { timeMWFarr.push(new Array(startTime, endTime)); }
                else if (filtersToApply[filterType][t].includes('tr')) { timeTRarr.push(new Array(startTime, endTime)); }
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
    console.log(filters);
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
        if (value.checked && ++numSelected < selectedFilters.length) {
            $("#"+value.id).parent().next().removeProp("disabled");    
        } else {
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
function getFilteredSections() {
    updateFilters(); 
    $.ajax({
        type: "POST",
        url: "sections",
        data: JSON.stringify(filters),
        dataType: "json",
        success: function(response) {
            data = response.sections;
            //filteredSections.push(response.sections);
            sectionFrame = $("#section-frame");
            sectionFrame.empty();
            var sectionFormatString =
                "<div id=\"section-{0}\" class=\"input-group\">\n" +
                "  <span class=\"input-group-addon\">\n" +
                "    <input id=\"section-{0}-checkbox\" type=\"checkbox\">\n" +
                "  </span>\n" +
                "  <p class=\"form-control\">{1}</p>\n" +
                "</div>\n";
            for (var i in data) {
                if ($.inArray(data[i], filteredSections) == -1) {
                    filteredSections.push(data[i]);
                }
                // Add to section window 
                sectionFrame.append(sectionFormatString.format(data[i].name, underscoreToSpaces(data[i].name)));
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

// Helper function that returns -1 if value by [name] is not found in array, else index of value
function inArrayByName(name, array) {
    for (var i=0;i<array.length;i++) {
        if (array[i].name.includes(name)) {
            return i;
        }
    }
    return -1;
}

// returns true if a section not already in Section Details has been selected (and needs to be added to Section Details)
function getSelectedSections() {
    newSectionSelected = false;
    $("#section-frame").children("div").each(function(index, value) { 
        console.log(value.id);
        if ($("#"+value.id+"-checkbox").prop('checked')) { 
            console.log("HELLO");
            if (inArrayByName(value.id.split("section-")[1], sectionDetails) === -1) {
                console.log("pushing...");
                console.log(filteredSections[inArrayByName(value.id.split("section-")[1], filteredSections)]);
                sectionDetails.push(filteredSections[inArrayByName(value.id.split("section-")[1], filteredSections)]);
                newSectionSelected = true;
            }
        }
    });
    return newSectionSelected;
}

// Selects all sections in filtered Section window
function selectAllSections() {
    $("#section-frame").children("div").each(function(index, value) { 
        $("#"+value.id+"-checkbox").prop("checked", true);
    });
}

// Unselects all sections in filtered Section window
function unselectAllSections() {
    $("#section-frame").children("div").each(function(index, value) { 
        $("#"+value.id+"-checkbox").prop("checked", false);
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
        }
    }
}

// gets all the currently selected filter types to be applied with logic
function getSelectedFilters() {
    var selectedFilters = [];
    $('.logic-checkbox').each(function (index, value) {
        if (value.checked) { selectedFilters.push(value.id); }
    });
    return selectedFilters;
}

function NewSection(request) {
    var sectionData = {};
    console.log($("#section_num").val());
    sectionData = {
         'section_num': $("#section_num").val(), 
         'schedule': $("#academic-term").val(), 
         'course': $("#course").val(),
         'section-type': $("#section-type").val(),
         'faculty': $("#faculty").val(),
         'room': $("#room").val(),
         'days': $("#days").val(),
         'capacity': $("#capacity").val(),
         'start-time': $("#start-time").val(),
         'end-time': $("#end-time").val()
        };
    console.log(sectionData);
    $.ajax({
        type: "POST",
        url: "newSection",
        data: JSON.stringify(sectionData),
        dataType: 'json',
        success: function(response) {
            console.log(sectionData)
            // Clear all elements
            $("#new-section-frame").find("select").each(function (index, value) {
                $($(value).children('option')[0]).prop('selected', true);
            })
            $("#new-section-frame").find("input").each(function (index, value) {
                ($(value).val(''));
            })
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/* Section Details Functions */

function updateSectionDetails(resort) {
    var sectionDetailsFormatString = 
        "<tr id=\"{0}-detail\">\n" + 
            "<td>\n" +
                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#deselect-section\" onclick=\"removeSectionFromDetails(this)\"><span class=\"glyphicon glyphicon-minus\" title=\"Remove section from details\"></span>&nbsp;</button>\n" +
                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#edit-section-modal\"><span class=\"glyphicon glyphicon-edit\" title=\"Edit section\"></span>&nbsp;</button>\n" +
                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#delete-section-modal\" onclick=\"confirmDeleteModal(this)\"><span class=\"glyphicon glyphicon-trash\" title=\"Delete section\"></span>&nbsp;</button>\n" +
            "</td>\n" +
            "<td>{1}</td>\n" + 
            "<td>{2}</td>\n" + 
            "<td>{3}</td>\n" + 
            "<td>{4}</td>\n" + 
            "<td>{5}</td>\n" + 
            "<td>{6}</td>\n" + 
            "<td>{7}</td>\n" + 
            "<td>{8}</td>\n" + 
            "<td>{9}</td>\n" + 
        "</tr>\n";
    var detailFrame = $("#section-detail-rows");
    if (getSelectedSections() || resort) {
        detailFrame.empty();
        for (var i in sectionDetails) {  
            detailFrame.append(sectionDetailsFormatString.format(sectionDetails[i].name, underscoreToSpaces(sectionDetails[i].name), sectionDetails[i].term, sectionDetails[i].course, sectionDetails[i].type, sectionDetails[i].faculty, sectionDetails[i].room, sectionDetails[i].days, sectionDetails[i].start_time, 
            sectionDetails[i].end_time));
        }
    }
}

function confirmDeleteModal(sectionElement) {
    sectionName = spacesToUnderscores($($(sectionElement).parent().next("td")).text());
    sectionIndex = inArrayByName(sectionName, sectionDetails);
    section = sectionDetails[sectionIndex];
    formatStr = "<h4\>{0}\</h4>\n" +
                "<ul>\n" +
                "<li>{1} {2}</li>\n" +
                "<li>{3} {4}</li>\n" +
                "<li>{5} {6} - {7}</li>\n" +
                "</ul>\n";
    console.log(section);
    frame = $("#delete-section-check");
    frame.empty();
    frame.append(formatStr.format(underscoreToSpaces(section.name), section.term, section.faculty, section.type, section.room, section.days, section.start_time, section.end_time));
}


function removeDeletedSection(sectionName) {
    $("#"+sectionName+"-detail").remove();
    // $("#delete-section-modal .close").click();
    $("#delete-section-modal").modal('hide');
}

function deleteSection(element) {
    sectionName = $($("#delete-section-check").children('h4')[0]).text();
    console.log("HERE" + sectionName);
    $.ajax({
        type: "POST",
        url: "delete-section",
        dataType: 'json',
        data: JSON.stringify({"section": sectionName}),
        success: function(response) {
            removeDeletedSection(spacesToUnderscores(sectionName));
        },
        error: function(err) {
            console.log(err);
        }
    });
}



// removes the section row from Section Details (does not delete)
function removeSectionFromDetails(element) {
    // remove element from sectionDetails
    index = inArrayByName($(element).parent().next("td").text(), sectionDetails);
    if (index !== -1) { sectionDetails.splice(index, 1); }
    // gets to <tr> parent element
    $(element).parent().parent().remove();
}

// sort by given attribute in Section Details 
function sortSectionDetailsBy(element, attribute) {
    sectionDetails.sort(function(a,b) { return a[attribute].localeCompare(b[attribute]); });
    updateSectionDetails(true);
    $(element).parent().children("th").each(function(index,value) {
        $(value).toggleClass("sorted", false);
    });
    $(element).toggleClass("sorted");
}

// OnClick function to set the days for a new section
function setDays(element, form) {
    form.days=element.id;
    form.save();
}







