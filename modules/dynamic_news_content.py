def allFactionNames():
# returns a dictionary containing all the variations on faction names known to man
#nicks -> singular
#nickp -> plural
#dnicks -> derogatory nick singular
#dnickp -> derogatory nick plural
	return {
"alltags" :
["full","nicks","nickp","dnicks","dnickp","government","posessive","homeworld"]

,"confed" :	{"full" : "Confederation of Inhabited Worlds"
		,"nicks" : "Confed"
		,"nickp" : "Confed"
		,"dnicks" : "Origami"
		,"dnickp" : "Origamis"
		,"government" : "Confederate Senate"
		,"posessive" : "Confederate"
		,"homeworld" : "Earth"
		}

,"aera" :	{"full" : "Aeran Ascendency"
		,"nicks" : "Aera"
		,"nickp" : "Aera"
		,"dnicks" : "Jingo"
		,"dnickp" : "Jingos"
		,"government" : "Aera Oligarchy"
		,"posessive" : "Aeran"
		,"homeworld" : "Aeneth"
		}

,"rlaan" :	{"full" : "Rlaan Sovereignty"
		,"nicks" : "Rlaan"
		,"nickp" : "Rlaan"
		,"dnicks" : "Four-Facer"
		,"dnickp" : "Four-Facers"
		,"government" : "Rlaan Assembly"
		,"posessive" : "Rlaan"
		,"homeworld" : "Aantlbzz"
		}

,"pirates" :	{"full" : "Various Pirate Factions"
		,"nicks" : "Pirate"
		,"nickp" : "Pirates"
		,"dnicks" : "Space Hyena"
		,"dnickp" : "Space Hyenas"
		,"government" : "Pirate Factions"
		,"posessive" : "Pirate's"
		,"homeworld" : "the pirates' homeworld"
		}

,"ISO" :	{"full" : "Interstellar Socialist Organization"
		,"nicks" : "ISO"
		,"nickp" : "ISO"
		,"dnicks" : "Pinko-Terrorist"
		,"dnickp" : "Pinko-Terrorists"
		,"government" : "Polit Convention"
		,"posessive" : "ISO's"
		,"homeworld" : "Trotsky"
		}

,"rlaan-briin" :{"full" : "Rlaan-Briin"
		,"nicks" : "Briin"
		,"nickp" : "Briin"
		,"dnicks" : "Bucket-Head"
		,"dnickp" : "Bucket-Heads"
		,"government" : "Briin Subordinate Assembly"
		,"posessive" : "Briin"
		,"homeworld" : "Bribztkabr"
		}

,"klk'k" :	{"full" : "Klk'k "
		,"nicks" : "Klk'k"
		,"nickp" : "Klk'k"
		,"dnicks" : "Wisenheimer"
		,"dnickp" : "Wisenheimers"
		,"government" : "Last House"
		,"posessive" : "Klk'k-an"
		,"homeworld" : "Ktah"
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
				 ,"draw"   :	{"good"		: []

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
				 ,"draw"   :	{"good"		: []

						,"bad"		: []

						,"neutral"	: []

						}
				 }
		
		,"end"		:{"success":	{"good"		: [(0.7,"all","In yet another event in the VAR_aggressor_posessive-VAR_defender_posessive war, VAR_aggressor_posessive forces have experienced a moral boosting victory today in the VAR_system_system system.  The blockade in the VAR_defender_posessive system ended today, three weeks after it began, with all VAR_defender_posessive supplies exhausted.  No information on the state of the infrastructure, or of casualties is as of yet available.")
								  ]

						,"bad"		: [(0.3,"all","An end to the VAR_aggressor_full's barbaric siege in the VAR_defender_posessive system VAR_system_system in the VAR_system_sector sector occured today.  After several weeks of remorseless blockading, no-one was left alive in any critical part of the VAR_defender_posessive defence.  Such an attrocity could only have been wrought by the VAR_aggressor_nickp, whose remorseless tactics have seen many wins, with the death of thousands of bystanders in a war that may well be going for a long time.  This act has only served to strengthen the resolve of the VAR_dockedat_government on VAR_dockedat_homeworld to boost rescources to the war effort against the VAR_aggressor_full.")
								  ]

						,"neutral"	: [(0.9,"all","The VAR_aggressor_full has greeted the news of their triumph in the siege in VAR_system_sector sector, VAR_system_system against a VAR_defender_posessive position today with barely a murmor.  Just another in a string of minor victories for the VAR_aggressor_nickp, and a string of minor losses for the VAR_defender_nickp in events which cause barely a murmur in our little corner of the galaxy, especially on VAR_dockedat_homeworld where war news is currently taking a back seat to recent political issues.")

								  ]

						}

				 ,"loss"   :	{"good"		: [(0.5,"all","The brutal VAR_aggressor_posessive siege against the people of the VAR_system_system in VAR_system_sector has finally been broken. VAR_aggressor_nicks forces have been driven out of the system, and are possibly regrouping for a second attack. Relief convoys are racing along a rapid jump circuit to make it to the suffering people there, bringing badly needed processed food, medical supplies, and relief workers. Estimates of the economic damage are still underway, but to many of the inhabitants of VAR_system_system who have lost loved ones in the defense or in the VAR_aggressor_posessive bombings, there will be no relief as long as the VAR_aggressor_full continues their brutal campaign.")
								  ]

						,"bad"		: [(0.8,"all","VAR_aggressor_posessive forces have lost the battle of wills in the VAR_system_system system today.  After weeks of blockade action, VAR_aggressor_nicks forces have conceded that they are unable to stop VAR_defender_posessive forces from resupplying.  \"Their warp technology is simply able to ignore all of our inhibitor technologies.\"")
								  ]

						,"neutral"	: [(0.8,"all","The VAR_defender_posessive defenders of VAR_system_system in the VAR_system_sector have defeated the attacking forces of the VAR_aggressor_full. Local military units, who bore the brunt of the VAR_aggressor_posessive onslaught, have requested additional support in the VAR_defender_nicks -- VAR_aggressor_nicks war. The commander of militia forces in VAR_system_system has stated that the recent siege is a sign that the VAR_system_system is one of the systems being targeted by the VAR_aggressor_posessive military in the VAR_system_sector Sector conflict, and that more military support from the VAR_defender_government would be a wise decision.")
								  ]

						}

				,"draw"   :	{"good"		: [(0.8,"all","draw is good")]#FIXED by hellcatv...sytnax error

						,"bad"		: [(0.8,"all","draw is bad")]

						,"neutral"	: [(0.8,"all","draw is neutral")]

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