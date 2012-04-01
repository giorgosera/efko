/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */

    // =============================== Listeners =============================== //
    
    $("#submit-btn").live("click", function() {
	var url = $("#url").val();	
	var title = $("#title").val();
	var artist = $("#artist").val();
	var uploader = $("#uploader").val();
	var genre = $('input[name="genre"]').val();
	if (url && title && uploader && genre){
		CYP.post("/submit", 
			 {url : url,
			  title : title,
			  artist : artist,
			  uploader: uploader,
			  genre: genre
			 },
			 true,
			 function(response) {
				CYP.successNotifier.show(response.msg)
		});
	} 
	else{
		$("#url").val("");	
		$("#title").val("");
		$("#artist").val("");
		$("#uploader").val("");
		CYP.successNotifier.show("Some fields are missing!")	
	}

    });
