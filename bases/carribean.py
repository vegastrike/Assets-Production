import Base
import random
import VS
plist=VS.musicAddList('carribean.m3u')
VS.musicPlayList(plist)    

time_of_day='_day'

#landing = Base.Room ('Landing Platform')
#Base.Texture (landing, 'tex', 'bases/carribean/landing.spr', 0, 0)
relax = Base.Room ('Pool')
Base.Texture (relax, 'tex', 'bases/carribean/relax.spr', 0, 0)
Base.Ship (relax, 'ship', (0,.388,8), (0,.9,-.15), (1,0,0))
Base.Launch (relax, 'Launch', -0.1, 0.25, 0.2, 0.268229, 'Launch')
bar = Base.Room ('Bar')
Base.Texture (bar, 'tex', 'bases/carribean/bar.spr', 0, 0)
Base.Texture (bar,'bartender','bases/generic/bartender%d.spr' % (random.randrange(0,4)), -0.469922, 0.080208)
Base.Python (bar, 'talk', -0.669922, -0.119792, 0.4, 0.4, 'Talk to the Bartender', 'bases/bartender_carribean.py')
concourse = Base.Room ('Concourse')
Base.Texture (concourse, 'tex', 'bases/carribean/concourse.spr', 0, 0)
Base.Comp (concourse, 'cargcomp', -0.755859, -0.450521, 0.253906, 0.471354,  'Hardware Purchases/Sales', 'BuyMode SellMode ShipMode UpgradeMode DowngradeMode')
Base.Comp (concourse, 'misscomp', 0.458984, -0.414063, 0.232422, 0.505208, 'Mission Computer', 'NewsMode MissionMode BriefingMode')
Base.Link (concourse, 'bar', -0.232422, -0.447917, 0.431641, 0.442708, 'Bar', bar)
Base.Link (concourse, 'Pool', -0.996094, -0.994792, 1.99219, 0.309896, 'Pool', relax)
Base.Link (relax, 'Concourse', -0.310547, -0.078125, 0.638672, 0.273438, 'Concourse', concourse)
Base.Link (bar, 'Concourse', 0.34375, -0.557292, 0.654297, 1.3151, 'Concourse', concourse)
Base.Link (bar, 'Concourse', -0.123047, -0.0807292, 0.164063, 0.601563,'Concourse',concourse)


