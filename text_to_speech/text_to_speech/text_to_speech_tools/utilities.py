import os.path

def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def fileExists(path) :
    return os.path.isfile(path)

def getFilePathAndCreateFolders(tool_folder, request, extension):
    local_folder = "tts_audio_files" 
    absolute_path_folder = os.path.expanduser('~') + "/" + local_folder + "/" + tool_folder + "/" + request.config.language + "/" + request.config.gender 
    createFolder(absolute_path_folder)
    return absolute_path_folder + "/" + request.text + "." + extension
    