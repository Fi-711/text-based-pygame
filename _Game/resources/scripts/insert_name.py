def insert_name(text, player_name):
    if type(text) == str:
        text = text.replace("[player]", player_name)
        return text
        
