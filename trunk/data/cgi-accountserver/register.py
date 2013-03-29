#!/usr/bin/python
#import cgitb;print 'Content-Type: text/html\n';cgitb.enable()
import db
import os

header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <title>Create Username/password</title>
</head>
<body>
"""

footer = """
</body>
</html>
"""

def print_heading():
    print('<h1>Create Username/password</h1>')

def print_form(filedb, mod):

    modstr=''
    if mod:
        modstr='?'+mod
    print('<form name="type" action="register_submit.py'+modstr+'" method="post">')
    print('<table>')
    type_select(filedb)
    faction_select(filedb)
    field('Handle','username')
    field('Password','password')
    submit_button()
    print('</table>')
    print('</form>')

def type_select(filedb):
    print('<tr>')
    print('<td align= "right">Which type?</td>')
    print('<td><select name="type" size="1">')
    type_dat = filedb.get_default_csv(None)
    units = type_dat[2:]
    units.sort()
    for line in units:

        if (len(line) and line.find("turret")==-1):
            name=""
            if line.find("./weapons")!=-1:
                break
            if line[0]=='"':
                endl=line[1:].find('"')
                if endl!=-1:
                    name=line[1:1+endl]
            else:
                endl=line.find(",")
                if endl!=-1:
                    name=line[:endl]
            if (len(name) and name.find("__")==-1 and name.find(".blank")==-1 and name!="beholder"):
                print('<option>'+name+'</option>')
    print('</select></td>')
    print('</tr>')


def faction_select(filedb):
    print('<tr>')
    print('<td align= "right">Which faction?</td>')
    print('<td><select name="faction" size="1">')
    f = filedb.open_default_file("factions.xml")
    type_dat = f.readlines()
    f.close()
    for line in type_dat[2:]:
        factionnamestr='action name="'
        where=line.find(factionnamestr)
        if (len(line) and where!=-1):
            name=""
            subline=line[where+len(factionnamestr):]
            where2=subline.find('"')
            if where2==-1:
                break
            name=subline[:where2]
            if (len(name) and name!="upgrades" and name!="neutral" and name!="planets"):
                print('<option>'+name+'</option>')
    print('</select></td>')
    print('</tr>')


def field(title, name):
    print('<tr>')
    print('<td align="right">'+title+':</td>')
    print('<td><input name="'+name+'" type="text" size="20"></td>')
    print('</tr>')

def submit_button():
    print('<tr><td colspan=2 align="center">')
    print('<input value="Submit" type="submit">')
    print('</td></tr>')

get_form=False
post_form=False
def execute(filedb, mod, post):
    print("Content-Type: text/html")
    print("")
    print(header)
    print_heading()
    print_form(filedb, mod)
    print(footer)

if __name__ == '__main__':
    mod = os.environ.get('QUERY_STRING','')
    filedb = db.DBBase(mod)
    execute(filedb, mod, '')
