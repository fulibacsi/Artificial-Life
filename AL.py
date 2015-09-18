# encoding: utf-8
# ----- AL.py -----
#
#  Usage:
#      python AL.py
#
#    A small and simple experiment with simulating artificial life.
#
#          Tested on Windows 7 and Ubuntu environment!
#
# Copyright (C) 2012, András Fülöp, fulibacsi@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:##www.gnu.org/licenses/>.
#

# imports
from al.simulator import Simulator

# hunger function for specifing starvation
def hf(value):
    return value - max(0.1, value * 0.2)


# main function
if __name__ == '__main__':
    # create simulation
    sim = Simulator(
        size=5,
        num_of_resources=10,
        num_of_consumers=10,
        resource_popup=0.2,
        base_hunger=0.4,
        hunger_function=hf,
        seed=42
    )

    # run it as you like
    while ((len(sim.consumers) > 0 and len(sim.consumers) < 100)
           and not (len(sim.consumers) <= 2 and sim.round > 1000)):
        sim.tick()
        sim.report()

    print 'Remaining consumers:'
    print '\n'.join([repr(consumer) for consumer in sim.consumers])
