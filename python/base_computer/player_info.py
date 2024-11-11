
newline = "#n#"
faction_grey = "#c0.667:0.667:1#"
green = "#c0:1:.5#"
light_grey = "#c.75:.9:1#"
grey = "#c.6:.7:.8#"
light_yellow = "#c.675:.925:.825#"
end_color = "#-c"
bold = "#b#"
end_bold = "#-b"

disallowed_factions = ['graphics', 'planets', 'upgrades', 'unprintable_factions']

def get_color(relation):
    norm_relation = (relation + 1) / 2; # Move relation value into 0-1 range.
    norm_relation = max(0, min(1, norm_relation)); # Make *sure* it's in the right range.
    
    red = 1 - norm_relation
    green = norm_relation
    blue = min(norm_relation, 1-norm_relation)
    
    return f"#c{red}:{green}:{blue}#"

def get_player_info(names, relations, kills):
    total_kills = 0
    
    if len(names) != len(relations) or len(names) != len(kills):
        return f"Error. Length mismatch ({len(names)}/{len(relations)}/{len(kills)})."
    
    text = f"{newline}{bold}Factions:{end_bold}#n1.7#"
    
    for name, relation_str, kills_str in zip(names, relations, kills):
        relation = int(round(float(relation_str) * 100))
        faction_kills = int(round(float(relation_str)))
        
        # For some reason, privateer reports 1 kill
        if name == 'privateer':
            faction_kills = 0
            
        total_kills += faction_kills
        
        color = get_color(relation)
        
        if faction_kills == 0 or name == 'privateer':
            text += f"{light_grey}{name}:{end_color} {color}{relation}{end_color}{newline}"
        else: 
            text += f"{light_grey}{name}:{end_color} {color}{relation}, kills: {faction_kills}{end_color}{newline}"
    
    text += f"{newline}{bold}Total Kills: {total_kills}{end_bold}{newline}"
        
    return text
