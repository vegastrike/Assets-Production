import vsrandom
import VS

production={}
def getImports(name,faction):
    try:
        prodlist=[]
        s = VS.LookupUnitStat(name,faction,"Cargo_Import")
        while (len(s)):
            where=s.find("{")
            if (where==-1):
                s=""
                break;
            else:
                s=s[where+1:]
            #print "beg: "+s
            where = s.find("}")
            if (where==-1):
                s=""
                break;
            else:
                tmp=s[:where]
                prodlist.append(tmp.split(";"))
                s=s[where+1:]
                if (len(prodlist[-1])>4):
                    try:
                        prodlist[-1][1]=float(prodlist[-1][1])
                    except:
                        prodlist[-1][1]=0.0
                    try:
                        prodlist[-1][2]=float(prodlist[-1][2])
                    except:
                        prodlist[-1][2]=0.0
                    try:
                        prodlist[-1][3]=float(prodlist[-1][3])
                    except:
                        prodlist[-1][3]=0.0
                    try:
                        prodlist[-1][4]=float(prodlist[-1][4])
                    except:
                        prodlist[-1][4]=0.0
                #print "rest "+s
        print "whole list: " +str(prodlist)
        return prodlist
    except:
        import sys
        print "GetImportFailure"
        print str(sys.exc_info()[0])+str(sys.exc_info()[1])
    return []
class trading:
    def __init__(self):
        self.last_ship=0
        self.quantity=4
        self.price_instability=0.01
        self.count=0
    def SetPriceInstability(self, inst):
        self.price_instability=inst
      
    def SetMaxQuantity (self,quant):
        self.quantity=quant
      
    def Execute(self):
        self.count+=1
        if (self.count<3):
            return
        self.count=0
        quant = (vsrandom.random()*(self.quantity-1))+1
        un = VS.getUnit (self.last_ship)
        if (un.isNull()):
            self.last_ship=0
        else:
            if (un.isSignificant()):
                if (un.isPlayerStarship()==-1):
                    global production
                    name = un.getName()
                    faction= un.getFactionName()
                    if un.isPlanet():
                        name = un.getFullname();
                        faction="planets"
                    prad=production.get((name,faction))
                    if None==prad:
                        prad= getImports(name,faction)
                        production[(name,faction)]=prad
                    if len(prad):
                        prod=prad[vsrandom.randrange(0,len(prad))]
                        cargo=VS.getRandCargo(int(prod[3]+prod[4]),prod[0])
                        if (cargo.GetCategory()==prod[0]):
                            removeCargo=False
                            if (prod[3] or prod[4]):
                                ownedcargo=un.GetCargo(cargo.GetContent())
                                quant=ownedcargo.GetQuantity()
                                #if un.getName()=="mining_base" and (cargo.GetContent()=="Tungsten" or cargo.GetContent()=="Space_Salvage"):
                                #    print "Mining "+str(quant)+" from "+str(prod[3])+" to "+str(prod[4])
                                if (quant<prod[3]-prod[4] or quant==0):
                                    quant=int(prod[3]+vsrandom.uniform(-1,1)*prod[4])
                                    #if un.getName()=="mining_base" and (cargo.GetContent()=="Tungsten" or cargo.GetContent()=="Space_Salvage"):                                   
                                    #    print "Will add quant "+str(quant)
                                    if (quant>0):
                                        cargo.SetQuantity(quant)
                                        price = prod[1]+vsrandom.uniform(-1,1)*prod[2]
                                        cargo.SetPrice(cargo.GetPrice()*price)
                                        print " adding "+str(quant)+" of "+cargo.GetContent()+" cargo for "+str(price)
                                        un.addCargo(cargo)
                                    else:
                                        removeCargo=True
                                elif quant>prod[3]+prod[4]:
                                   removeCargo=True
                            else:
                                removeCargo=True
                            if removeCargo:
                                ownedcargo=un.GetCargo(cargo.GetContent())
                                if (ownedcargo.GetQuantity()):
                                    print "Removing one "+ownedcargo.GetContent()
                                    
                                    un.removeCargo(ownedcargo.GetContent(),ownedcargo.GetQuantity()/3+1,0)
            self.last_ship+=1
        
