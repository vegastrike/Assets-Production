#---------------------------------------------------------------------------------
# Vega Strike script for a quest
# Copyright (C) 2008-2025 The vsUTCS Contributors
# Contact: maintainers@vega-strike.org
# Internet: https://github.com/vegastrike/Assets-Production
#.
# This file is part of Vega Strike: Upon the Coldest Sea ("vsUTCS").
#
# vsUTCS is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# vsUTCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Vega Strike.  If not, see <https://www.gnu.org/licenses/>.
#
# Description: AI for VS units - escort and patrol
# Author: pyramid
# Version: 2008-04-23
#
#---------------------------------------------------------------------------------

import VS
import Vector
import unit

class ai_escortpatrol(VS.PythonAI):

    def init(self,un):
        self.timer = VS.GetGameTime()
        self.target = self.GetParent().GetTarget()
        self.GetParent().setSpeed(100)
        # calculate required thrust factor as an approximate relation of mass to reference mass
        # found empirically, since thrust values are not read from the model
        self.thrustfactor = self.GetParent().GetMass()/50

    # things that could be improved
    # (a) add lateral thrus to compensate drift when changing direction
    # (b) if possible, make patrol radius and max velocity configurable
    def Execute(self):
        import unit
        import Vector
        import vsrandom
        VS.PythonAI.Execute(self);
        distance = abs(self.GetParent().getDistance(self.target))

        # evade the target and almost parallel flyby
        if (distance<=2000 and VS.GetGameTime()>self.timer):
            angle = unit.facingAngleToUnit(self.GetParent(),self.target)
            velocity = unit.getSignedVelocity(self.GetParent())
            if (angle<0.30):
                angular = 0.80-angle
                change  = (vsrandom.uniform(-angular,angular),
                            vsrandom.uniform(angular,angular),
                            vsrandom.uniform(-angular,angular))
                self.GetParent().SetAngularVelocity(change)
            if (velocity<100):
                self.GetParent().LongitudinalThrust(100)
            self.timer = VS.GetGameTime()+1

        # patrol in random direction
        if (distance>2000 and distance<7000 and VS.GetGameTime()>self.timer):
            angular = vsrandom.uniform(0.01,0.10)
            change  = (vsrandom.uniform(-angular,angular),
                        vsrandom.uniform(angular,angular),
                        vsrandom.uniform(-angular,angular))
            self.GetParent().SetAngularVelocity(change)
            velocity = unit.getSignedVelocity(self.GetParent())
            if (velocity<100):
                self.GetParent().LongitudinalThrust(200)
            self.timer = VS.GetGameTime()+2

        # return to target proximity
        if (distance>=7000 and VS.GetGameTime()>self.timer):
            # calculates the angular velocity required to turn back on target
            vec = Vector.Sub(self.GetParent().Position(),self.target.Position())
            change = Vector.Cross(Vector.SafeNorm(self.GetParent().GetOrientation()[2]),Vector.SafeNorm(vec))
            self.GetParent().SetAngularVelocity(change)
            # calculate the required thrust depending on mass and
            # signed velocity magnitude as result of momentum
            velocity = unit.getSignedVelocity(self.GetParent())
            if (velocity<100):
                if (velocity<0):
                    # thrust more while not flying forward
                    thrust = self.thrustfactor * max(abs(velocity),300)
                else:
                    thrust = self.thrustfactor * 300
                self.GetParent().LongitudinalThrust(thrust)
            self.timer = VS.GetGameTime()+1
        return 1

hi1 = ai_escortpatrol()
#print 'AI creation successful: ai_escortpatrol'
#hi1 = 0
