function getRank() {
	rank_vals = {};
	$( "#sortable" ).children("li").each(function(index,value) {
		index = index + 1
		rank_vals[index.toString()] = $(value).text();
	});
}

//updates the database with ranks
function updateRank() {
	getRank();
	$.ajax({
		type: "POST",
        url: "update-rank",
        data: JSON.stringify(rank_vals), 
        dataType: "json"
	});
}


