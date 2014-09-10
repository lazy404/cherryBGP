#
# encoding: UTF-8

import os, time
import cherrypy

table = [{'dst': '10.2.2.2/32', 'typ': 'global', 'created': 19999, 'ttl':19999}, {'dst': '10.2.10.2/32', 'typ': 'pl', 'created': 19999, 'ttl':19999},]

class CherryBGPStatus(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):
        return [{'peer':'10.0.2.2', 'status': 'Online %d' % int(time.time())}, {'peer': '10.0.2.1', 'status': 'Down'}]
        
    @cherrypy.expose
    def index(self):
        return r'''<html>
    <head>
        <title>AJAX with jQuery and cherrypy</title>
        <script type="text/javascript" src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
        <script type="text/javascript" src="/static/json2html.js"></script>
        <script type="text/javascript" src="/static/jquery.json2html.js"></script>
    <script type="text/javascript">
        $(function() {
        $("#testform").submit(function() {
            // post the form values via AJAX…
            var postdata = {dst: $("#dst").val(), ttl: $("#ttl").val(), typ: $("#typ").val()} ;
            $.post('/routes', postdata, function(data) {
                // and set the title with the result
                $("#last_command").html(data['status']) ;
               });
            return false ;
            });
        });
        
        (function status_worker() {
            
            $.get('/status', function(data) {
              
              var transform= {"tag":"div","id":"${id}","children":[
                  {"tag":"span","html":"Peer: ${peer}"},
                  {"tag":"span","html":"Status: ${status}"}
                ]};
            $('#sessions').html('');
            $('#sessions').json2html(data, transform, {'replace': true});
            setTimeout(status_worker, 5000);
          });
        })();
        
        (function routes_worker() {
          $.get('/routes', function(data) {
            var transform = {"tag":"tbody","id":"${id}","children":[
                            {"tag":"tr","children":[
                                {"tag":"td","html":"${dst}"},
                                {"tag":"td","html":"${typ}"},
                                {"tag":"td","html":"${created}"},
                                {"tag":"td","html":"${ttl}"}
                              ]}
                          ]};
            $("#routes").html('');
            $('#routes').json2html(data, transform, {'replace': true});
            setTimeout(routes_worker, 2000);
          });
        })();
        
    </script>
    </head>
        <body>
        <div id="sessions">Status Unknown</div>
        <div id="last_command"></div><br>
        Active blackhole routes:
        <table>
        <tr><th>Destination</th><th>Type</th><th>Created</th><th>Ttl</th></tr>
        <tbody id="routes">
        </tbody>
        </table><br/>
        Inject blackhole:
        <form id="testform" action="#" method="post">
            <p>
            <label for="dst">Name:</label>
            <input type="text" id="dst" /> <br />
            <label for="typ">Typ:</label>
            <select id=typ>
              <option value="global">Zagranica</option>
              <option value="all">Wszystko</option>
            </select></br>
            <label for="typ">TTL:</label>
            <select id=ttl>
              <option value="60">1 minute</option>
              <option value="180">3 munutes</option>
              <option value="600">10 munutes</option>
            </select></br>

            <input type="submit" value="Set" />
            </p>
        </form>
        
        </body>
    </html>'''

class CherryBGPWebService(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        global table
        print table
        return table
        
    @cherrypy.tools.json_out()
    def POST(self, dst, typ, ttl):
        global table
        table.append({'dst': str(dst), 'typ': str(typ), 'created': int(time.time()), 'ttl':int(ttl)})

        
        return {'status': 'route %s added successfully' % dst}

    def DELETE(self):
        global string
        string=""

if __name__ == '__main__':
    conf = {
     '/routes': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
     },
     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './static',
         'tools.staticdir.root': os.path.abspath(".")
     }
    }
    
    webroot=CherryBGPStatus()
    webroot.routes=CherryBGPWebService()
    cherrypy.quickstart(webroot, '/', conf)