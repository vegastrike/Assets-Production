import VS
import sys
import aitest
#class MyAI(VS.CommAI):
#    def Execute(self):
#        sys.stdout.write('MyAI\\n')
#        return ''
print sys.path
#Set up output redirection
hi2 = aitest.MyAI()
hi1 = VS.CommAI()
print hi1.Execute()
print hi1.Execute()
print hi1.Execute()
print hi2.Execute()
print hi2.Execute()
print hi2.Execute()
