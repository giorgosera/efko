####################################
# Tornado App Launcher.            #
# Author: Giorgos Eracleous  	   #
# Acknowledgement: Alexis Michael  #
####################################

import ConfigParser #@UnresolvedImport
import environment #@UnusedImport
import tornado.web, os, pymongo
import app.deps 
from urls import url_patterns
from dependencies import css_deps, js_deps
from mongoengine import connect #@UnresolvedImport
from optparse import OptionParser #@UnresolvedImport

class Youcoverme(tornado.web.Application):
    def __init__(self, env, port, config_file):
	self.APP_NAME = "youcoverme-" + str(port)
	
	settings = {
                    'static_path'   : "static",
                    'template_path' : "templates",
                    'cookie_secret' : "aKlRsPkySWyOqByxAQfLsKMbEAKj3ErRtg1RgkBUQ6E=noteslib",
                    'login_url'     : "/register", #landing page if user is not authenticated
                    'xsrf_cookies'  : True,
                    'autoescape'    : "xhtml_escape",
                    'facebook_api_key': "301107653292393",
                    'facebook_secret': "49acde9b4ccc9a22cb71d0813a3e5030"
                    }

	config = ConfigParser.RawConfigParser()
        config.read(config_file)

	############################
        #  Databse configuration   #
        ############################
        
        db_host = config.get(env, "db_host") or "localhost"
        db_name = "efko_db"
        db_user = config.get(env, "db_user")
        db_pass = config.get(env, "db_pass")

	if env == "prod" and db_user and db_pass:
            connect(db_name, host=db_host, username=db_user, password=db_pass)
        else:
            connect(db_name, host=db_host)
        
        conn = pymongo.Connection(host=db_host)

	if hasattr(conn, db_name):
            db = getattr(conn, db_name)
            if env == "prod" and db_user and db_pass:
                db.authenticate(db_user, db_pass)
            # Create some capped collections..
            if "system.profile" not in db.collection_names():
                db.create_collection("system.profile", capped=True, size=50000000, max=300000)
            db.set_profiling_level(pymongo.ALL)

        ############################################
        ## Configure CSS and JS dependency loader ##
        ############################################
        
        deps = app.deps.ScriptDeps().registerDep(css_deps).registerDep(js_deps)

        ########################################################
        ## Initialize references to application-wide modules. ##
        ########################################################
            
        self.db   = db
        self.deps = deps
        self.env  = env
        
        tornado.web.Application.__init__(self, url_patterns, **settings)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", type="int", dest="port", help="Server port.")
    parser.add_option("-c", type="string", dest="config", help="Config file location.")
    options, args = parser.parse_args()
    
    env = "NLENV" in os.environ and os.environ["NLENV"] or "dev"
    config_file = options.config or os.path.join("config", "config.default")
    
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    print "pre"
    port = int(options.port or config.get(env, "port") or 8888)
    print port
    Youcoverme(env, port, config_file).listen(port)
    
    tornado.ioloop.IOLoop.instance().start()
