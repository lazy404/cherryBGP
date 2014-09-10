#
# encoding: UTF-8

import os, time
import cherrypy

table = [{'dst': '10.2.2.2/32', 'typ': 'global', 'created': 19999, 'ttl':19999}, {'dst': '10.2.10.2/32', 'typ': 'pl', 'created': 19999, 'ttl':19999},]

class CherryBGPStatus(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):
        return [{'peer':'10.0.2.2', 'status': 'Online'}, {'peer': '10.0.2.1', 'status': 'Down'}]
        
    @cherrypy.expose
    def index(self):
        return r'''<html>
    <head>
        <title>AJAX with jQuery and cherrypy</title>
        <style type="text/css"><!--
        body { font-family: arial, helvetica, sans-serif; font-size: 12px; font-weight: normal; color: black; background: white;}
        th,td { font-size: 16px;}
        h1 { font-size: x-large; margin-bottom: 0.5em;}
        h2 { font-family: helvetica, arial; font-size: x-large; font-weight: bold; font-style: italic; color: #6020a0; margin-top: 0em; margin-bottom: 0em;}
        h3 { font-family: helvetica, arial; font-size: 16px; font-weight: bold; color: #b00040; background: #e8e8d0; margin-top: 0em; margin-bottom: 0em;}
        li { margin-top: 0.25em; margin-right: 2em;}
        .hr {margin-top: 0.25em; border-color: black; border-bottom-style: solid;}
        .titre	{background: #20D0D0;color: #000000; font-weight: bold; text-align: center;}
        .total	{background: #20D0D0;color: #ffff80;}
        .frontend	{background: #e8e8d0;}
        .socket	{background: #d0d0d0;}
        .green	{background: #c0ffc0;}
        .red	{background: #f07849;}
        .yellow	{background: #co7820;}
        .rls      {letter-spacing: 0.2em; margin-right: 1px;}

        a.px:link {color: #ffff40; text-decoration: none;}a.px:visited {color: #ffff40; text-decoration: none;}a.px:hover {color: #ffffff; text-decoration: none;}a.lfsb:link {color: #000000; text-decoration: none;}a.lfsb:visited {color: #000000; text-decoration: none;}a.lfsb:hover {color: #505050; text-decoration: none;}
        table { border-collapse: collapse; border-style: none;}
        table td { text-align: right; border-width: 1px 1px 1px 1px; border-style: solid solid solid solid; padding: 2px 3px; border-color: gray; white-space: nowrap;}
        table td.ac { text-align: left;}
        table td.cac { text-align: center;}
        table th { border-width: 1px; border-style: solid solid solid solid; border-color: gray;}
        table th.pxname { background: #b00040; color: #ffff40; font-weight: bold; border-style: solid solid none solid; padding: 2px 3px; white-space: nowrap;}
        table th.empty { border-style: none; empty-cells: hide; background: white;}
        table th.desc { background: white; border-style: solid solid none solid; text-align: left; padding: 2px 3px;}

        table.lgd { border-collapse: collapse; border-width: 1px; border-style: none none none solid; border-color: black;}
        table.lgd td { border-width: 1px; border-style: solid solid solid solid; border-color: gray; padding: 2px;}
        table.lgd td.noborder { border-style: none; padding: 2px; white-space: nowrap;}
        u {text-decoration:none; border-bottom: 1px dotted black;}
        -->
        </style>
        <script type="text/javascript" src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
        <script type="text/javascript" src="/static/json2html.js"></script>
        <script type="text/javascript" src="/static/jquery.json2html.js"></script>
    <script type="text/javascript">
        $(function() {
        $("#blform").submit(function() {
            // post the form values via AJAX…
            var postdata = {dst: $("#dst").val(), ttl: $("#ttl").val(), typ: $("#typ").val()} ;
            $.post('/routes', postdata, function(data) {
                $("#last_command").html(data['log']);

                if(data['status'] == 'ok')
                    $('#blform')[0].reset();

               });
            return false ;
            });
        });
        
        (function status_worker() {
            
            $.get('/status', function(data) {
              
            var transform= {"tag":"div","children":[
                  {"tag":"span","html":"Peer: ${peer}"},
                  {"tag":"span","html":"Status: ${status}"}]};
            
            $('#sessions').html(json2html.transform(data, transform));
            setTimeout(status_worker, 5000);
          });
        })();
        
        (function routes_worker() {
          $.get('/routes', function(data) {
            var transform =   {"tag":"tr","children":[
                                {"tag":"td","html":"${dst}"},
                                {"tag":"td","html":"${typ}"},
                                {"tag":"td","html":"${created}"},
                                {"tag":"td","html":"${ttl}"}
                              ]};
            $('#routes').html(json2html.transform(data, transform));
            //$('#routes').json2html(data, transform, {'replace': true});
            
            setTimeout(routes_worker, 2000);
          });
        })();
        
    </script>
    </head>
        <body>
        <div id="sessions">Status Unknown</div>
        Active blackhole routes:
        <table>
        <tr><th>Destination</th><th>Type</th><th>Created</th><th>Ttl</th></tr>
        <tbody id="routes">
        </tbody>
        </table><br/>
        Inject blackhole:
        <form id="blform" action="#" method="post">
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

        <div id="last_command"></div><br>
        
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

        
        return {'status': 'ok', 'log': 'route %s added successfully' % dst}
        #return {'status': 'error', 'log': 'route %s added unsuccessfully' % dst}
        
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