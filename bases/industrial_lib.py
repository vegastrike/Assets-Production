import Base
import weapons_lib
import vsrandom
import VS
def MakeCorisc(time_of_day='day',mybartender='bases/bartender_default.py'):
    plist=VS.musicAddList('industrial.m3u')
    VS.musicPlayList(plist)    

    room1 = Base.Room ('Landing Platform')
    Base.Texture (room1, 'tex', 'bases/industrial/landing'+time_of_day+'.spr', 0, 0)
    bar = Base.Room ('Bar')
    Base.Texture (bar, 'tex', 'bases/industrial/bar'+time_of_day+'.spr', 0, 0)
    Base.Link (bar, 'Exlink1', -1, -1, 0.466797, 2, 'Exit The Bar', 0)
    Base.Link (bar, 'Exlink2', -1, -0.200521, 1, 1.200521, 'Exit The Bar', 0)
    Base.Python (bar, 'talk', 0.46875, -0.151042, 0.4, 0.4, 'Talk to the Bartender', mybartender)
    Base.Texture(bar,'bartender','bases/industrial/bartender%d.spr' % (vsrandom.randrange(0,4)),0.66875, 0.048958)
    weap = weapons_lib.MakeWeapon (room1,time_of_day)
    if (time_of_day=='_day'):
        Base.Comp (room1, 'CargoComputer', -0.476563, -0.705729, 0.0664063, 0.200521, 'Cargo Computer', 'BUYMODE SELLMODE')
        Base.Comp (room1, 'MissionComputer', 0.300781, -0.695313, 0.0800781, 0.195313, 'Mission Computer', 'NEWSMODE MISSIONMODE BRIEFINGMODE')
        Base.Ship (room1, 'ship', (-0.02539065*2,-0.4254165*2,4.5), (0,.9,-.13), (.5,.13,.8))
        Base.Link (room1, 'BarLink', -0.347656, -0.335938, 0.144531, 0.195313, 'Bar', bar)
        Base.Link (room1, 'WeapLink', 0.152344, -0.40625, 0.294922, 0.361979, 'Weapons Room', weap)
        Base.LaunchPython (room1, 'launch','bases/launch_music.py', -0.369844, -0.997396, 0.638672, 0.40625, 'Launch Your Ship')
    else:
        Base.Comp (room1, 'comp', -0.900391, -0.848958, 0.136719, 0.411458, 'Computer', 'BuyMode SellMode NewsMode MissionMode BriefingMode')
        Base.Ship (room1, 'ship', (0.0539065*2,-0.3354165*2,2), (0,1,0), (.5,0,.86))
        Base.Link (room1, 'BarLink', -0.558594, -0.151042, 0.275391, 0.242188, 'Bar', bar)
        Base.Link (room1, 'WeapLink', 0.3125, -0.0963542, 0.681641, 0.333333, 'Weapons Room', weap)
        Base.LaunchPython (room1, 'launch','bases/launch_music.py', -0.492188, -1, 0.982422, 0.625, 'Launch Your Ship')
    return (room1,bar,weap)
