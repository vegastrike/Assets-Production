import VS
import sys
import printhello
#class MyAI(VS.CommAI):
#    def Execute(self):
#        sys.stdout.write('MyAI\\n')
#        return ''
print sys.path
#Set up output redirection
hi2 = printhello.MyAI()
hi1 = VS.PythonAI()
print hi1.Execute()
print hi1.Execute()
print hi1.Execute()
print hi2.Execute()
print hi2.Execute()
print hi2.Execute()
#test of the meer
