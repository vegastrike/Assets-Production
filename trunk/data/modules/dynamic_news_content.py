def allFactionNames():
# returns a dictionary containing all the variations on faction names known to man
	return {
"alltags" :
["full","nick","government","posessive","homeworld"]

,"confed" :	{"full" : "Confederation of Inhabited Worlds"
		,"nick" : "Confed"
		,"government" : "Confederate Senate"
		,"posessive" : "Confederate"
		,"homeworld" : "Earth"
		}

,"aera" :	{"full" : "Aeran Empire"
		,"nick" : "Aera"
		,"government" : "Aera Oligarchy"
		,"posessive" : "Aeran"
		,"homeworld" : "Aeneth"
		}

,"rlaan" :	{"full" : "Rlaan Empire"
		,"nick" : "Rlaan"
		,"government" : "Rlaan Assembly"
		,"posessive" : "Rlaan"
		,"homeworld" : "Rlaa"
		}

,"pirates" :	{"full" : "Various Pirate Factions"
		,"nick" : "Pirates"
		,"government" : "Pirate Factions"
		,"posessive" : "Pirate's"
		,"homeworld" : "the pirates' homeworld"
		}

,"ISO" :	{"full" : ""
		,"nick" : "ISO"
		,"government" : ""
		,"posessive" : ""
		,"homeworld" : ""
		}
}


def allNews():
# returns a dictionary containing all the dynamic news items in existancs ;-)
	return	{

"neutral" :

{"siege" :	{"start"	:{"success":	{"good"		: []

						,"bad"		: []

						,"neutral"	: []

						}
				 ,"loss"   :	{"good"		: []

						,"bad"		: []

						,"neutral"	: []

						}
				 }

		,"middle"	:{"success":	{"good"		: []

						,"bad"		: []

						,"neutral"	: []

						}

				 ,"loss"   :	{"good"		: []

						,"bad"		: []

						,"neutral"	: []

						}
				 }
		
		,"end"		:{"success":	{"good"		: [(0.8,"all","VAR_aggressor_posessive forces have experienced a moral boosting victory today in the VAR_system_system system.  The blockade in the VAR_defender_posessive system ended today, three weeks after it began, with all VAR_defender_posessive supplies exhausted.  No information on the state of the infrastructure, or of casualties is as of yet available.")
								  ]

						,"bad"		: [(0.3,"all","An end to the VAR_aggressor_full 's barbaric siege in the VAR_defender_posessive system VAR_system_system in the VAR_system_sector sector occured today.  After several weeks of remorseless blockading, no-one was left alive in any critical part of the VAR_defender_posessive defence.  Such an attrocity could only have been wrought by the VAR_aggressor_nick , whose remorseless tactics have seen many wins, to the tunes of thousands of bystanders in a war that may well be going for a long time.  This act has only served to strengthen the resolve of the VAR_dockedat_government on VAR_dockedat_homeworld to boost rescources to the war effort against the VAR_aggressor_full .")
								  ]

						,"neutral"	: [(0.8,"all","The VAR_aggressor_full has greeted the news of their triumph in the siege in VAR_system_sector sector, VAR_system_system against a VAR_defender_posessive position today with barely a murmor.  Just another in a string of minor victories for the VAR_aggressor_nick , and a string of minor losses for the VAR_defender_nick in events which cause barely a murmur in our little corner of the galaxy, especially on VAR_dockedat_homeworld where war news is currently taking a back seat to recent political issues.")
								  ]

						}

				 ,"loss"   :	{"good"		: []

						,"bad"		: [(0.8,"all","VAR_aggressor_posessive forces have lost the battle of wills in the VAR_system_system system today.  After weeks of blockade action, VAR_aggressor_nick forces have conceded that they are unable to stop VAR_defender_posessive forces from resupplying.  \"Their warp technology is simply able to ignore all of our inhibitor technologies.\"")
								  ]

						,"neutral"	: []

						}
				 }


		}
}


,"confed" :
{"siege" :	{"start"	:{"good"	: []

				 ,"bad"		: []

				 ,"neutral"	: []

				}

		,"middle"	:{"good"	: []

				 ,"bad"		: []

				 ,"neutral"	: []

				}
		
		,"end"		:{"good"	: []

				 ,"bad"		: []

				 ,"neutral"	: []

				}

		}



}

,"aera" :	{"start" : {}
		
		,"middle" : {}
		
		,"end" : {}
		}

,"rlaan" :	{"start" : {}
		
		,"middle" : {}
		
		,"end" : {}
		}

,"pirates" :	{"start" : {}
		
		,"middle" : {}
		
		,"end" : {}
		}

,"ISO" :	{"start" : {}
		
		,"middle" : {}
		
		,"end" : {}
		}

}