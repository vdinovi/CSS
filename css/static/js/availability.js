function updateAvailability(availablity_list){
	var table = document.getElementById("table");
    for (var i = 0, row; row = table.rows[i]; i++) {
    	if(row.cells[1].innerHTML == name)
        {
        	document.getElementById("edit_room_name").value = name;
            document.getElementById("edit_room_description").value = row.cells[2].innerHTML;
            document.getElementById("edit_room_capacity").value = row.cells[3].innerHTML;
            document.getElementById("edit_room_notes").value = row.cells[4].innerHTML;
            document.getElementById("edit_room_equipment").value = row.cells[5].innerHTML;
          }
        }
      }