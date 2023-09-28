import os
import moviepy.editor as mp

def getAudio():
    folderLs = os.listdir("videos")
    for title in folderLs:
        try:
            splittedTitle = title.split(".mp4")[0]
            video = mp.VideoFileClip(f"videos/{splittedTitle}.mp4")
            audio = video.audio
            audio.write_audiofile(f"audios/{splittedTitle}.wav")
        except:
            print("Error to split")