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


    $("#non-autenticated-vote").live("click", function() {
	var tmpl = $("#registration-popup-template").tmpl();
	CYP.popup.show(tmpl);
    });


    $("#next-cover-btn").live("click", function() {
	CYP.get("/next", 
		 true,
		 function(response) {
		     console.log("new videos");
		 });
    });

    $("#close-registration-popup").live("click", function() {
	CYP.popup.close();
    });




    


