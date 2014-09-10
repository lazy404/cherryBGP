#
# encoding: UTF-8

import random
import string

import cherrypy

string=""

class CherryBGPStatus(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):
        return {'peers': ['10.0.2.2', '10.0.2.1'], '10.0.2.2': 'Online', '10.0.2.1': 'Down'}
        
    @cherrypy.expose
    def index(self):
        return r'''<html>
    <head>
        <title>AJAX with jQuery and cherrypy</title>
        <script type="text/javascript" src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
    <script type="text/javascript">
        $(function() {
        $("#testform").submit(function() {
            // post the form values via AJAX…
            var postdata = {route: $("#name").val()} ;
            $.post('/routes', postdata, function(data) {
                // and set the title with the result
                $("#title").html(data['status']) ;
               });
            return false ;
            });
        });
        
        (function status_worker() {
          $.get('/status', function(data) {
            $('#sessions').html(data['peers'].toString());
            setTimeout(status_worker, 5000);
          });
        })();
        
    </script>
    </head>
        <body>
        <h1 id="title">What's your name?</h1>
        <h1 id="sessions">...</h1>
        <form id="testform" action="#" method="post">
            <p>
            <label for="name">Name:</label>
            <input type="text" id="name" /> <br />

            <input type="submit" value="Set" />
            </p>
        </form>
        </body>
    </html>'''

class CherryBGPWebService(object):
    exposed = True

    def GET(self):
        global string
        print 'returning', string
        return string

    @cherrypy.tools.json_out()
    def POST(self, route):
        global string
        sting=route
        print 'setting', route
        return {'status': 'route %s added successfully' % route}

    def DELETE(self):
        global string
        string=""

if __name__ == '__main__':
    conf = {
     '/routes': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
     }
    }
    webroot=CherryBGPStatus()
    webroot.routes=CherryBGPWebService()
    cherrypy.quickstart(webroot, '/', conf)