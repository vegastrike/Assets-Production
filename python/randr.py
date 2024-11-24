import subprocess

class Screen:
    resolutions = []
    def __init__(self, index):
        self.index = index
        
    def add_resolution(self, resolution_str):
        if 'x' not in resolution_str:
            return
        
        xy = resolution_str.split('x')
        
        if len(xy) != 2:
            return
        
        self.resolutions.append(xy)
        

def parse_xrandr(input):
    lines = input.split('\n')
    screens = []
    screen = None
    index = 0
    
    for line in lines:
        components = []
        spaces = line.split(' ')
        
        for space in spaces:
            space = space.strip()
            if len(space) > 0:
                components.append(space)
                
        if len(components) < 2:
            continue
        
        if components[0] == 'Screen':
            screen = Screen(index)
            screens.append(screen)
            index += 1
            
        screen.add_resolution(components[0])
        
    return screens

def xrandr():
    cmd = ['/usr/bin/xrandr']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    return (proc.returncode, o.decode('ascii'), e.decode('ascii'))

result = xrandr()
screens = parse_xrandr(result[1])

print(f"Number of monitors: {len(screens)}")
for screen in screens:
    print(f"Screen #{screen.index}")
    for resolution in screen.resolutions:
        print(resolution)
    print('\n')

