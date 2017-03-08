/* *** GLOBALS *** */
const filter_types = ["course", "faculty", "room", "time"];
var filters = {"schedule":{"logic":"and", "filters":[]}, "course":{"logic":"and", "filters":[]}, "faculty":{"logic":"and", "filters":[]}, "room":{"logic":"and", "filters":[]}, "time":{"logic": "and", "filters":{"MWF":[], "TR":[]}}}; //
var filteredSections = [];
var sectionDetails = [];

/* *** UTILITY *** */
// String format function. 
// Replaces all '{n}' in format string with n-th positional arg.
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
            var scheduleFormatString = "<button class=\"list-group-item\" onclick=\"addSchedule('{0}')\" data-dismiss=\"modal\">{0}</button>\n";
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
    //$("#"+name).parent().className("dropdown active-schedule");
    $("#"+name).addClass("active-schedule");
}

// Gets the currently selected term. If none, returns false
function getSelectedSchedules() {
    var arr = []
    $("#open-terms").children("li").each( function(index, value) {
        if ($(value).children("a").hasClass("active-schedule"))
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
                        "      <button id=\"time-window-mwf-btn\" type=\"button\" class=\"btn btn-primary\" value=\"active\" onclick=\"selectDay('mwf')\" style=\"display:inline-block;\">MWF</button>\n" +
                        "      <button id=\"time-window-th-btn\" type=\"button\" class=\"btn btn-default\" value=\"inactive\" onclick=\"selectDay('th')\" style=\"display:inline-block;\">TH</button>\n" +
                        "    </div>\n" +
                        "    <div class=\"col-xs-12\" style=\"margin-top:30px;\">\n" +
                        "      <label for=\"time-window-start-time\">Start Time:</label>\n" +
                        "      <input id=\"time-window-start-time\" type=\"time\" name=\"start-time\"></input>\n" +
                        "    </div>\n" +
                        "    <div class=\"col-xs-12\" style=\"margin-top:30px;\">\n" +
                        "      <label for=\"time-window-end-time\">End Time:</label>\n" +
                        "      <input id=\"time-window-end-time\" type=\"time\" name=\"end-time\"></input>\n" +
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
                        "<div id=\"option-{0}\" class=\"input-group\" style=\"height:auto\">\n" +
                        "  <span class=\"input-group-addon\">\n" +
                        "    <input id=\"option-{0}-checkbox\" type=\"checkbox\" onclick=\"selectOption(this)\">\n" +
                        "  </span>\n" +
                        "  <div class=\"form-control\" style=\"max-width:100%; height:100%;\">\n" +
                        "    <p style=\"height: 100%;\">{1}</p>\n" +
                        "  </div>\n" +
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
    if ($("#time-window-mwf-btn")[0].value == "active")
        time.day = "mwf";
    else
        time.day = "th";
    var startTime = $("#time-window-start-time").val();
    var endTime = $("#time-window-end-time").val();
    if ((compareTime(startTime, minTime)) < 0 || (compareTime(maxTime, startTime) < 0)) {
        sweetAlert("Invalid Start Time", "Department Hours: "+toStandardTime(minTime)+" - "+toStandardTime(maxTime));
        return false;
    }
    if ((compareTime(endTime, minTime) < 0) || (compareTime(maxTime, endTime) < 0)) {
        sweetAlert("Invalid End Time", "Department Hours: "+toStandardTime(minTime)+" - "+toStandardTime(maxTime));
        return false;
    }
    if (compareTime(startTime, endTime) > 0) {
        sweetAlert("Start time must come before end time");
        return false; 
    }
    time.startTime = startTime;
    time.endTime = endTime;
    var optionId = (time.day+"-"+time.startTime+"-"+time.endTime).replace(/[: ]/g, '-');
    var optionText = time.day.toUpperCase()+":<br> "+toStandardTime(time.startTime)+" - "+toStandardTime(time.endTime);
    var timeOptionFormatString = 
        "<div id=\"{0}\"class=\"selected-option\" style=\"overflow:hidden;height:100%; min-height: 20px;\">\n" +
        "  <button onclick=\"unselectSelectedTime('{0}')\" style=\"float:left;padding-bottom:100%; margin-bottom:-100%;\">x</button>\n" +
        "  <li class=\"filter-options\" style=\"display:flex;height:100%;min-height: 25px;\">{1}</li>\n" +
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
    if (filterType.prop('id') != "time-options" && element.checked) {
        var optionFormatString = 
                    "<div id=\"{0}\"class=\"selected-option\" style=\"overflow:hidden;height:100%; min-height: 20px;\">\n" +
                    "  <button onclick=\"unselectSelectedOption('{0}')\" style=\"float:left;padding-bottom:100%;margin-bottom:-100%;\">x</button>\n" +
                    "  <li class=\"filter-options\" style=\"height:100%;min-height: 25px;\">{1}</li>\n" +
                    "</div>"; 
        var text = $(element).parents("div").children("div").children("p").text();
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
            if ($(value).children("li").text() == $(element).parent().parent().children('div').children("p").text())
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
        if (name.replace(/-/g, ' ') == $(value).children("div").children('p').text()) {
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
        if ($(value).children("span").children("input").prop('checked') == true) {
            checkbox = $(value).children("span").children("input");
            checkbox.prop('checked', false);
            selectOption(checkbox);
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
    filters['schedule']['filters'] = filtersToApply['schedule'];
    $('.logic-checkbox').each(function (index, value) {        
        timeMWFarr = []
        timeTRarr = []
        otherArr = []
        filterType = value.id.split("-logic-checkbox")[0]; 
        if (value.checked) {
            for (var t=0;t<filtersToApply[filterType].length;t++) {
                timeArr = filtersToApply[filterType][t].split("-");
                startTime = timeArr[1] + ":" + timeArr[2];
                endTime = timeArr[3] + ":" + timeArr[4];
                if (filtersToApply[filterType][t].includes('mwf')) { timeMWFarr.push(new Array(startTime, endTime)); }
                else if (filtersToApply[filterType][t].includes('tr')) { timeTRarr.push(new Array(startTime, endTime)); }
            } 
            otherArr = filtersToApply[filterType]       
            $('#'+value.id).parent('label').addClass("checked");
        } else {      
            $('#'+value.id).parent('label').removeClass("checked");
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

/* *** HELPER FUNCTIONS FOR LOGIC *** */
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
        if ($("#"+value.id+"-checkbox").prop('checked')) { 
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
        if (value.checked) { selectedFilters.push(value.id.split("-logic-checkbox")[0]); }
    });
    return selectedFilters;
}

function newSection(sectionData) {
    sectionData = {
             'section-num': $("#section-num").val(), 
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

/* Confirming new section */
function sectionConflictCheck(element) {
    var sectionData = {};
    if (element.id.includes("create")) {
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
    }
    else {
        sectionData = {
         'schedule': $("#edit-term").children("p").text(),
         'name': $("#edit-course").children("p").text() + "-" + $("#edit-section_num").val(),
         'section_num': $("#edit-section_num").val(),
         'type': $("#edit-type").val(),
         'faculty': $("#edit-faculty").val(),
         'room': $("#edit-room").val(),
         'days': $("#edit-days").val(),
         'capacity': $("#edit-capacity").val(),
         'start-time': $("#edit-start_time").val(),
         'end-time': $("#edit-end_time").val(),
         'students_enrolled': $("#edit-students_enrolled").val(),
         'students_waitlisted': $("#edit-students_waitlisted").val()
        };
    }
    console.log(sectionData);
    $.ajax({
        type: "POST",
        url: "conflict-check",
        data: JSON.stringify(sectionData),
        dataType: 'json',
        success: function(response) {
            room_conflicts = response.room;
            console.log(room_conflicts);
            faculty_conflicts = response.faculty;
            console.log(faculty_conflicts);
            if (!(room_conflicts.length) && !(faculty_conflicts.length)) {
                if (element.id.includes("create")) {
                    newSection();
                }
                else {
                    editSection();
                }
            }
            else {
                if (element.id.includes("create")) {
                    $('#confirm-create-conflicts-modal').show();
                    $('#confirm-create-conflicts-modal').toggleClass("in");
                    frame = $("#confirm-create-section-check");
                }
                else {
                    $('#confirm-edit-conflicts-modal').show();
                    $('#confirm-edit-conflicts-modal').toggleClass("in");
                    frame = $("#confirm-edit-section-check");
                }
                

                var roomFormatStr1 = "<div class=\"col-xs-6\" style=\"text-align:center;\"\>\n" +
                             "<h4>Room Conflicts</h4>\n" +
                             "<ul>\n";
                var roomFormatStr2 = "";
                if (room_conflicts.length == 0) {
                    roomFormatStr2 = "None";
                }
                else {
                    for (i = 0; i < room_conflicts.length; i++)
                        roomFormatStr2 += "<li> {0} </li>\n".format(underscoreToSpaces(room_conflicts[i].name));
                }
                var roomFormatStr3 = "</ul>\n</div>\n";
                var roomFormatStr = roomFormatStr1 + roomFormatStr2 + roomFormatStr3;

                var facultyFormatStr1 = "<div class=\"col-xs-6 col-xs-offset-6\" style=\"text-align:center;\"\>\n" +
                                        "<h4>Faculty Conflicts</h4>\n" +
                                        "<ul>\n";
                var facultyFormatStr2 = "";
                if (faculty_conflicts.length == 0) {
                    facultyFormatStr2 = "None";
                }
                else {
                    for (i = 0; i < faculty_conflicts.length; i++)
                        facultyFormatStr2 += "<li> {0} </li>\n".format(underscoreToSpaces(faculty_conflicts[i].name));
                }
                var facultyFormatStr3 = "</ul>\n</div>\n";
                var facultyFormatStr = facultyFormatStr1 + facultyFormatStr2 + facultyFormatStr3;

                frame.empty()
                frame.append(roomFormatStr + facultyFormatStr);
                                   
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function updateSectionDetailConflicts() {
    $.ajax({
        type: "POST",
        url: "section-detail-conflicts",
        data: JSON.stringify({'section_details': sectionDetails}),
        dataType: 'json',
        success: function(response) {
            console.log(sectionDetails.length);
            for (var key in sectionDetails) {
                console.log('in for loop');
                // Gets conflicts for one section
                var conflicts = response[sectionDetails[key].name];

                // Save room conflicts for section
                var room_conflicts = []
                for (var room in conflicts['room']) {
                    room_conflicts.push(conflicts['room'][room].name)
                    console.log(room_conflicts)
                }

                // Save faculty conflicts for section
                var faculty_conflicts = []
                for (var faculty in conflicts['faculty']) {
                    faculty_conflicts.push(conflicts['faculty'][faculty].name)
                    console.log(faculty_conflicts)
                }

                var sectionDetailEntry = $("#{0}-detail".format(sectionDetails[key].name))

                if (room_conflicts.length || faculty_conflicts.length) {
                    var conflictSectionFormatString = 
                            "<td>\n" +
                                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#deselect-section\" onclick=\"removeSectionFromDetails(this)\"><span class=\"glyphicon glyphicon-minus\" title=\"Remove section from details\"></span>&nbsp;</button>\n" +
                                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#edit-section-modal\" onclick=\"displaySectionInfo(this)\"><span class=\"glyphicon glyphicon-edit\" title=\"Edit section\"></span>&nbsp;</button>\n" +
                                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#delete-section-modal\" onclick=\"confirmDeleteModal(this)\"><span class=\"glyphicon glyphicon-trash\" title=\"Delete section\"></span>&nbsp;</button>\n" +
                            "</td>\n" +
                            "<td>{1}</td>\n" + 
                            "<td>{2}</td>\n" + 
                            "<td>{3}</td>\n" + 
                            "<td>{4}</td>\n" + 
                            "<td {5}>{6}</td>\n" + 
                            "<td {7}>{8}</td>\n" + 
                            "<td>{9}</td>\n" + 
                            "<td>{10}</td>\n" + 
                            "<td>{11}</td>\n";
                    sectionDetailEntry.empty();

                    var faculty_string = ""
                    var room_string = ""
                    if (faculty_conflicts.length) {
                        console.log("FACULTY CONFLICT FOUND")
                        faculty_string = 'class=\"alert-danger\" data-toggle=\"popover\" data-trigger=\"hover\" title=\"Conflicting Sections\" data-content=\"BLAH\"'
                    }
                    if (room_conflicts.length) {
                        console.log("ROOM CONFLICT FOUND")
                        room_string = 'class=\"alert-danger\" data-toggle=\"popover\" data-trigger=\"hover\" title=\"Conflicting Sections\" data-content=\"BLAH\"'
                    }

                    console.log(conflictSectionFormatString.format(sectionDetails[key].name, underscoreToSpaces(sectionDetails[key].name), sectionDetails[key].term, sectionDetails[key].course, sectionDetails[key].type, 
                        faculty_string, 
                        sectionDetails[key].faculty, room_string, sectionDetails[key].room, sectionDetails[key].days, sectionDetails[key].start_time, 
                        sectionDetails[key].end_time));
                    sectionDetailEntry.prepend(conflictSectionFormatString.format(sectionDetails[key].name, underscoreToSpaces(sectionDetails[key].name), sectionDetails[key].term, sectionDetails[key].course, sectionDetails[key].type, 
                        faculty_string, sectionDetails[key].faculty, room_string, sectionDetails[key].room, sectionDetails[key].days, sectionDetails[key].start_time, 
                        sectionDetails[key].end_time));
                    // if (room_conflicts.length) {
                    //     console.log("ROOM CONFLICT FOUND");
                    //     console.log(conflictSectionFormatString.format(sectionDetails[key].name, underscoreToSpaces(sectionDetails[key].name), sectionDetails[key].term, sectionDetails[key].course, sectionDetails[key].type, 
                    //         "", sectionDetails[key].faculty, 'class=\"alert-danger\" data-toggle=\"popover\" data-trigger=\"hover\" title=\"Conflicting Sections\" data-content=\"BLAH\"', sectionDetails[key].room, sectionDetails[key].days, sectionDetails[key].start_time, 
                    //         sectionDetails[key].end_time));
                    //     sectionDetailEntry.append(conflictSectionFormatString.format(sectionDetails[key].name, underscoreToSpaces(sectionDetails[key].name), sectionDetails[key].term, sectionDetails[key].course, sectionDetails[key].type, 
                    //         "", sectionDetails[key].faculty, 'class=\"alert-danger\" data-toggle=\"popover\" data-trigger=\"hover\" title=\"Conflicting Sections\" data-content=\"BLAH\"', sectionDetails[key].room, sectionDetails[key].days, sectionDetails[key].start_time, 
                    //         sectionDetails[key].end_time));
                    // }
                }
            }
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
                "<button type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#edit-section-modal\" onclick=\"displaySectionInfo(this)\"><span class=\"glyphicon glyphicon-edit\" title=\"Edit section\"></span>&nbsp;</button>\n" +
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
            detailFrame.prepend(sectionDetailsFormatString.format(sectionDetails[i].name, underscoreToSpaces(sectionDetails[i].name), sectionDetails[i].term, sectionDetails[i].course, sectionDetails[i].type, sectionDetails[i].faculty, sectionDetails[i].room, sectionDetails[i].days, toStandardTime(sectionDetails[i].start_time), 
            toStandardTime(sectionDetails[i].end_time)));
        }
    }

    updateSectionDetailConflicts();
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
    $("#delete-section-modal").children(".close").click();
}

function deleteSection(element) {
    sectionName = $($("#delete-section-check").children('h4')[0]).text();
    console.log("HERE" + sectionName);
    $.ajax({
        type: "POST",
        url: "deleteSection",
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

function daysAreEqual(sectionOption, sectionAttr) {
    // console.log(sectionOption);
    // console.log(sectionAttr);
    return ((sectionOption == "Mon/Wed/Fri" && sectionAttr == "MWF") || (sectionOption == "Tue/Thu" && sectionAttr == "TR"));
}

function displaySectionInfo(sectionElement) {
    sectionName = $(sectionElement).parent().parent().attr('id').split("-detail")[0];
    $.ajax({
        type: "POST",
        url: "get-section-info",
        dataType: "json",
        data: JSON.stringify({"section": sectionName}),
        success: function(response) {
            console.log("SUCCESS");
            sectionInfo = response.info;
            sectionOptions = response.options;
            parStr = "<p>{0}</p>";

            optionFormatString = "<option value=\"{0}\">{1}</option>"
            selectedOptionFormatString = "<option selected value=\"{0}\">{1}</option>"

            for (var attribute in sectionInfo) {
                element = $("#edit-"+attribute);
                if (element.is("div")) {
                    element.empty();
                    element.append(parStr.format(sectionInfo[attribute]));
                } else if (element.is("select")) {
                    if (attribute == "days") {
                        $("#edit-days").children("option").each(function(index, value) {
                            if ((sectionInfo['days'] == $(value).val())) {
                                $(value).prop("selected", true);
                            }
                        });
                    } else {
                        for (var i=0;i<sectionOptions[attribute].length;i++) {
                            if (sectionOptions[attribute][i] == sectionInfo[attribute]) {
                                $("select#edit-"+attribute).append(selectedOptionFormatString.format(spacesToUnderscores(sectionOptions[attribute][i]),sectionOptions[attribute][i]));
                            } else {
                                $("select#edit-"+attribute).append(optionFormatString.format(spacesToUnderscores(sectionOptions[attribute][i]),sectionOptions[attribute][i]));
                            }
                        }
                    }
                } else if (element.is("input")) {
                    if (attribute.includes("time")) {
                        element.val(sectionInfo[attribute].split(" ")[0]);
                    } else {
                        element.val(sectionInfo[attribute]);
                    }
                }
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function editSection(sectionData) {
    sectionData = {
         'schedule': $("#edit-term").children("p").text(),
         'name': $("#edit-course").children("p").text() + "-" + $("#edit-section_num").val(),
         'section-num': $("#edit-section_num").val(),
         'type': $("#edit-type").val(),
         'faculty': $("#edit-faculty").val(),
         'room': $("#edit-room").val(),
         'days': $("#edit-days").val(),
         'capacity': $("#edit-capacity").val(),
         'start-time': $("#edit-start_time").val(),
         'end-time': $("#edit-end_time").val(),
         'students_enrolled': $("#edit-students_enrolled").val(),
         'students_waitlisted': $("#edit-students_waitlisted").val()
        };
    console.log(sectionData);
    $.ajax({
        type: "POST",
        url: "edit-section",
        data: JSON.stringify(sectionData),
        dataType: 'json',
        success: function(response) {
            console.log("Successful update!");
        },
        error: function(err) {
            console.log(err);
        }
    });
}

/*** EDIT SECTION INFO FUNCTIONS  ***/
function renderSectionNumber() {

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

function selectDataTab(name) {
    $("#data-tab-window").children().each( function(index, value) {
        if ($(value).prop('id') != name+'-tab' && $(value).hasClass('active')) {
            $(value).removeClass('active');
        }
    });
    $("#"+name+'-tab').addClass('active');
    $("#data-window").children().each( function(index, value) {
        $(value).hide();
    });
    $("#"+name).show() 
}

function openDataTab(name, title, data) {
    var tabAlreadyOpened = false;
    $("#data-tab-window").children().each( function(index, value) {
        if ($(value).prop('id') == name+"-tab")
            tabAlreadyOpened = true;
    });
    if (!tabAlreadyOpened) {
        var tabFormat = "<li id=\"{0}-tab\" onclick=\"selectDataTab('{0}')\"><a href=\"#\">{1}</a></li>";
        $("#data-tab-window").append(tabFormat.format(name, title));
    }
    $("#data-window").children().each( function(index, value) {
        if ($(value).prop('id') == name)  {
            $(value).remove();
        }
    });
    $("#data-window").append(data)
}

// Section Creation - Data window interaction
// On term selection
$("#academic-term").on('change', function() {
    var dataFormat = 
        "<div id=\"student-plan\" class=\"container\">\n" +
        "<h3>Student Plan Data</h3>\n" + 
        "<table class=\"table\">\n" +
        "  <thead>\n" +
        "    <tr>\n" +
        "      <th>Schedule</th>\n" +
        "      <th>Course</th>\n" +
        "      <th>Section Type</th>\n" +
        "      <th>Seat Demand</th>\n" +
        "      <th>Sections Offered</th>\n" +
        "      <th>Enrollment Capacity</th>\n" +
        "      <th>Unmet Seat Demand</th>\n" +
        "    </tr>\n" +
        "  </thead>\n" +
        "  <tbody>\n" +
        "    <tr>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "      <td>{0}</td>\n" +
        "    </tr>\n" +
        "  </tbody>\n" +
        "</table>\n" +
        "</div>";
    // Get Student Plan Data
    $.ajax({
        type: "GET",
        url: "student-plan-data",
        contentType: "application/json",
        dataType: "json",
        data: {
            'schedule': $("#academic-term").val()
        },
        success: function(response) {
            $("#data-window").empty();
            $("#data-tab-window").empty();
            openDataTab('student-plan', 'Student Plan Data', dataFormat.format('temp'));
            selectDataTab('student-plan');
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Format cohort data
function formatCohortData(courseName, cohortData, cohortTotal) {
    var grades = ['freshman', 'sophomore', 'junior', 'senior'];
    var cohortDataFormat = 
        "<div id=\"cohort-data\" class=\"container\">\n" +
        "<h3>Cohort Data</h3>\n" +
        "<table class=\"table\">\n" +
        "  <thead>\n" +
        "    <tr>\n" +
        "      <th>"+courseName+"</th>" + // Course Name
        "    </tr>\n" +
        "    <tr>\n" +
        "      <th></th>\n";
    // Paste in majors
    for (var k in cohortData) {
        cohortDataFormat += 
        "      <th>"+k+"</th>\n";
    }
        "    </tr>\n" +
        "  </thead>\n" +
        "  <tbody>\n";
    // Paste in data
    for (var i = 0; i < 3; ++i) {
        cohortDataFormat +=
        "    <tr>\n" +
        "      <td>"+grades[i]+"</td>\n";
        for (var k in cohortData) {
        cohortDataFormat += 
        "      <td>"+cohortData[k][i]+"</td>\n";
        }
        cohortDataFormat +=
        "    </tr>\n";
    }
    cohortDataFormat +=
        "    <tr>\n" +
        "      <td>Cohort Total</td>\n" +
        "    </tr>\n";
    // @TODO Add cohort total
    /*for (var i = 0; i < 3; ++i) {
        cohortDataFormat +=
        "    <tr>\n" +
        "    <td>"+grades[i]+"</td>\n";
        for (var k in cohortData) {
        cohortDataFormat += 
        "      <td>"+cohortTotal[k][i]+"</td>\n";
        }
        cohortDataFormat +=
        "    </tr>\n";
    }*/
        "  </tbody>\n" +
        "</table>\n" +
        "</div>";
    return cohortDataFormat;
}

$("#course").on('change', function() {
    // Get Cohort, Course, and Enrollment Data
    var courseDataFormat =
        "<div id=\"course-info\" class=\"container\">\n" +
        "<h3>Course Info</h3>\n" +  
        "<table class=\"table\">\n" +
        "  <thead>\n" +
        "    <tr>\n" +
        "      <th>{0}</th>" + // Course Name
        "    </tr>\n" +
        "    <tr>\n" +
        "      <th>Description</th>\n" +
        "      <th>Equipement Required</th>\n" +
        "    </tr>\n" +
        "  </thead>\n" +
        "  <tbody>\n" +
        "    <tr>\n" +
        "      <td>{1}</td>\n" +
        "      <td>{2}</td>\n" +
        "    </tr>\n" +
        "  </tbody>\n" +
        "</table>\n" +
        "</div>";
    var enrollmentDataFormat = 
        "<div id=\"enrollment-data\" class=\"container\">\n" +
        "<h3>Historic Enrollment Data</h3>\n" +   
        "<table class=\"table\">\n" +
        "  <thead>\n" +
        "    <tr>\n" +
        "      <th>{0}</th>" + // Course Name
        "    </tr>\n" +
        "  </thead>\n" +
        "  <tbody>\n" +
        "    <tr>\n" +
        "      <td>NOT YET IMPLEMENTED</td>\n" +
        "    </tr>\n" +
        "  </tbody>\n" +
        "</table>\n" +
        "</div>";
    $.ajax({
        type: "GET",
        url: "course-info",
        contentType: "application/json",
        dataType: "json",
        data: {
            'schedule': $("#academic-term").val(),
            'course': $("#course").val()
        },
        success: function(response) {
            $("#data-window").children().each( function(index, value) {
                $(value).hide();
            });
            var course = response.course
            var cohortData = response.cohort_data
            var cohortTotal = response.cohort_total
            openDataTab('cohort-data', 'Cohort Data', formatCohortData(course.name, cohortData, cohortTotal));
            openDataTab('enrollment-data', 'Historic Enrollment Data', enrollmentDataFormat.format(course.name));
            openDataTab('course-info', 'Course Info', courseDataFormat.format(course.name,
                                                                              course.equipment_req,
                                                                              course.description)
            );
            selectDataTab('course-info');
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$("#faculty").on('change', function() {
    //@TODO Render faculty availability and course preferences
});

$("#room").on('change', function() {
    var roomDataFormat =
        "<div id=\"room-info\" class=\"container\">\n" +
        "<h3>Room Info</h3>\n" +   
        "<table class=\"table\">\n" +
        "  <thead>\n" +
        "    <tr>\n" +
        "      <th>{0}</th>" + // Room Name
        "    </tr>\n" +
        "    <tr>\n" +
        "      <th>Description</th>\n" +
        "      <th>Equipement</th>\n" +
        "      <th>Capacity</th>\n" +
        "      <th>notes</th>\n" +
        "    </tr>\n" +
        "  </thead>\n" +
        "  <tbody>\n" +
        "    <tr>\n" +
        "      <td>{1}</td>\n" +
        "      <td>{2}</td>\n" +
        "      <td>{3}</td>\n" +
        "      <td>{4}</td>\n" +
        "    </tr>\n" +
        "  </tbody>\n" +
        "</table>\n" +
        "</div>\n";
    $.ajax({
        type: "GET",
        url: "room-info",
        contentType: "application/json",
        dataType: "json",
        data: {
            'room': $("#room").val()
        },   
        success: function(response) {
            room = response.room
            openDataTab('room-info', 'Room Info', 
                        roomDataFormat.format(room.name, room.description, room.equipment,
                                              room.capacity, room.notes
                        )
            );
            selectDataTab('room-info');
        },
        error: function(error) {
            console.log(error);
        } 
    });
});









