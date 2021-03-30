from LevelEditor.scripts.editor import Editor

def main():
    #Runs the editor
    editor = Editor()
    editor.load('data/levels/level2.json')
    editor.main_loop()

main()
