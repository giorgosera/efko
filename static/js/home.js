/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    $("a.btn-success").live("click", function() {
	sid = $(this).attr("sid");
	CYP.post("/vote", 
		 {sid : sid},
		 true,
		 function(response) {
			console.log("Vote casted")
			});
    });

    $("#next-cover-btn").live("click", function() {
	CYP.get("/next", 
		 true,
		 function(response) {
		     console.log("new videos");
		 });
    });
    
    $("#selected-genre").live("click", function() {
	genre = $(this).attr("value");
	//TODO pick one genre
    });


