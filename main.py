import telebot
from os.path import realpath,dirname,join
from os import listdir
from math import ceil
from time import sleep
from datetime import datetime
from ssl import SSLWantWriteError
CWD = realpath(dirname(__name__))
TOKEN = "5655546835:AAHhgZm1ydBPquuwkJ5B12dqAm_vgv1HYE4"
CHANNEL = -1001894150205
bot = telebot.TeleBot(TOKEN)
picDirectory = join(CWD,"Pics") 
offset = 291 #291 maybe dangerous #428
print("Got path -> ", picDirectory)
pics = listdir(picDirectory)
if(len(pics)<10):Len = 1
else:Len = ceil(len(pics)/10)
print("Started")
def reopen(files):
	for file in files:
		file.close()
	files = []
	for pic in pics[i*10:((i+1)*10)]: 
		file = open(join(picDirectory,pic),"rb")
		files.append(file)
	return files
try:
	for i in range(offset,Len):
		while True:
			PICBATCH = []
			files = []
			print(f"	Forming batch №{i}")
			for pic in pics[i*10:((i+1)*10)]: 
				file = open(join(picDirectory,pic),"rb")
				PICBATCH.append(telebot.types.InputMediaPhoto(file))
				files.append(file)
			print(f"	Sending batch №{i}")
			try: bot.send_media_group(CHANNEL,PICBATCH)
			except ConnectionError as E: print(f"Connection Error -> {E}")
			except telebot.apihelper.ApiTelegramException as E:
				if("Error code: 400" in E.args[0]):
					print(f"	Empty files. You probably just fucked up something.")
				elif("Error code: 429" in E.args[0]):
					wait = int(str(E)[str(E).find("after")+6:])
					print(f"	Too many requests. Waiting {wait} seconds")
					sleep(wait)
				else:
					print(f"############\nException -> {E}\n Exception args -> {E.args}\n############")
			except TimeoutError:
				print(f"Timeout error! -> {files}")
			except Exception as e:
				print(f"Unknown fuckup -> {e}\nTrying to send one by one.")
				files = reopen(files)
				testfiles = files
				while True:
					for file in testfiles:
						try:
							print(f"	batch №{i} file №{testfiles.index(file)}",end=" ")
							bot.send_photo(CHANNEL,file)
						except Exception as e:
							file.seek(0)
							print(f"{e}.")
						else:
							testfiles.remove(file)
							print("sent.")
					if(len(testfiles)==0):
						break
					else:
						print(f"	Sending the errored one's ({len(testfiles)} units)")
				testfiles = []
				print(f"Batch of pictures is succesfully sent. {datetime.now().time()}")
				break
			else: 
				print(f"Batch of pictures is succesfully sent. {datetime.now().time()}")
				break
			finally:
				for file in files:
					file.close()
except KeyboardInterrupt: 
	print("stopped by you")
	quit()
else:
	print("done")
	input()