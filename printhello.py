import AI
import sys
class MyAI(AI.PythonAI):
    def Execute(self):
        AI.PythonAI.Execute(self);
        sys.stdout.write('h')
        return ''
hi1 = MyAI()

print 'AI creation successful'
hi1 = 0
#: 1.7; previous revision: 1.6
