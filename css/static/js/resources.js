function setDeleteFormItem(string, resourceType){

  document.getElementById(resourceType).value = string;

}
function setEditFormFields(name, resourceType){
  print "punch"
  var table = document.getElementById("table");
  for (var i = 0, row; row = table.rows[i]; i++) {

    if(row.cells[1].innerHTML == name)
    {
      if(resourceType == 'room')
      {
        document.getElementById("edit_room_name").value = name;
        document.getElementById("edit_room_description").value = row.cells[2].innerHTML;
        document.getElementById("edit_room_capacity").value = row.cells[3].innerHTML;
        document.getElementById("edit_room_notes").value = row.cells[4].innerHTML;
        document.getElementById("edit_room_equipment").value = row.cells[5].innerHTML;
      }
      else if(resourceType == 'course')
      {
	document.write("flower power")
        document.getElementById("edit_course_course_name").value = name;
        document.getElementById("edit_course_equipment_req").value = row.cells[2].innerHTML;
        document.getElementById("edit_course_description").value = row.cells[3].innerHTML;
      }
      else if(resourceType == 'faculty')
	document.write("turbulance")
	document.getElementById("edit_faculty_name").value = name;
	document.getElementById("edit_faculty_email").value = row.cells[1].innerHTML;
    }
  }
}

/*-----------------------------------Resources Page----------------------------------------------*/
var currentCourse;
var currentFaculty;
var csrf;

  function addSectionType() {
    $('#add-section-type-area').show();
    $('#save-section-type-button').show();
    $('#add-section-type-button').hide()
  }
  function submitSectionType() {
    var checkBoxes = $("input[name='name']");

    for (var i = 0; i < checkBoxes.length; i++)
    {
      if(checkBoxes[i].checked)
      {
        var selectedSectionType = checkBoxes[i].value;
        break;
      }

    }

    $.post("/resources/courses/",
          {
              "csrfmiddlewaretoken": csrf,
              "request-name":'save-section-request',
              "course": currentCourse,
              "id_name": selectedSectionType,
              "id_work_units": $('#id_work_units').val(),
              "id_work_hours": $('#id_work_hours').val()
          },

          updateSectionTypesView
    );

    $('#add-section-type-area').hide();
    $('#save-section-type-button').hide();
    $('#add-section-type-button').show()
  }

  function getCourseInfo(course) {
    currentCourse = course;
    csrf = $('#csrf-token').html();

    $.post("/resources/courses/",
          {
              "csrfmiddlewaretoken": csrf,
              "request-name": "course-section-request",
              "course": course
          },

          updateSectionTypesView
    );
  }

  function deleteSectionType(sectionTypeName, courseName) {
    $.post("/resources/courses/",
          {
              "csrfmiddlewaretoken": csrf,
              "request-name": "delete-section-type-request",
              "course": courseName,
              "section_type_name": sectionTypeName
          },

          updateSectionTypesView
    );
  }
  function updateSectionTypesView(data, status){
     var sectionTypes = JSON.parse(data);
      $('#ajax-area').empty();

     for(var sectionType in sectionTypes) {
       $('#ajax-area').append("<p><button onclick=\"deleteSectionType('" + sectionTypes[sectionType].section_type_name + "', '" + sectionTypes[sectionType].course_name + "')\"style=\"font-size: .7em;\" type=\"button\" class=\"btn btn-info btn-xs\" data-toggle=\"modal\" data-target=\"#add-section-type\"><span class=\"glyphicon glyphicon-minus\"></button> " + sectionTypes[sectionType].section_type_name + " Work Units: " + sectionTypes[sectionType].work_units + " Work Hours: " + sectionTypes[sectionType].work_hours + "</p>");
    }
  }

  function getFacultyInfo(CUser) {
    currentFaculty = CUser;
    csrf = $('#csrf-token').html();
    print "we out here"
    $.post("/resources/faculty/",
	{
	    "crsfmiddlewaretoken": csrf,
	    "request-name": "faculty-name-request",
	    "faculty": CUser
	},

	updateSectionTypesView
    );
