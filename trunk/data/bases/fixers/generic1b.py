import fixers
import mission_lib
import VS

fixers.DestroyActiveButtons ()
if VS.numActiveMissions()>1:
	Base.Message('You are already doing a mission. Finish that instead.')
else:
	mission_lib.BriefLastMission(1,1)
	VS.LoadMission('mission/internal2.mission')