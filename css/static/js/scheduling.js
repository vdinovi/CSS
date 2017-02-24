// Onclick func for filter type button
//  * If a new filter-type is selected:
//     - Unchecks any previousely selected filter types
//     - Populates the option window with all opions for selected filter type
//     - Checks all options that have already been selected for this filter type
//  * A filter type may not be un-selected
//     - Only set to inactive if another is selected
function selectFilter(btn) {
    if (btn.value == "inactive") {
        btn.value = "active";
        btn.className = "noselect filter-type-active";
        if (btn.id != "course-filter-btn") {
            $("#course-filter-btn").value = "inactive"
            $("#course-filter-btn").className = "noselect filter-type"
        }
        if (btn.id != "facuty-filter-btn") {
            $("#faculty-filter-btn").value = "inactive"
            $("#faculty-filter-btn").className = "noselect filter-type"
        }
        if (btn.id != "room-filter-btn") {
            $("#room-filter-btn").value = "inactive"
            $("#room-filter-btn").className = "noselect filter-type"
        }
        if (btn.id != "time-filter-btn") {
            $("#time-filter-btn").value = "inactive"
            $("#time-filter-btn").className = "noselect filter-type"
        }
    }
    else {
        btn.value = "inactive";
        btn.className = "noselect filter-type";
    }
}

// OnClick function for new section frame
// - Toggles between new section frame and filter frame
function switchFrame(firstFrame, secondFrame) {
    $("#"+firstFrame).hide();
    $("#"+secondFrame).show();
}


// OnClick function for an option checkbox
//  - Populates section window with all sections for selected option
//  - Checks all sections in section window 
function selectItem(element) {
    //@TODO everything :( 
    return true;
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

