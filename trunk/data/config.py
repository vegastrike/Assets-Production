import VS
import sys

vsio = VS.IO()
vsio.write('beat 0')
sys.stdout = vsio
sys.stderr = vsio
VS.Var.testar="3"
