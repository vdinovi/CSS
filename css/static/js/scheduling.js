
// OnClick function for a filter checkbox
//  - Unchecks any already checked filters and remove associated options from option window
//  - Populates the option window with all options for selected filter (involved ajax request)
function selectFilter(element) {
    if (element.checked) {
        // Deselect all other filters - Only one may be active at a time (unless all filter)
        if (element.id != 'course-checkbox') {
            $("#course-checkbox")[0].checked = false;
        }
        if (element.id != 'faculty-checkbox') {
            $("#faculty-checkbox")[0].checked = false;
        }
        if (element.id != 'room-checkbox') {
            $("#room-checkbox")[0].checked = false;
        }
        if (element.id != 'time-checkbox') {
            $("#time-checkbox")[0].checked = false;
        }
        //@TODO Add selected filter options to the option window
        // - Make AJAX for options ex) Courses -> ajax:getallcourses
        // - Put all in options window, give them id 
    }
    else {
        //@TODO Remove selected filter options from the option window
        // - Remove all options related to filter from option window
    }
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

