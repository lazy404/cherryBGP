#
# encoding: UTF-8

import os, time, xmlrpclib, ipaddr
import cherrypy
import config

class CherryBGPStatus(object):
    
    def __init__(self, rpc_url):
        self.rpc_url=rpc_url
        self.rpc=xmlrpclib.ServerProxy(rpc_url)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['GET'])
    def status(self):
        return [{'peer':'10.0.2.2', 'status': 'Online'}, {'peer': '10.0.2.1', 'status': 'Down'}]
        
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
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
            $.post('/set_route', postdata, function(data) {
                $("#last_command").html(data['log']);

                if(data['status'] == 'ok')
                    $('#blform')[0].reset();

               });
            return false ;
            });
        });
/*
        (function status_worker() {
            
            $.get('/status', function(data) {
              
            var transform= {"tag":"div","children":[
                  {"tag":"span","html":"Peer: ${peer}"},
                  {"tag":"span","html":"Status: ${status}"}]};
            
            $('#sessions').html(json2html.transform(data, transform));
            setTimeout(status_worker, 5000);
          });
        })();
*/

        (function routes_worker() {
            setTimeout(routes_worker, 4000);

          $.get('/routes', function(data) {
            var transform =   {"tag":"tr","children":[
                                {"tag":"td","html":"${dst}"},
                                {"tag":"td","html":"${typ}"},
                                {"tag":"td","html":"${created}"},
                                {"tag":"td","html":"${ttl}"}
                              ]};
            $('#routes').html(json2html.transform(data, transform));
            //$('#routes').json2html(data, transform, {'replace': true});
            
          });
        })();
        
    </script>
    </head>
        <body>
        <!-- <div id="sessions">Status Unknown</div> -->
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
              <option value="Zagranica">Zagranica</option>
              <option value="Global">Wszystko</option>
            </select></br>
            <label for="typ">TTL:</label>
            <select id=ttl>
              <option value="60">1 minute</option>
              <option value="180">3 munutes</option>
              <option value="600">10 munutes</option>
              <option value="0">Remove</option>
            </select></br>

            <input type="submit" value="Set" />
            </p>
        </form>

        <div id="last_command"></div><br>
        
        </body>
    </html>'''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['GET'])
    def routes(self):
        table = []
        #'neighbor 86.111.240.24 10.11.11.11/32 next-hop 10.0.200.1\n'
        #table = [{'dst': '10.2.2.2/32', 'typ': 'global', 'created': 19999, 'ttl':19999},]

        #TODO: implement proper rpc function write + select + read
        self.rpc.write('show routes\n')
        time.sleep(0.5)
        ret=self.rpc.read()
        print ret
        for l in ret.split('\n'):
            if l:
                (dummy, neighbor, dst, dummy, nh)=l.split(' ')
                table.append({'dst':dst, 'typ': 'global', 'ttl':199})
        print table
        return table
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['POST'])
    def set_route(self, dst, typ, ttl):
        try:
            dst=str(ipaddr.IPAddress(dst))
            ttl=int(ttl)
            if ttl > 0 :
                cmd='announce route %s/32 next-hop 10.0.200.1 community [%s]\n' % (dst, config.community_map[typ])
            else:
                cmd='withdraw route %s/32 next-hop 10.0.200.1 community [%s]\n' % (dst, config.community_map[typ])
                
            self.rpc.write(cmd)
        except Exception as e:
            return {'status': 'error', 'log': str(e)}

        return {'status': 'ok', 'log': 'route %s sent' % dst}
        #return {'status': 'error', 'log': 'route %s added unsuccessfully' % dst}
 
if __name__ == '__main__':
    conf = {
     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './static',
         'tools.staticdir.root': os.path.abspath(".")
     }
    }
    
    #webroot=CherryBGPStatus()
    #webroot.routes=CherryBGPWebService()
    cherrypy.quickstart(CherryBGPStatus(config.rpc_url), '/', conf)