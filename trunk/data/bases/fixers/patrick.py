import Base
import fixers

fixers.DestroyActiveButtons ()
fixers.CreateChoiceButtons(Base.GetCurRoom(),[
	fixers.Choice("bases/fixers/yes.spr","bases/fixers/patrick2.py","Accept This Agreement"),
	fixers.Choice("bases/fixers/no.spr","bases/fixers/no.py","Decline This Agreement")])
Base.Message("The Centerion is a fine vessel.  Do you really want to buy this ship")
