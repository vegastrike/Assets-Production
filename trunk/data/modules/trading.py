import vsrandom
import VS
class trading:
  def __init__(self):
    self.last_ship=0
    self.quantity=4
    self.price_instability=0.01
    
  def SetPriceInstability(self, inst):
    self.price_instability=inst
  
  def SetMaxQuantity (self,quant):
    self.quantity=quant
  
  def Execute(self):
    quant = (vsrandom.random()*(self.quantity-1))+1
    un = VS.getUnit (self.last_ship)
    if (un.isNull()):
      self.last_ship=0
    else:
      if (un.isSignificant()):
	player = VS.getPlayer()
	if (player!=un):
	  if (vsrandom.random()<.5):
	    un.incrementCargo(1-(quant*self.price_instability),quant)
	  else:
	    un.decrementCargo(1+(self.price_instability))
      self.last_ship+=1
  
