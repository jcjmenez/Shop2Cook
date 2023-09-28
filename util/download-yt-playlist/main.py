import getTextFromWav
import utils
import os
import YTVideoDownloader
import getAudioFromVideo

if __name__ == "__main__":
    utils.createFolders()
    toSearch = "https://www.youtube.com/watch?v=wFEpBjxUGzg&list=PL4YDpMzkXfArjg95gVHPiURj_VA3vgVeX&index=39"
    videosToDownload = YTVideoDownloader.download_playlist(toSearch)
    folderVs = os.listdir("videos")
    for video in folderVs:
        os.rename("videos/" + video, "videos/" + utils.remove_emojis(video))
    getAudioFromVideo.getAudio()
    #print(videosToDownload)

    #getTextFromVideo.getTextFromVideo()
    getTextFromWav.getTranscription()

    
