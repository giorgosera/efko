############################
# CSS and JS dependencies  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
             ("/login/google", ["bootstrap.css"]),
             ("/", ["bootstrap.css", "bootstrap-responsive.css"])
            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/register/google/*", ["user.js"]),
             ("/thisisasecreturl18211281", ["admin.js"]),
	         ("/rankings", ["/libs/twitter/*"]),
             ("/", ["home.js", "submit.js"])  		
	        ])

