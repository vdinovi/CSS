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
            Availability.create(
            	response['email'],
                availabilityData.get['day'],
                availabilityData.get['start_time'],
               	availabilityData.get['end_time'],
               	availabilityData.get['level']
                )
        },
        error: function(err) {
            console.log(err);
        }
    });
}