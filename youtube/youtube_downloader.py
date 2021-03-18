## importing the module
import pafy

## url of the video
url = "https://www.youtube.com/watch?v=yqtgqP4ra5E"
## calling the new method of pafy
result = pafy.new(url)
## getting the best quality of video from the 'result' using the getbest()
best_quality_video = result.getbest()
## you can print it to see the quality of the video
print(best_quality_video)
## download it using the download()
best_quality_video.download()
