/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    $("a.btn-success").live("click", function() {
	sid = $(this).attr("sid");
	if (! $(this).attr("disabled")) {
		CYP.post("/vote", 
			 {sid : sid},
			 true,
			 function(response) {
				$("a.btn-success").attr("disabled", "disabled");
				$("#votes-first").attr("style", "display:inline");
				$("#votes-second").attr("style", "display:inline");
			 });
	}
    });

    $("#next-cover-btn").live("click", function() {
	CYP.get("/next", 
		 true,
		 function(response) {
		     console.log("new videos");
		 });
    });


    


