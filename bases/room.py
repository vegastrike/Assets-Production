import Base

room = Base.Room ('Sleeping Room')
Base.Texture (room, 'tex', 'bases/room/room.spr', 0, 0)
Base.Comp (room, 'missioncomp', 0.824, -0.652, 0.14, 1.058, 'Exit to Mission Computer', 'Missions News')
Base.Link (room, 'about', -0.556, -0.25, 1.064, 0.859, 'Information', 1)

room = Base.Room ('About')
Base.Texture (room, 'tex', 'bases/room/about.spr', 0, 0)
Base.Link (room, 'exit', 0.718, 0.609, 0.281, 0.388, 'Exit', 0)
Base.Link (room, 'credits', 0.054, -1, 0.945, 0.437, 'Credits', 3)
Base.Link (room, 'history', -0.998, -1, 0.937, 0.437, 'History', 2)

room = Base.Room ('History')
Base.Texture (room, 'tex', 'bases/room/history.spr', 0, 0)
Base.Link (room, 'exit', 0.718, 0.609, 0.281, 0.388, 'Exit', 0)
Base.Link (room, 'about', 0.054, -1, 0.945, 0.437, 'About', 1)
Base.Link (room, 'credits', -0.998, -1, 0.937, 0.437, 'Credits', 3)


room = Base.Room ('Credits')
Base.Texture (room, 'tex', 'bases/room/credits.spr', 0, 0)
Base.Link (room, 'exit', 0.718, 0.609, 0.281, 0.388, 'Exit', 0)
Base.Link (room, 'history', 0.054, -1, 0.945, 0.437, 'History', 2)
Base.Link (room, 'about', -0.998, -1, 0.937, 0.437, 'About', 1)
