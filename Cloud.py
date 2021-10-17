import youtube_dl

def getSongData(url):
	ydl_opts = {}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		song_info = ydl.extract_info(url, download=False)
		return song_info


def downloadYtSong(videoToDownload):
	if not(videoToDownload.isVideo):
		if not(videoToDownload.isDefaultFormat):
			ydl_opts = {
				'format': 'bestaudio/best',
		        'outtmpl': 'Downloads/'+videoToDownload.nombre+'.%(ext)s',
		        'noplaylist': True,
		        'postprocessors': [{
		        	'key': 'FFmpegExtractAudio',
		            'preferredcodec': videoToDownload.formato, #mp3, m4a, wav
					'preferredquality': '192', }]
			}
		else:
			ydl_opts = {
				'format': 'bestaudio/best',
		        'outtmpl': 'Downloads/'+videoToDownload.nombre+'.%(ext)s',
		        'noplaylist': True,
			}
	else:
		if not(videoToDownload.isDefaultFormat):
			ydl_opts = {
				'format': 'bestvideo+bestaudio/best',
		        'outtmpl': 'Downloads/'+videoToDownload.nombre+'.%(ext)s',
		        'noplaylist': True,
		        'postprocessors': [{
		        	'key': 'FFmpegVideoConvertor',
		            'preferedformat': videoToDownload.formato, #avi, flv, mkv, mp4, ogg, webm
				}]
			}
		else:
			ydl_opts = {
				'format': 'bestvideo+bestaudio/best',
		        'outtmpl': 'Downloads/'+videoToDownload.nombre+'.%(ext)s',
		        'noplaylist': True,
			}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([videoToDownload.url])