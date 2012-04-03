/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */

    // =============================== Listeners =============================== //

	$('#user-form').submit(function() {
	   	var username = $("#username").val();	
	   	var first = $("#first").val();
	   	var last = $("#last").val();
	   	var email = $("#email").val();
		var password = $("#password").val();
		var passwordVerify = $("#password-verify").val();
		if (username && password && passwordVerify){
			if ( password != passwordVerify ){
				CYP.successNotifier.show("Passwords do not match.");
				return false;			
			}

			return true;
		} 
		else{			
			CYP.successNotifier.show("Some fields are missing.");
 		       return false;	
		}
	});    

	$('#login-form').submit(function() {
	   	var username = $("#username").val();	
		var password = $("#password").val();
		if (username && password){
			return true;
		} 
		else{			
			CYP.successNotifier.show("Some fields are missing.");
 		       return false;	
		}
	});    
