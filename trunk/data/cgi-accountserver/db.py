import random
import os
import urllib.request, urllib.parse, urllib.error
import sys

try:
    import settings
except(ImportError):
    sys.stdout.write("Content-Type: text/html\r\n\r\n")
    print("UNKNOWN Error&trade;:")
    print("Failed to import settings module.  <br>")
    print("You probably just checked out the server and have not customized it yet. <br>")
    print("")
    print("Copy settings.sample.py to settings.py and edit it to your liking.")
    print("Also, make sure that you have created a units/ folder that contains these four")
    print("files: default.save, factions.xml, units.csv and vegastrike.config.")
    print("For each 'mod', make a folder inside the units/ folder containing a copy of")
    print("those four files, with custom mod settings.")
    print("")
    sys.exit(0)


#CGI Helper function to replace buggy FieldStorage
def urlDecode(args):
    argsplit = args.split('&')
    arglist = {}
    for arg in argsplit:
        if not arg:
            continue
        argsp= arg.split('=')
        name = urllib.parse.unquote(argsp[0])
        if len(argsp)>1:
            value = urllib.parse.unquote(argsp[1].replace('+',' '))
        else:
            value = ''
        arglist[name] = value
    return arglist

class DBError(RuntimeError):
    def __init__(self, args):
        RuntimeError.__init__(self, args)

# Catch this error for problems with input.
class DBInputError(DBError):
    def __init__(self, args):
        DBError.__init__(self, args)

class DBBase:
    def __init__(self, mod):
        if mod not in settings.mods:
            raise DBInputError("Invalid mod '"+mod+"'")
        self.moddata = settings.mods[mod]
        self.mod = self.moddata['path']
        self.modkey = mod
        self.data_path = settings.data_path
        if self.mod:
            self.data_path += '/' + self.mod
    def check_password(self, username, password):
        return False
    def modify_account(self, username, type="llama.begin", faction="confed"):
        self.save_account(username, self.get_default_save(type, faction),
                self.get_default_csv(type))

    def save_account(self, username, save, csv):
        pass
    def get_login_info(self, user, password):
        pass
    def hash_password(self, password):
        import hashlib
        if settings.password_hash_methode == 'md5':
            return hashlib.md5(password).hexdigest()
        elif settings.password_hash_methode == 'sha':
            return hashlib.sha1(password).hexdigest()

    def compare_password(self, hash, password):
        phash = self.hash_password(password)
        if len(hash)<len(phash):
            return password == hash
        else:
            return phash.lower() == hash.lower()

    def check_string(self, s):
        if not s:
            return "" # Should return something at least.
            #raise DBInputError, "All fields must be non-empty."
        for c in s:
            oc = ord(c)
            if oc < 32 or oc >= 127:
                raise DBInputError("Invalid character "+str(oc)+" in field.")
        return s

    def get_server(self, system):
        servers = self.moddata['servers']
        return servers.get(system,
                servers.get(system.split('/')[0],
                servers.get('', "0.0.0.0:4364")))
    def open_default_file(self, file):
        return open(self.data_path+'/'+file,"rb")

    def get_default_save(self, shiptype='', faction=''):
        try:
            f=self.open_default_file("network.save")
        except IOError:
            try:
                f=self.open_default_file("New_Game")
            except IOError:
                try:
                    f=self.open_default_file("accounts/default.save")
                except IOError:
                    try:
                        f=self.open_default_file("default.save")
                    except:
                        raise DBError("Not able to open the default saved game.")
        s = f.read()
        f.close()
        if not shiptype:
            return s
        caret = s.find('^')
        if caret != -1:
            caret = s.find('^', caret+1)
        eol = s.find('\n')
        if caret == -1 or eol == -1:
            s='Crucible/Cephid_17^\n'
            caret = len(s)-2
            eol = len(s)-1
        if not faction:
            lastsp = s.rfind(' ',0,eol)
            faction = s[lastsp+1:eol]
        s=s[:caret]+"^"+shiptype+" "+str(120000000000+random.uniform(-10000,10000))+" "+str(40000000+random.uniform(-10000,10000))+" "+str(-110000000000+random.uniform(-10000,10000))+" "+faction+s[eol:]
        return s
    def get_default_csv(self, shiptype):
        try:
            unfp=self.open_default_file('units.csv')
        except IOError:
            try:
                unfp=self.open_default_file('units/units.csv')
            except:
                raise DBError("Not able to open units.csv")
        type_dat = unfp.readlines()
        unfp.close()
        if not shiptype:
            return type_dat
        s = ''
        if len(type_dat)>3:
            s += (type_dat[0])
            s += (type_dat[1])
        for line in type_dat[2:]:
            # Turrets do not work server-side, so avoid any ships with turrets for now.
            if (not len(line) or line.find("turret")!=-1):
                continue
            name=""
            if line.find("./weapons")!=-1:
                continue
            if line[0]=='"':
                endl=line[1:].find('"')
                if endl!=-1:
                    name=line[1:1+endl]
            else:
                endl=line.find(",")
                if endl!=-1:
                    name=line[:endl]
            if (len(name) and name.find("__")==-1 and name.find(".blank")==-1 and name!="beholder"):
                if name==shiptype:
                    s += line
                    return s;
        raise DBError("Can not find information for unit '"+shiptype+"'")

class FileDB(DBBase):
    def __init__(self, config, mod):
        DBBase.__init__(self, mod)
        self.storage_path = config['storage']
        if self.storage_path[-1]=='/':
            self.storage_path = self.storage_path[:-1]
        try:
            os.mkdir(self.storage_path)
        except:
            pass
        if self.mod:
            try:
                os.mkdir(self.storage_path+'/'+self.mod)
            except:
                pass
        self.storage_path += '/'
        self.user_path = self.storage_path
        if self.mod:
            self.storage_path += self.mod + '/'
        if config.get('create_user',True):
            self.create_user=True
        else:
            self.create_user=False
    def check_password(self, username, password, can_create = False):
        success=False
        try:
            f=open(self.user_path+username+".password","rb")
            s=f.read()
            f.close()
            if self.compare_password(s, password):
                success=True
        except IOError:
            if self.create_user and can_create:
                f=open(self.user_path+username+".password","wb")
                f.write(self.hash_password(password))
                f.close()
                success=True
            else:
                success=False
        return success
    # Checks a string for valid username characters.
    def check_string(self, s):
        if not s:
            raise DBInputError("You must fill out all fields")

        for c in s:
            if not (c.isalnum() or c=='_' or c=='-' or c=='.' or c=='$'):
                raise DBInputError("Invalid character "+c+" in input "+s)

        if s.find("..")!=-1 or s.find(".xml")!= -1 or s.find(".save")!=-1 or s.find("accounts")!=-1 or s.find("default")!=-1:
            raise DBInputError("Invalid character . in input "+s)

        return s

    def save_account(self, username, save, csv):
        o=open(self.storage_path+username+".save","wb")
        o.write(save)
        o.close()
        o=open(self.storage_path+username+".xml","wb")
        o.write(csv)
        o.close()

    def get_login_info(self, user, password):
        result={}
        f=None
        if not self.check_string(user):
            return None
        try:
            f=open(self.user_path+user+".password","rb")
            tpass=f.read()
            f.close()
            if self.compare_password(tpass, password):
                try:
                    f=open(self.storage_path+user+".save","rb")
                    result['savegame']=f.read()
                    f.close()
                except IOError:
                    result['savegame']=None
                try:
                    f=open(self.storage_path+user+".xml","rb")
                    result['csv']=f.read()
                    f.close()
                except IOError:
                    result['csv']=None
                try:
                    f=open(self.storage_path+user+'.logged',"rb")
                    result['logged_in_server']=f.read()
                    f.close()
                except IOError:
                    result['logged_in_server']=None
                return result
        except IOError:
            pass
        return None

    def set_connected(self, user, isconnected):
        if not self.check_string(user):
            return
        f=open(self.storage_path+user+'.logged',"wb")
        if isconnected:
            f.write("1")
        f.close()#empty file

class debugcursor:
    def __init__(self,curs):
        self.curs=curs
    def execute(self,query,tup):
        fp = open('/tmp/persistent/vegastrike_forum/debugacct.txt','at')
        try:
            fp.write(str(query%tup))
        except:
            fp.write('Error: '+repr(query)+' % '+repr(tup))
        fp.close()
        self.curs.execute(query,tup)
    def fetchone(self):
        return self.curs.fetchone()

class debugconn:
    def __init__(self,db):
        self.db=db
    def cursor(self,*args):
        return debugcursor(self.db.cursor(*args))

class MysqlDB(DBBase):
    def __init__(self, config, mod):
        DBBase.__init__(self, mod)
        if 1: #try:
            import MySQLdb
            self.conn = MySQLdb.connect(
                    host   = config['host'],
                    port   = int(config.get('port','3306')),
                    passwd = config['passwd'],
                    user   = config['user'],
                    db     = config['db'])
            self.dict_cursor = MySQLdb.cursors.DictCursor
        else: #except:
            self.conn = None
            self.dict_cursor = None
        self.user_table = config.get('user_table', 'accounts')
        self.account_table = config.get('account_table', 'accounts')

        if config.get('create_user',True):
            self.create_user = True
        else:
            self.create_user = False

    def check_password(self, username, password, can_create=False):
        username=username.replace(' ','_')
        c = self.conn.cursor() #self.dict_cursor
        c.execute('SELECT user_id, user_password FROM ' +
                self.user_table + ' WHERE username=%s',
                (username,) )
        result = c.fetchone()
        if result and result[0]:
            return self.compare_password(result[1], password)
        else:
            if self.create_user and can_create:
                maxquery = self.conn.cursor()
                maxquery.execute('SELECT MAX(user_id) FROM ' + self.user_table)
                answer_row = maxquery.fetchone()
                user_id = answer_row[0]+1
                c = self.conn.cursor()
                c.execute('INSERT INTO '+self.user_table +
                        ' (username, user_id, user_password) VALUES ' +
                        ' (%s, '+str(int(user_id))+', %s)',
                        (username, self.hash_password(password)) )
                return True
            else:
                return False

    def save_account(self, username, save, csv):
        #print save
        #print csv
        if not save:
            raise DBError('Empty save file')
        elif not csv:
            raise DBError('Empty csv file')
        c = self.conn.cursor()
        whereadd=''
        username=username.replace(' ','_')
        if self.user_table != self.account_table:
            c.execute('SELECT logged_in_server FROM '+self.account_table +
                    ' WHERE username=%s AND modname=%s',
                    (username, self.modkey))
            row = c.fetchone()
            if not row:
                c.execute('INSERT INTO '+self.account_table +
                        ' (username, modname, csv, savegame, logged_in_server)'+
                        ' VALUES (%s, %s, %s, %s, 0)',
                        (username, self.modkey, csv, save))
            else:
                #print ('UPDATE ' + self.account_table +
                #       ' SET savegame=%s, csv=%s WHERE username=%s AND modname=%s' %
                #       (save, csv, username, self.modkey))
                c.execute('UPDATE ' + self.account_table +
                        ' SET savegame=%s, csv=%s WHERE username=%s AND modname=%s',
                        (save, csv, username, self.modkey))
        else:
            c.execute('UPDATE ' +self.user_table+
                    'SET savegame=%s, csv=%s WHERE username=%s',
                    (save, csv, username))

    def get_login_info(self, username, password):
        username=username.replace(' ','_')
        c = self.conn.cursor(self.dict_cursor)
        if self.user_table != self.account_table:
            if self.check_password(username, password, False):
                c.execute('SELECT logged_in_server, savegame, csv FROM ' +
                        self.account_table + ' WHERE username=%s AND modname=%s',
                        (username,self.modkey))
                ret = c.fetchone()
                if not ret:
                    return {'savegame':None,
                            'csv': None,
                            'logged_in_server':None}
                return ret
        else:
            c.execute('SELECT logged_in_server, user_password, savegame, csv FROM ' +
                    self.user_table + ' WHERE username=%s',
                    (username,))
            result = c.fetchone()
            if (result):
                if self.compare_password(result['user_password'], password):
                    return result
        return None

    def set_connected(self, user, isconnected):
        user=user.replace(' ','_')
        c = self.conn.cursor()
        logged_in_str = '0'
        if isconnected:
            logged_in_str = '1'
        if self.user_table != self.account_table:
            c.execute('UPDATE '+self.account_table+' SET logged_in_server='+
                    logged_in_str+' WHERE username=%s', (user,) )
        else:
            c.execute('UPDATE '+self.user_table+' SET logged_in_server='+
                    logged_in_str+' WHERE username=%s', (user,) )

def connect(config, mod):
    if config['type'] == 'file':
        return FileDB(config, mod)
    elif config['type'] == 'mysql':
        return MysqlDB(config, mod)
    else:
        raise DBError('invalid database type: '+str(dbconfig.type))
