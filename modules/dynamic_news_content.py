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
		,"nickp" : "Confeds"
		,"dnicks" : "Origami"
		,"dnickp" : "Origamis"
		,"government" : "Confederate Senate"
		,"possessive" : "Confederate"
		,"homeworld" : "Earth"
		}

,"merchant" :	{"full" : "Merchant Union"
		,"nicks" : "trader"
		,"nickp" : "traders"
		,"dnicks" : "pill popper"
		,"dnickp" : "pill poppers"
		,"government" : "Merchant Union Council"
		,"possessive" : "Merchant"
		,"homeworld" : "Earth"
		}

,"militia" :	{"full" : "Confederate Police Force"
		,"nicks" : "police"
		,"nickp" : "police"
		,"dnicks" : "space copper"
		,"dnickp" : "space coppers"
		,"government" : "High Commission"
		,"possessive" : "militia"
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

						,"bad"		: [(0.3,"all","VAR_aggressor_nickp Beaten By VAR_defender_dnickp?\\One simple ambush was all that it took to demolish the VAR_aggressor_possessive forces today in VAR_system_sector. Given the high esteem VAR_aggressor_possessive forces are held in the VAR_dockedat_government, and the fact that this was apparently the beginnings of a full scale assult, this has been a surprising result to all. The VAR_defender_possessive forces defending VAR_system_system, shocked by their sudden reprieve, have now had time to ready their defensive grid, making another attack by the VAR_aggressor_possessive forces a much greater challenge."),(0.3,"all","startONE"),(0.3,"all","startTWO"),(0.3,"all","startTHREE"),(0.3,"all","startFOUR"),(0.3,"all","startFIVE")

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
		
		,"end"		:{"success":	{"good"		: [(0.7,"all","VAR_aggressor_full Victory in VAR_system_system!\\In yet another event in the VAR_aggressor_possessive-VAR_defender_possessive war, VAR_aggressor_possessive forces have experienced a moral boosting victory today in the VAR_system_system system.  The blockade in the VAR_defender_possessive system ended today, three weeks after it began, with all VAR_defender_possessive supplies exhausted.  No information on the state of the infrastructure, or of casualties is as of yet available."),(0.7,"all","endONE"),(0.7,"all","endTWO"),(0.7,"all","endTHREE"),(0.7,"all","endFOUR"),(0.7,"all","endFIVE")
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

,"battle" :	{"end" :	{"success" :	{"good"		: [(0.1,"all","VAR_defender_dnickp Vaporised!\\In the outer regions of the VAR_system_system system today, the VAR_aggressor_FG squadron of VAR_aggressor_nicks VAR_aggressor_FGtype ships in transit came across a group of VAR_defender_possessive VAR_defender_FGtype fighters on an intercept course with a VAR_aggressor_possessive passenger liner.  The hostiles were engaged and swiftly destroyed by the VAR_aggressor_FGtype squadron -- no energy sources remained active.")
										  ,(0.3,"player","VAR_aggressor_FG Hero!\\Once again VAR_aggressor_FG, in a VAR_aggressor_FGtype has struck a blow for the VAR_dockedat_full with yet another VAR_defender_possessive flightgroup, this time the VAR_defender_FG Squadran of VAR_defender_FGtype craft, destroyed.  With the war against the VAR_defender_full beginning to drag out, it is people like this hero who will make the difference.  Only with the determination and the will of the people can we ever hope to rid our corner of the galaxy of the VAR_defender_dnicks for good.\\\\\\GNN - In our special report tonight, learn about the VAR_defender_possessive parents who used their own children as shields against VAR_dockadat_nicks troopers.")
										  ]
						,"bad"		: [(0.3,"player","VAR_aggressor_FG Strikes Civilian Transport!\\The VAR_aggressor_FGtype mercillessly struck down the VAR_defender_FG VAR_defender_FGtype in a surprise raid.  The flightgroup was carrying VAR_defender_nicks tourists, and antiquities on an intersystem taxi service when, without warning, the VAR_aggressor_FGtype swooped in and launched several blasts which destroyed the ships instantly.\\Such an attack is characteristic of the VAR_aggressor_full and their allies, using mercenaries and bounty hunters to terorrise the civilian populations of the VAR-defender_full.  VAR_aggressor_FG in particular is well known for utter contempt for life.")]
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		}


,"fleetbattle":	{"start" :	{"success" :	{"good"		: [(0.3,"all","The VAR_aggressor_FG Storms the VAR_defender_nickp:\\Moments ago out of the window of my pleasure yacht I witnessed one of the most impressive sights of my career.  The VAR_aggressor_FGtype Class VAR_aggressor_possessive ship VAR_aggressor_FG and support warped right into the middle of a large VAR_defender_possessive VAR_defender_FGtype led invasion force!\\From the few moments I saw (out pilot was heeding the advice of the VAR_aggressor_FG and getting out of there as fast as possible) the VAR_defender_dnicks were taken completely by surprise with somewhere near half of their fleet badly damaged before the VAR_aggressor_nicks forces had gone out of range.  Information on the outcome of the battle will be available later, when out pilot deems it safe to go investigating closer\\\\Daneel Aleki, GNN")]
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}

		,"middle" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		,"end" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		}

,"destroyed":	{"end" :	{"success" :	{"good"		: [(0.4,"all","Departed Heroes:\\Tragically, the VAR-defender_FG squadron, comprised mainly of VAR_defender_FGtype fighters have been killed in battle today.  A squadron with a more distinguished career would be hard to find in the VAR-defender_possessive forces, with contributions to many of the great battles of this war.\\Their lead commander Jameson was quoted recently saying \"When a pilot goes into battle if he clears his mind of all things, there is a good chance he will come out of it alive.  If he does not, he risks being distracted and hesitating.  In space, hesitation is death.\"")
								  ,(0.4,"player","Freelancer Helps the Cause!\\The VAR_aggressor_FG squardon can add yet another kill to their belts today, as they made short work of the VAR_defender_possessive squadron VAR_defender_FG (of type VAR_defender_FGtype) in VAR_system_system system.  VAR_aggressor_FG has been one of the more prominent of the freelance mercenaries, helping the VAR_dockedat_possessive forces and out allies with many of the smaller scale attacks while the majority of our forces have been engaged on the frontlines.  It is people like these that allow most of us to continue with out lives in peace.")
								  ]
						,"bad"		: [(0.4,"all","VAR_defender_dnicks Vaporised!\\The VAR_defender_possessive squadron of VAR_defender_FGtype VAR_defender_FG has been obliterated today.  The VAR_defender_dnickp have been disrupting both civilian and military operations around VAR_system_system in the VAR_system_sector Sector, and their destruction is sure to be a boon for all operators in the area.  This writer just wishes this type of thing would occur more often.")
								  ,(0.4,"player","VAR_aggressor_FG Scurge Strikes Again!\\This time in a VAR_aggressor_FGtype ship, this mercenary group destroyed yet another VAR_defender_nicks squadron, this time the VAR_defender_FG.  One of the VAR_defender_nickp less experienced groups of VAR_defender_FGtype, they battled corageously but were overwhelmed by the VAR_aggressor_possessive forces.  May they rest in peace, these brave heroes of the VAR_defender_full.")
								  ]
						,"neutral"	: [(0.5,"all","VAR_defender_FG Destroyed:\\The squadron of mainly VAR_defender_FGtype ships was destroyed today in the VAR_system_system system.  More afraid of VAR_dockedat_possessive forces than we were of them, their destruction will not affect business in the area, let alone on VAR_docketat_homeworld.")
								  ,(0.5,"player","VAR_defender_FG Destroyed by VAR_aggressor_FG:\\The pilots of VAR_defender_FG saw their last meal earlier today, oblivious their later fate.  The VAR_defender_FG has been wreaking havok in and around VAR_system_system system lately, disrupting much of the VAR_defender_possessive activity.  Such an event however is relatively commonplace these days, and does not do much to upset the lives of VAR_dockedat_possessive citizens any conceivable amount.")
								  ]
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

,"merchant" : {
"siege" :	{"start" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}

		,"middle" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		,"end" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		}

,"battle" :	{"start" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}

		,"middle" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		,"end" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		}

,"fleetbattle":	{"start" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}

		,"middle" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		,"end" :	{"success" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"draw" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				,"loss" :	{"good"		: []
						,"bad"		: []
						,"neutral"	: []
						}
				}
		}
}

#\/The last close bracket for the whole dictionary\/
}
