/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //


    $("#dlt-btn").live("click", function() {
	var sid = $(this).attr("sid");
	CYP.post("/thisisasecreturl18211281", 
		 {sid: sid},
		 true,
		 function(response) {
		     CYP.popup.show("Song deleted!");
		 });
    });
    
