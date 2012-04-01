/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    $("a.btn-success").live("click", function() {
	sid = 5;	
	CYP.post("/vote", 
		 {sid : sid},
		 true,
		 function(response) {
			console.log("Vote casted")
			});
    });

    $("a.close").live("click", function() {
	CYP.post("/populate", 
		 {},
		 true,
		 function(response) {
			console.log("DB populated")
			});
    });
    



