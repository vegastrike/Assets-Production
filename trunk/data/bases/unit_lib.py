import Base
import bar_lib
import weapons_lib
import dynamic_mission

def MakeUnit (bartendername='bases/bartender_default.py'):
    dynamic_mission.CreateMissions()
    room1 = Base.Room ('Landing Platform')
    room2 = Base.Room ('Main Concourse')
    Base.Texture (room1, 'tex', 'bases/generic/base_entrance.spr', 0, 0)
    Base.Texture (room2, 'tex', 'bases/generic/base_concourse.spr', 0, 0)
    Base.Ship (room1, 'ship', (0,-.3*2,2*2),(0,.93,-.34) ,(-1,0,0))
    Base.LaunchPython (room1, 'launch','bases/launch_music.py', -0.841797, -0.859375, 1.5625, 0.565104, 'Launch Your Ship')
    Base.Link (room1, 'Conc', -0.453125, -0.291667, 0.767578, 0.770833, 'Concourse',room2)
    #Base.LaunchPython (room, 'launch','bases/launch_music.py', -0.841797, -0.859375, 1.5625, 0.565104, 'newlaunchlink')
    #Base.Link (room, 'link', -0.453125, -0.291667, 0.767578, 0.770833, 'newgotolink', -842150451)
    bar = bar_lib.MakeBar (room2,'_night',bartendername)
    weap = weapons_lib.MakeWeapon (room2,'_night')
    Base.Link (room2, 'BarLink', -0.669922, -0.721354, 0.292969, 0.403646, 'Bar', bar)
    Base.Link (room2, 'WeaponsRoom', 0.382813, -0.731771, 0.326172, 0.427083, 'Weapons Room', weap)
    Base.Link (room2, 'LandingLink', -0.142578, -0.244792, 0.341797, 0.338542, 'Landing Platform', room1)
    Base.Comp (room2, 'MissionComputer', -0.425781, -0.307292, 0.183594, 0.200521, 'Mission Computer', 'News Missions')
    Base.Comp (room2, 'CargoComputer', 0.289063, -0.283854, 0.146484, 0.179688, 'Cargo Computer', 'Cargo')
    return (room1, room2, bar, weap)
