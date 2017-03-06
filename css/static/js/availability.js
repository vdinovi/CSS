function viewAvailablity() {
    var availabilityData = {};
    availabilityData = {
    	'day': $("#id_day").val(), 
        'start_time': $("#id_start_time").val(),
        'end_time': $("#id_end_time").val(),
        'level': $("#id_level").val(),
        'availability_view': 'hello'
         };
    $.ajax({
        type: "POST",
        url: "availabilityView",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(availabilityData),
        dataType: 'json',
        success: function(response) {
        	//javascript object of returned after success 
   			data = response
   			//loop over all of the availability objects for one faculty
        	for (avail in data.availability_view) {
        		console.log(data.availability_view[avail])
        	}
        },
        error: function(err) {
            console.log(err);
        }
    });
}