#
# encoding: UTF-8

import os, time, xmlrpclib, ipaddr, exceptions, traceback
import cherrypy
import config

from util import *

class CherryBGPStatus(object):
    
    def __init__(self, rpc_url):
        self.rpc_url=rpc_url
        self.rpc=xmlrpclib.ServerProxy(rpc_url)
        self.allow_prefix=map(ipaddr.IPNetwork, config.allow_prefix) 
        self.ban_prefix=map(ipaddr.IPNetwork, config.ban_prefix)

    def allowed(self, ip):
        for n in self.ban_prefix:
            if ip in n:
                return False

        for n in self.allow_prefix:
            if ip in n:
                return True

        return False

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
        <title>cherryBGP</title>
        <style type="text/css"><!--
        body { font-family: arial, helvetica, sans-serif; font-size: 14px; font-weight: normal; color: black; background: #a0bbc0;}
        a {text-decoration: none;}
        th {background: #e8e8d0;}
        td {background: #c0ffc0;}
        h1 { font-size: x-large; margin-bottom: 0.5em;}
        h2 { font-family: helvetica, arial; font-size: x-large; font-weight: bold; font-style: italic; color: #6020a0; margin-top: 0em; margin-bottom: 0em;}
        h3 { font-family: helvetica, arial; font-size: 16px; font-weight: bold; color: #6020a0; background: #e8e8d0; margin-top: 0em; margin-bottom: 0em;}
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
        <script type="text/javascript" src="/static/jquery-2.0.3.min.js"></script>
        <script type="text/javascript" src="/static/json2html.js"></script>
        <script type="text/javascript" src="/static/jquery.json2html.js"></script>
        <!--<script type="text/javascript" src="/static/jquery.input-ip-address-control-1.0.min.js"></script>-->
        

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
        <tr>
        <td>${dst}</td><td>${typ}</td><td><td>${community}</td><a class="del" href="/dele/${dst}">Remove</a></td>
        </tr>
        
        <tr>
        <td>${dst}</td><td>${typ}</td><td>${community}</td><td><a class="del" ref="/dele/${dst}">Remove</a></td>
        </tr>
        
*/

        (function routes_worker() {
            setTimeout(routes_worker, 4000);

          $.get('/routes', function(data) {
            var transform ={"tag":"tr","children":[
    {"tag":"td","html":"${dst}"},
    {"tag":"td","html":"${typ}"},
    {"tag":"td","html":"${community}"},
    {"tag":"td","children":[
        {"tag":"a","class":"del","href":"/dele/${dst}","html":"Remove"}
      ]}
  ]};
            $('#routes').html(json2html.transform(data, transform));
            //$('#routes').json2html(data, transform, {'replace': true});
            
            //$("#last_command").html('');
            
            $(".del").click(function() {
                var del_dst = this.href.slice(this.href.lastIndexOf('/')+1);
                if (confirm('Are you sure you want to remove: '+del_dst+' ?')) {
                    // Save it!
                    var postdata = {dst: del_dst} ;
                    $.post('/del_route', postdata, function(data) {
                        $("#last_command").html(data['log']);
                       });
                }
                
                return false; // return false so that we don't follow the link!
            });
            
          });
        })();
        
    </script>
    </head>
        <body>
        <!-- <div id="sessions">Status Unknown</div> -->
        <h2 class="red">Active blackhole routes:</h2>
        <table>
        <tr><th>Destination</th><th>Type</th><th>Community</th><th>Action</th></tr>
        <tbody id="routes">
        </tbody>
        </table><br/><br/>
        <h3>Inject blackhole routes:</h2>
        <form id="blform" action="#" method="post">
            <input type="text" size=16 id="dst" />
            <label for="dst">- IP</label><br/>
            
            <select id=typ multiple>
              %s
            </select>
            <label for="typ">- Blackholle types</label><br />
            
            <input type="submit" value="Announce"/>
        </form>

        <div id="last_command"></div><br>
        
        </body>
    </html>''' % '\n'.join(['<option value="%s">%s</option>' % (t, t) for t in config.community_map.keys()])

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['GET'])
    def routes(self):
        table = []
        #'neighbor 86.111.240.24 10.11.11.11/32 next-hop 10.0.200.1\n'
        #table = [{'dst': '10.2.2.2/32', 'typ': 'global', 'created': 19999, 'ttl':19999},]

        #TODO: implement proper rpc function write + select + read
        ret=self.rpc.api_call('show routes extensive\n')
        #ret=self.rpc.api_call('show routes\n')
        print ret
        for l in ret.split('\n'):
            if l:
                rt=l.split()
                com=rt.index('community') + 1
                dst=rt.index('next-hop') - 1
                comunities=filter(lambda x: x not in ('[', ']', 'extended-community'), rt[com:])
                table.append({'dst':rt[dst].split('/')[0], 'typ': nr_to_txt(comunities), 'community': ' '.join(comunities)})
        print table
        return table
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['POST'])
    def set_route(self, **kw):
        try:
            dst=kw['dst']
            typ=kw['typ[]']
            dst=ipaddr.IPAddress(dst)
            
            if not self.allowed(dst):
                raise Exception('%s not allowed' % str(dst))

            if type(typ) != list:
                typ=[typ]
            
            cmd='announce route %s/32 next-hop %s %s\n' % (str(dst), config.nexthop, txt_to_nr(map(str, typ)))

            self.rpc.api_call_noret(cmd)
        except Exception as e:
            print traceback.format_exc()
            return {'status': 'error', 'log': str(e)}

        return {'status': 'ok', 'log': 'route %s sent ' % cmd}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=['POST'])
    def del_route(self, dst):
        try:
            dst=str(ipaddr.IPAddress(dst))
            cmd='withdraw route %s/32 next-hop %s\n' % (dst, config.nexthop)
            self.rpc.api_call_noret(cmd)
        except Exception as e:
            return {'status': 'error', 'log': str(e)}

        return {'status': 'ok', 'log': 'route %s withdrawn'% cmd}

if __name__ == '__main__':

    conf = {
     'global': {
         'tools.basic_auth.on': True,
         'tools.basic_auth.realm': 'cherryBGP',
         'tools.basic_auth.users': config.users,
         'tools.basic_auth.encrypt': config.encrypt_pw,
         },
     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './static',
         'tools.staticdir.root': os.path.abspath(".")
         },
    }
    
    cherrypy.quickstart(CherryBGPStatus(config.rpc_url), '/', conf)
