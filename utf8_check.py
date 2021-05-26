import VS
import os

def is_utf8(save_game):
    try:
        file_path = VS.getSaveDir() + os.path.sep + save_game
        with open(file_path, encoding='utf-8') as in_file:
            text = in_file.read()
        return True
    except Exception as ex:
        print(ex)		
        return False
