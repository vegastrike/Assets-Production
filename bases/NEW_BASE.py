import Base

room = Base.Room ('Pool')
Base.Launch (room, 'Launch', -0.1, 0.25, 0.2, 0.268229, 'Launch')
Base.Link (room, 'Concourse', -0.310547, -0.078125, 0.638672, 0.273438, 'Concourse', 2)
Base.Texture (room, 'tex', 'bases/carribean/relax.spr', 0, 0)
Base.Ship (room, 'ship', (0,0.194,8), (1, 0, 0), (0, 0.9, -0.15))

room = Base.Room ('Bar')
Base.Python (room, 'talk', -0.669922, -0.119792, 0.4, 0.4, 'Talk to the Bartender', 'bases/bartender.py')
Base.Link (room, 'Concourse', 0.34375, -0.557292, 0.654297, 1.3151, 'Concourse', 2)
Base.Link (room, 'Concourse', -0.123047, -0.0807292, 0.164063, 0.601563, 'Concourse', 2)
Base.Texture (room, 'tex', 'bases/carribean/bar.spr', 0, 0)
Base.Texture (room, 'bartender', 'bases/generic/bartender0.spr', -0.469922, 0.080208)

room = Base.Room ('Concourse')
Base.Comp (room, 'cargcomp', -0.755859, -0.450521, 0.253906, 0.471354, 'Hardware Purchases/Sales', 'BuyMode SellMode ShipMode UpgradeMode DowngradeMode ')
Base.Comp (room, 'misscomp', 0.458984, -0.414063, 0.232422, 0.505208, 'Mission Computer', 'NewsMode MissionMode BriefingMode ')
Base.Link (room, 'bar', -0.232422, -0.447917, 0.431641, 0.442708, 'Bar', 1)
Base.Link (room, 'Pool', -0.996094, -0.994792, 1.99219, 0.309896, 'Pool', 0)
Base.Texture (room, 'tex', 'bases/carribean/concourse.spr', 0, 0)

