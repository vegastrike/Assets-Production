import random
import bar_lib
import weapons_lib
import Base
import VS
def MakeLandingAndConcourse (time_of_day='_day'):

    plist=VS.musicAddList('agricultural.m3u')
    VS.musicPlayList(plist)
    new_time_of_day=time_of_day
    if (random.randrange(0,3)==0):
        new_time_of_day='_storm'
    room1 = Base.Room ('Landing Platform')
    room2 = Base.Room ('Main Concourse')
    Base.LaunchPython (room1, 'launch','bases/launch_music.py', -0.666016, -0.361979, 0.791016, 0.205729, 'Launch Your Ship')
    Base.Link (room1, 'Main Concourse', -0.611111, -0.0634573, 1.25278, 0.354486, 'Go To The Main Concourse', room2)
    Base.Texture (room1, 'tex', 'bases/ocean/landing'+new_time_of_day+'.spr', 0, 0)
    Base.Ship (room1, 'ship', (0*2,-.1*2,40),(0,.93,-.34) ,(-1,0,0))
    Base.Comp (room2, 'CargoComputer', -0.306641, -0.263021, 0.105469, 0.420833, 'Cargo Computer', 'BUYMODE SELLMODE')
    Base.Texture (room2, 'tex', 'bases/ocean/concourse'+new_time_of_day+'.spr', 0, 0)
    bar = bar_lib.MakeBar (room2,time_of_day)
    Base.Comp (room2, 'MissionComputer', 0.292969, -0.263021, 0.0878906, 0.420833, 'Mission Computer', 'NEWSMODE MISSIONMODE BRIEFINGMODE')
    Base.Link (room2, 'BarLink', 0.580078, -1, 0.419922, 1.09115, 'Bar', bar)
    weap = weapons_lib.MakeWeapon (room2,time_of_day)
    Base.Link (room2, 'WeaponsRoom', -1, -1, 0.419922, 1.09115, 'Weapons Room', weap)
    Base.Link (room2, 'LandingLink', -1, -1, 2, 0.28125, 'Landing Platform', room1)
    ### MUST BE LAST LINK ###
    return (room1,room2,bar,weap)
