import random
import VS
class trading:
  quantity=4
  last_ship=0
  price_instability=0.01
  def __init__(self):
    pass #does nothing; all variables are set in the 3 lines above
  
  def SetPriceInstability(self, inst):
    self.price_instability=inst
  
  def SetMaxQuantity (self,quant):
    self.quantity=quant
  
  def Execute(self):
    quant = (random.random()*(self.quantity-1))+1
    un = VS.getUnit (self.last_ship)
    if (un.isNull()):
      self.last_ship=0
    else:
      if (un.isSignificant()):
	player = VS.getPlayer()
	if (player!=un):
	  if (random.random()<.5):
	    un.incrementCargo(1-(quant*self.price_instability),quant)
	  else:
	    un.decrementCargo(1+(quant*self.price_instability),quant)
      self.last_ship+=1
  
