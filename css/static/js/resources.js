function setDeleteFormItem(string, resourceType){
  console.log("name " + string + " resourceType " + resourceType);
  console.log("previous value " + document.getElementById(resourceType).value);
  document.getElementById(resourceType).value = string;
  console.log("value: " + document.getElementById(resourceType).value);

}
function setEditFormFields(name, resourceType){
  console.log("name " + name);
  var table = document.getElementById("table");
  for (var i = 0, row; row = table.rows[i]; i++) {
    if(row.cells[1].innerHTML == name)
    {
      console.log(resourceType);

      //document.getElementById("edit_room_name").value = name;
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
        document.getElementById("edit_course_course_name").value = name;
        document.getElementById("edit_course_equipment_req").value = row.cells[2].innerHTML;
        document.getElementById("edit_course_description").value = row.cells[3].innerHTML;
      }
    }
  }
}
