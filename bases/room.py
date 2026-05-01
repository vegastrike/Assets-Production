import Base

room = Base.Room ('Sleeping Room')
Base.Texture (room, 'tex', 'bases/room/room.spr', 0, 0)
Base.Comp (room, 'missioncomp', 0.824, -0.652, 0.14, 1.058, 'Exit to Mission Computer', 'Info')
Base.Link (room, 'about', 0.099, -0.041, 0.341, 0.753, 'Information', 1)

room = Base.Room ('About')
Base.Texture (room, 'tex', 'bases/room/about.spr', 0, 0)
Base.Link (room, 'exit', 0.605, 0.787, 0.318, 0.138, 'Exit', 0)
Base.Link (room, 'credits', -0.089, 0.787, 0.326, 0.142, 'Credits', 3)
Base.Link (room, 'history', -0.488, 0.783, 0.32, 0.097, 'History', 2)

room = Base.Room ('History')
Base.Texture (room, 'tex', 'bases/room/history.spr', 0, 0)
Base.Link (room, 'exit', 0.605, 0.787, 0.318, 0.138, 'Exit', 0)
Base.Link (room, 'about', -0.898, 0.785, 0.33, 0.144, 'About', 1)
Base.Link (room, 'credits', -0.089, 0.787, 0.326, 0.142, 'Credits', 3)


room = Base.Room ('Credits')
Base.Texture (room, 'tex', 'bases/room/credits.spr', 0, 0)
Base.Link (room, 'exit', 0.605, 0.787, 0.318, 0.138, 'Exit', 0)
Base.Link (room, 'history', -0.488, 0.783, 0.32, 0.097, 'History', 2)
Base.Link (room, 'about', -0.898, 0.785, 0.33, 0.144, 'About', 1)
