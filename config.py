import VS
import sys

vsio = VS.IO()
vsio.write('beat 0')
sys.stdout = vsio
sys.stderr = vsio

VS.Var.testar="3"
print(vsio.write)
print(VS.Var.__setattr__)
print(VS.Var().testar)

