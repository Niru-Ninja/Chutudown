from tkinter import *
from tkinter import _setit
from tkinter import ttk
import _thread

import Cloud

root = Tk()
root.title("Chutudown")
root.geometry("420x260")

class YTInfo:
	def __init__(self, _url, _songInfo):
		self.url = _url
		self.songInfo = _songInfo


songData = YTInfo('', '')
isVideo = True
defaultFormat = BooleanVar()
playlistDownload = BooleanVar()
videosToDownload = []

######## ADRESS BAR & BUTTONS: ########
def clearSearch():
	addressBar.delete(0, 'end')


def getVideoInfo(url):
	global songData
	songData.url = url
	songData.songInfo = Cloud.getSongData(url)
	print(type(songData.songInfo))
	updateInfo()
	return


topBar = Frame(root)
clearButton = Button(topBar, text="X", command=clearSearch, font='Consolas 8 bold')
addressBar = Entry(topBar, font='Consolas 8 bold', cursor="xterm", width=57)
getButton = Button(topBar, text="Info", command=lambda:getVideoInfo(addressBar.get()), font='Consolas 8 bold')
topBar.pack()
clearButton.grid(row=0, column=0, padx=2)
addressBar.grid(row=0, column=1, pady=5)
getButton.grid(row=0, column=2, padx=2)

######## INFO FRAME AND DOWNLOAD LIST: ########
infoAndList = Frame(root)
infoAndList.pack()

class downloadInfo:
	url = ""
	nombre = ""
	isVideo = True
	formato = ""
	isDefaultFormat = False
	def __init__(self, _url, _nombre, _isVideo, _formato, _isDefaultFormat):
		self.url = _url
		self.nombre = _nombre
		self.isVideo = _isVideo
		self.formato = _formato
		self.isDefaultFormat = _isDefaultFormat


def switchIsVideo(button, formatEntry, optionsVideo, optionsAudio, selectedOpt):
	global isVideo
	isVideo = not(isVideo)
	formatEntry['menu'].delete(0, 'end')
	if isVideo:
		button.configure(text="Video")
		for choice in optionsVideo:
			formatEntry['menu'].add_command(label=choice, command=_setit(selectedOpt, choice))
		selectedOpt.set("mp4")
	else:
		button.configure(text="Audio")
		for choice in optionsAudio:
			formatEntry['menu'].add_command(label=choice, command=_setit(selectedOpt, choice))
		selectedOpt.set("mp3")		


def startDownloadThread(showList):
	global videosToDownload
	for video in videosToDownload:
		Cloud.downloadYtSong(video)
		showList.delete(0)
	videosToDownload = []
	return


def downloadAll():
	if not(videosToDownload):
		addToList(fileName.get(), selectedOpt.get())
	_thread.start_new_thread(startDownloadThread, (downloadList, ))
	return


def addToList(nombre, formato):
	global isVideo, songData
	if not(playlistDownload.get()):
		if 'entries' in songData.songInfo: 
			getVideoInfo(songData.url.split('&')[0])
		videoToDownload = downloadInfo(addressBar.get(), nombre, isVideo, formato, defaultFormat.get())
		videosToDownload.append(videoToDownload)
		downloadList.insert('end', nombre)
	else:
		for i, item in enumerate(songData.songInfo):
			videoToDownload = downloadInfo(songData.songInfo['entries'][i]['webpage_url'], songData.songInfo['entries'][i]['title'], isVideo, formato, defaultFormat.get())
			videosToDownload.append(videoToDownload)
			downloadList.insert('end', songData.songInfo['entries'][i]['title'])
			print(i)


def toggleEnableOptionMenu():
	if defaultFormat.get():
		formatEntry.configure(state="disabled")
	else:
		formatEntry.configure(state="normal")

## Info Frame: ##
infoFrame = Frame(infoAndList)

filenameFrame = Frame(infoFrame)
fileNameLabel = ttk.Label(filenameFrame, text="Name: ", font='Consolas 8 bold')
fileName = Entry(filenameFrame, font='Consolas 8 bold', cursor="xterm", width=27)
filenameFrame.grid(pady=(10,15))
fileNameLabel.grid(row=0, column=0)
fileName.grid(row=0, column=1)

audioOrVideoButton = Button(infoFrame, text="Video", command=lambda:switchIsVideo(audioOrVideoButton, formatEntry, optionsVideo, optionsAudio, selectedOpt), font='Consolas 8 bold', width=35)
audioOrVideoButton.grid(pady=5)

playlistDownloadCheck = Checkbutton(infoFrame, text="Download Playlist", variable=playlistDownload, font='Consolas 8 bold')
playlistDownloadCheck.grid(pady=(5,0), sticky=W)

defaultCheck = Checkbutton(infoFrame, text="Native Format", variable=defaultFormat, command=toggleEnableOptionMenu, font='Consolas 8 bold')
defaultCheck.grid(pady=(0,5), sticky=W)

formatFrame = Frame(infoFrame)
formatLabel = ttk.Label(formatFrame, text="Format: ", font='Consolas 8 bold')
selectedOpt = StringVar()
selectedOpt.set("mp4")
optionsVideo = [
	"mp4",
	"avi",
	"flv",
	"mkv",
	"ogg",
	"webm"
]
optionsAudio = [
	"mp3",
	"m4a",
	"wav"
]
formatEntry = OptionMenu(formatFrame, selectedOpt, *optionsVideo)
formatFrame.grid(pady=2, sticky=W)
formatLabel.grid(row=0, column=0, sticky=W)
formatEntry.grid(row=0, column=1, sticky=E)

addButton = Button(infoFrame, text="Add", command=lambda:addToList(fileName.get(), selectedOpt.get()), font='Consolas 8 bold', width=35)
addButton.grid(pady=(11,0))

infoFrame.grid(row=0, column=0, sticky=NW)

def updateInfo():
	fileName.delete(0,END)
	fileName.insert(0, songData.songInfo['title'])
	addressBar.delete(0,END)
	addressBar.insert(0, songData.url)
	return

## List Frame: ##
def downloadListDoubleClick(event):
	global isVideo
	selectedItem = downloadList.curselection()[0]
	addressBar.delete(0,END)
	addressBar.insert(0, videosToDownload[selectedItem].url)
	fileName.delete(0,END)
	fileName.insert(0, videosToDownload[selectedItem].nombre)
	isVideo = videosToDownload[selectedItem].isVideo
	if isVideo:
		audioOrVideoButton.configure(text="Video")
		formatEntry['menu'].delete(0, 'end')
		for choice in optionsVideo:
			formatEntry['menu'].add_command(label=choice, command=_setit(selectedOpt, choice))
		selectedOpt.set(videosToDownload[selectedItem].formato)
	else:
		audioOrVideoButton.configure(text="Audio")
		formatEntry['menu'].delete(0, 'end')
		for choice in optionsAudio:
			formatEntry['menu'].add_command(label=choice, command=_setit(selectedOpt, choice))
		selectedOpt.set(videosToDownload[selectedItem].formato)
	if videosToDownload[selectedItem].isDefaultFormat:
		defaultCheck.select()
		formatEntry.configure(state="disabled")
	else:
		defaultCheck.deselect()
		formatEntry.configure(state="normal")


def downloadListRCMenuPopup(event):
	try:
		downloadListRCMenu.tk_popup(event.x_root, event.y_root)
	finally:
		downloadListRCMenu.grab_release()


def downloadListRCCommand():
	selectedItems = downloadList.curselection()
	for item in selectedItems[::-1]:
		downloadList.delete(item)
		del videosToDownload[item]


listFrame = Frame(infoAndList)
downloadList = Listbox(listFrame,
					selectmode=EXTENDED,
					font='Consolas 8 bold',
					activestyle= None,
					width=30,
					height=14)
downloadList.pack(padx=5)
downloadList.bind('<Double-1>', downloadListDoubleClick)
downloadList.bind('<Button-3>', downloadListRCMenuPopup)
downloadListRCMenu = Menu(downloadList, tearoff=0, font="Consolas 8 bold")
downloadListRCMenu.add_command(label="Remove", command=downloadListRCCommand)

downloadButton = Button(listFrame, text="Download", command=downloadAll, font='Consolas 8 bold', width=29)
downloadButton.pack(pady=5)

listFrame.grid(row=0, column=1, sticky=E)

root.mainloop()