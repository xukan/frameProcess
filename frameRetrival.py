import os
import glob
import shutil
from pdb import set_trace as bp

PREFIX = "/media/smilelab/" #have problem with file position
INPUTDIR = "Lynnsey/UCF-101/UCF-101_frames_flow/";

#PATH = os.getcwd();
PATH = os.path.normpath(os.path.join(os.getcwd(), os.pardir))
OUTPUTDIR = PATH + "/mergedFrames"
#OUTPUTDIR = PATH + "/testFrames"
TENFRAMES = PATH + "/tenframes"

FLOW_X = "flow_x"
FLOW_Y = "flow_y"
RGB = "rgb"

PUNCH = "Punch"
FENCING = "Fencing"

TEST_FRAME1 = "v_YoYo_g19_c05"
TEST_FRAME2 = "v_YoYo_g21_c01"
TEST_FRAME3 = "v_YoYo_g22_c06"

#input = {TEST_FRAME1, TEST_FRAME2, TEST_FRAME3};
#input = {TEST_FRAME6};

def getInput():
	"""
	Test function
	"""
	videos = os.listdir( PREFIX + INPUTDIR )
	inputList  = [ video for video in videos if "ApplyLipstick" in video ]
	return inputList

def getLabel( labelPath ):
	labels = {}
	with open( labelPath, "r") as file:
		for line in file:
			tokens = line.split(" ")
			label = tokens[1].replace("\r\n","")
			if label not in labels:
				labels[ label ] = tokens[ 0 ]
	return labels

def videoProcess( videos ):
	videoDict = {}
	for video in videos:
		tokens = video.split( "_" )
		if tokens[ 1 ] not in videoDict:
			videoDict[ tokens[ 1 ] ] = {}
		videoDict[ tokens[ 1 ] ][ video ] = len( videoDict[ tokens[ 1 ] ] ) + 1 
	return videoDict		

def getVideoNum( videoDict, video ):
	tokens = video.split( "_" )
	return videoDict[ tokens[ 1 ] ][ video ]

def getVideos():
	videos = os.listdir( PREFIX + INPUTDIR )
	videos.sort( key=str.lower )
	return videos

def twoVideoRetrieve( labels ):
	"""
	copy 10 frames from each video to destionation folder and rename image file
	new name format is frame#_actionLabel_video#.jpg
	"""
	videos = getVideos()
	videoDict = videoProcess( videos )
	punchimgs = []
	if os.path.exists(TENFRAMES):
		shutil.rmtree(TENFRAMES)
	os.makedirs(TENFRAMES)
	if not os.path.exists(OUTPUTDIR):
		print "Folder is not created"
		return
	videoNum = 1
	print len(videoDict[ FENCING ])
	for action in [ PUNCH, FENCING]:
		for video in videoDict[ action ]:
			imgs = glob.glob( PREFIX + INPUTDIR + video + "/img_*.jpg")	 
			imgs.sort()
			frameNum = 0
			srcimgs = imgs[::len(imgs)/9]	
			if len(srcimgs) < 10:
				srcimgs.append(imgs[-1])
			for img in srcimgs: 
				#frame = img.split("/")[-1]
				#frameNum = frame.split( "_" )[-1].split(".")[0][ -3 : ]
				frameNum += 1
				videoNum = videoDict[ action ][ video ]
				newFileName = str( frameNum ).rjust( 3, '0' ) + \
					"_" + labels[ action ].rjust( 3, '0' ) + \
					"_" + str( videoNum ).rjust( 3, '0' ) + ".jpg";
				shutil.copy( img, TENFRAMES + "/" + newFileName )
	print "Mission Complete" 

def retrieve( labels ):
	"""
	copy first 100 frames from each video to destionation folder and rename image file
	new name format is frame#_actionLabel_video#.jpg
	"""
	if os.path.exists(OUTPUTDIR):
		shutil.rmtree(OUTPUTDIR)
	os.makedirs(OUTPUTDIR)
	if not os.path.exists(OUTPUTDIR):
		print "Folder is not created"
		return
	os.makedirs(OUTPUTDIR + "/" + FLOW_X)	
	os.makedirs(OUTPUTDIR + "/" + FLOW_Y)	
	os.makedirs(OUTPUTDIR + "/" + RGB)	
	if not os.path.exists(OUTPUTDIR  + "/" + FLOW_X) or \
	   not os.path.exists(OUTPUTDIR  + "/" + FLOW_Y) or \
	   not os.path.exists(OUTPUTDIR  + "/" + RGB):
		print "subfolders are not created"
		return	
	#videos = os.listdir( PREFIX + INPUTDIR )
	#videos.sort( key=str.lower )
	videos = getVideos()
	videoDict = videoProcess( videos )
	imageDict = dict()
	for video in videos:
	#input = getInput()
	#input.sort( key=str.lower )
	#bp()
	#print input
	#for video in input:
		videoNum = getVideoNum( videoDict, video )
		label = video.split("_")[1]
		actionLabel = labels[ label ]
		frames =  os.listdir(PREFIX+INPUTDIR+ video );
		frames.sort()
		imageDict.clear()
		#bp()
		for frame in frames:
			tokens = frame.split( "_" )
			frameType = "_".join( tokens[ : -1 ] )
			if frameType not in imageDict:
				imageDict[ frameType ] = []
			imageDict[ frameType ].append( video + "/" + frame )
		for token in imageDict.keys():
			subfolder = ""
			#if token == "img":
			#	bp()
			if token == "flow_x":
				subfolder = FLOW_X
			elif token == "flow_y":
				subfolder = FLOW_Y
			else:
				subfolder = RGB
			# token is one of flow_x, flow_y or img
			imageDict[ token ].sort( key = str.lower )
			jpgs = imageDict[ token ]
			i = 1
			newName = ""
			newFile = ""
			for jpg in jpgs:
				srcFile = PREFIX + INPUTDIR + jpg
				#frame = jpg.split( "/" )[ 0 ]
				image = jpg.split( "/" )[ 1 ]
				shutil.copy( srcFile, OUTPUTDIR + "/" + subfolder )
				dstFile = OUTPUTDIR + "/" + subfolder + "/" + image
				newName = "_".join([ str(i).rjust( 3, '0' ), 
						     str(actionLabel).rjust( 3, '0' ), 
						     str(videoNum).rjust( 3, '0' ) ]) + ".jpg"
				newFile = OUTPUTDIR + "/" + subfolder + "/" + newName
				os.rename( dstFile, newFile )
				i += 1
				if i > 100:
					break
			while i <= 100:
				newName = "_".join([ str(i).rjust( 3, '0' ), 
						     str(actionLabel).rjust( 3, '0' ), 
						     str(videoNum).rjust( 3, '0' ) ]) + ".jpg"
				shutil.copy( newFile, OUTPUTDIR + "/" + subfolder + "/" + newName )
				i += 1
	
	print "mission complete"
					
if __name__== "__main__":
	labels = getLabel( PATH + "/classInd.txt")
	retrieve( labels )
