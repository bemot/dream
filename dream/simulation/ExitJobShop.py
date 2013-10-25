# ===========================================================================
# Copyright 2013 University of Limerick
#
# This file is part of DREAM.
#
# DREAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DREAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DREAM.  If not, see <http://www.gnu.org/licenses/>.
# ===========================================================================
'''
Created on 2 oct 2012

@author: George
'''
'''
extends the Exit object so that it can act as a jobshop station. Preceding station is read from the Entity
'''

from SimPy.Simulation import Process, Resource
from SimPy.Simulation import activate, passivate, waituntil, now, hold

from Exit import Exit

#the ExitJobShop object
class ExitJobShop(Exit):
    
    #checks if the Exit can accept an entity and there is an entity waiting for it
    def canAcceptAndIsRequested(self):
        if self.getGiverObject():
            return self.getGiverObject().haveToDispose(self)
        else:
            return False

    #get the giver object in a getEntity transaction.       
    def getGiverObject(self):
        from Globals import G
        #loop through the objects to see if there is one that holds an Entity requesting for current object
        for obj in G.ObjList:
            if len(obj.getActiveObjectQueue())>0 and (obj!=self) and now()!=0:
                activeEntity=obj.getActiveObjectQueue()[0]
                if activeEntity.remainingRoute[0][0]==self.id:
                    return obj
        return None        
        