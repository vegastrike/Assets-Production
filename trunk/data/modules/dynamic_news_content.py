def allFactionNames():
# returns a dictionary containing all the variations on faction names known to man
#nicks -> singular
#nickp -> plural
#dnicks -> derogatory nick singular
#dnickp -> derogatory nick plural
	return {
"alltags" :
["full","nicks","nickp","dnicks","dnickp","government","possessive","homeworld"]

,"confed" :	{"full" : "Confederation of Inhabited Worlds"
		,"nicks" : "Confed"
		,"nickp" : "Confed"
		,"dnicks" : "Origami"
		,"dnickp" : "Origamis"
		,"government" : "Confederate Senate"
		,"possessive" : "Confederate"
		,"homeworld" : "Earth"
		}

,"aera" :	{"full" : "Aeran Ascendency"
		,"nicks" : "Aera"
		,"nickp" : "Aera"
		,"dnicks" : "Jingo"
		,"dnickp" : "Jingos"
		,"government" : "Aera Oligarchy"
		,"possessive" : "Aeran"
		,"homeworld" : "Aeneth"
		}

,"rlaan" :	{"full" : "Rlaan Sovereignty"
		,"nicks" : "Rlaan"
		,"nickp" : "Rlaan"
		,"dnicks" : "Four-Facer"
		,"dnickp" : "Four-Facers"
		,"government" : "Rlaan Assembly"
		,"possessive" : "Rlaan"
		,"homeworld" : "Aantlbzz"
		}

,"pirates" :	{"full" : "Various Pirate Factions"
		,"nicks" : "Pirate"
		,"nickp" : "Pirates"
		,"dnicks" : "Space Hyena"
		,"dnickp" : "Space Hyenas"
		,"government" : "Pirate Factions"
		,"possessive" : "Pirate's"
		,"homeworld" : "the pirates' homeworld"
		}

,"ISO" :	{"full" : "Interstellar Socialist Organization"
		,"nicks" : "ISO"
		,"nickp" : "ISO"
		,"dnicks" : "Pinko-Terrorist"
		,"dnickp" : "Pinko-Terrorists"
		,"government" : "Polit Convention"
		,"possessive" : "ISO's"
		,"homeworld" : "Trotsky"
		}

,"rlaan-briin" :{"full" : "Rlaan-Briin"
		,"nicks" : "Briin"
		,"nickp" : "Briin"
		,"dnicks" : "Bucket-Head"
		,"dnickp" : "Bucket-Heads"
		,"government" : "Briin Subordinate Assembly"
		,"possessive" : "Briin"
		,"homeworld" : "Bribztkabr"
		}

,"klk'k" :	{"full" : "Klk'k "
		,"nicks" : "Klk'k"
		,"nickp" : "Klk'k"
		,"dnicks" : "Wisenheimer"
		,"dnickp" : "Wisenheimers"
		,"government" : "Last House"
		,"possessive" : "Klk'k-an"
		,"homeworld" : "Ktah"
		}
}


def allNews():
# returns a dictionary containing all the dynamic news items in existancs ;-)
	return	{

"neutral" :

{"siege" :	{"start"	:{"success":	{"good"		: [(0.8,"all","BLOCKADE!\\The VAR_aggressor_government has openly reported their intent of invasion with VAR_defender_full in the VAR__system_sector Sector today. The VAR_aggressor_possessive forces have strategically blocked all entrance and exit from VAR_system_system and continue a valiant assault upon the planet.")

								  ]

						,"bad"		: [(0.3,"all","VAR_aggressor_nickp Invasion Plans?\\It is a grave day in VAR_system_system today, as the hordes of the VAR_aggressor_full have senselessly commenced bombardments upon a VAR_defender_possessive planet in VAR_system_sector Sector. The inhabitants were doing nothing that would legally provoke hostile actions, yet VAR_aggressor_possessive troops have already begun their invasion procedures. Can anyone stop these cruel, heartless VAR_aggressor_dnickp?")

								  ]

						,"neutral"	: [(0.6,"all","VAR_aggressor_possessive on the Offencive:\\It seems that the VAR_system_system system has struck a nerve with the VAR_aggressor_government. VAR_aggressor_possessive forces recently launched an attack in the system, and met some resistance from the local regiment of VAR_defender_nickp.  However, this resistance appears to be fading. By all accounts it seems that the VAR_aggressor_possessive forces will, in the long run, win.")

								  ]

						}
				 ,"loss"   :	{"good"		: [(0.2,"all","VAR_defender_nickp Repel Attack:\\Moments after their strike began, the forces of the VAR_aggressor_full were crushed from the VAR_system_system system as the VAR_defender_possessive defence held strong.  The VAR_aggressor_government says they have no intention of retreat. Some ask if this is prudent on the part of the VAR_aggressor_nickp to continue such a hopeless campaign.")

								  ]

						,"bad"		: [(0.3,"all","VAR_aggressor_nickp Beaten By VAR_defender_dnickp?\\One simple ambush was all that it took to demolish the VAR_aggressor_possessive forces today in VAR_system_sector. Given the high esteem VAR_aggressor_possessive forces are held in the VAR_dockedat_government, and the fact that this was apparently the beginnings of a full scale assult, this has been a surprising result to all. The VAR_defender_possessive forces defending VAR_system_system, shocked by their sudden reprieve, have now had time to ready their defensive grid, making another attack by the VAR_aggressor_possessive forces a much greater challenge.")

								  ]

						,"neutral"	: [(0.4,"all","VAR_aggressor_nicks and VAR_defender_nicks Sounding-Off:\\Today, the VAR_aggressor_government is quoted \"The VAR_defender_full will feel our full fury in the VAR_system_system system today!\" Ironically, the VAR_aggressor_possessive forces were repelled in their initial attack. The VAR_defender_government has released a statement saying, \"We no longer have any respect for the VAR_aggressor_government, for we cannot bring ourselves to believe that this was their \"full fury\", yet if it was, we give them our full laughter!\"")

								  ]

						}
				 ,"draw"   :	{"good"		: [(0.4,"all","The VAR_defender_full have the VAR_aggressor_dnickp Stumped:\\Deep in the heart of VAR_system_sector Sector, VAR_aggressor_possessive forces have shown their hostile objectives towards VAR_defender_possessive forces in VAR_system_system. Even after this act of hostility, no movement from either side has been reported. Though the VAR_aggressor_government assures the conflict will be swiftly decided, no one can clearly see a victor in this struggle.")

								  ]

						,"bad"		: [(0.5,"all","VAR_defender_dnicks Resistance!\\After a brutal landing the VAR_aggressor_possessive force entered into a deadlock with the local VAR_defender_possessive peace keepers. Both sides show no sign of retreat or advancement. The VAR_aggressor_government seem to have placed a large amount of resources in the secrecy of their actions. The word \"barbaric\" comes to mind when pondering the siege technique of the VAR_aggressive_possessive forces, yet nothing has happened that may lead to a swift end.")

								  ]

						,"neutral"	: [(0.6,"all","VAR_system_system Deadlock:\\The makings of a siege seem to be present in VAR_system_sector Sector. Though neither the VAR_aggressor_possessive forces nor the VAR_defender_nickp have shown any mercy, neither has shown any true hostility. Most first-hand accounts suggest that this is the result of some hot-headed and frustrated commanders on both sides, leading their forces into an engagement that seems to be going nowhere fast.")

								  ]

						}
				 }

		,"middle"	:{"success":	{"good"		: [

								  ]

						,"bad"		: [

								  ]

						,"neutral"	: [

								  ]

						}

				 ,"loss"   :	{"good"		: [

								  ]

						,"bad"		: [

								  ]

						,"neutral"	: [

								  ]

						}
				 ,"draw"   :	{"good"		: [

								  ]

						,"bad"		: [

								  ]

						,"neutral"	: [

								  ]

						}
				 }
		
		,"end"		:{"success":	{"good"		: [(0.7,"all","VAR_aggressor_full Victory in VAR_system_system!\\In yet another event in the VAR_aggressor_possessive-VAR_defender_possessive war, VAR_aggressor_possessive forces have experienced a moral boosting victory today in the VAR_system_system system.  The blockade in the VAR_defender_possessive system ended today, three weeks after it began, with all VAR_defender_possessive supplies exhausted.  No information on the state of the infrastructure, or of casualties is as of yet available.")
								  ]

						,"bad"		: [(0.3,"all","Tragedy in VAR_system_system:\\An end to the VAR_aggressor_full's barbaric siege in the VAR_defender_possessive system VAR_system_system in the VAR_system_sector sector occured today.  After several weeks of remorseless blockading, no-one was left alive in any critical part of the VAR_defender_possessive defence.  Such an attrocity could only have been wrought by the VAR_aggressor_nickp, whose remorseless tactics have seen many wins, with the death of thousands of bystanders in a war that may well be going for a long time.  This act has only served to strengthen the resolve of the VAR_dockedat_government on VAR_dockedat_homeworld to boost rescources to the war effort against the VAR_aggressor_full.")
								  ]

						,"neutral"	: [(0.9,"all","VAR_defender_possessive VAR_system_system -to- VAR_aggressor_possessive VAR_system_system:\\The VAR_aggressor_full has greeted the news of their triumph in the siege in VAR_system_sector sector, VAR_system_system against a VAR_defender_possessive position today with barely a murmor.  Just another in a string of minor victories for the VAR_aggressor_nickp, and a string of minor losses for the VAR_defender_nickp in events which cause barely a murmur in our little corner of the galaxy, especially on VAR_dockedat_homeworld where war news is currently taking a back seat to recent political issues.")

								  ]

						}

				 ,"loss"   :	{"good"		: [(0.5,"all","Relief for VAR_system_system VAR_defender_nicks:\\The brutal VAR_aggressor_possessive siege against the people of the VAR_system_system in VAR_system_sector has finally been broken. VAR_aggressor_nicks forces have been driven out of the system, and are possibly regrouping for a second attack. Relief convoys are racing along a rapid jump circuit to make it to the suffering people there, bringing badly needed processed food, medical supplies, and relief workers.\\Estimates of the economic damage are still underway, but to many of the inhabitants of VAR_system_system who have lost loved ones in the defense or in the VAR_aggressor_possessive bombings, there will be no relief as long as the VAR_aggressor_full continues their brutal campaign.")
								  ]

						,"bad"		: [(0.8,"all","VAR_aggressor_possessive Withdrawal from VAR_system_system:\\VAR_aggressor_possessive forces have lost the battle of wills in the VAR_system_system system today.  After weeks of blockade action, VAR_aggressor_nicks forces have conceded that they are unable to stop VAR_defender_possessive forces from resupplying.  \"Their warp technology is simply able to ignore all of our inhibitor technologies.\"")
								  ]

						,"neutral"	: [(0.8,"all","VAR_aggressor_possessive VAR_system_sector Sector Jitters:\\The VAR_defender_possessive defenders of VAR_system_system in the VAR_system_sector have defeated the attacking forces of the VAR_aggressor_full. Local military units, who bore the brunt of the VAR_aggressor_possessive onslaught, have requested additional support in the VAR_defender_nicks -- VAR_aggressor_nicks war. The commander of militia forces in VAR_system_system has stated that the recent siege is a sign that the VAR_system_system is one of the systems being targeted by the VAR_aggressor_possessive military in the VAR_system_sector Sector conflict, and that more military support from the VAR_defender_government would be a wise decision.")
								  ]

						}

				,"draw"   :	{"good"		: [(0.8,"all","draw is good")
								  
								  ]

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