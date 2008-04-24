from optparse import OptionParser


parser = OptionParser()

# DEBUGGING OPTIONS -----------------------------------------------------

parser.add_option("--debug", help="enable debug window",
		action="store_true", dest="DebugWindow", default=False)

parser.add_option("--no-debug-int", help="Fatal errors don't genereate an int 3 before exiting",
		action="store_false", dest="dbgInt3Enabled", default=True)

parser.add_option("--debug-file", help="output debugging info to a file",
		action="store_true", dest="debugToFile", default=False)

parser.add_option("--ran-caller-debug", help="debug non-deterministic calling of random numbers",
		action="store_true", dest="ranCallerDebug", default=False)

parser.add_option("--autosave-debug", help="autosaves game frequently",
		action="store_true", dest="autoSaveDebug", default=False)

# SYSTEM OPTIONS -----------------------------------------------------

def set_heap(option, opt, value, parser):
	if value > 18*1024*1024 * 2:
		parser.values.MemoryHeapSize = value
parser.add_option("--heap", metavar="N", help="Sets size of global memory heap to [N]",
		action="callback", callback=set_heap,
		dest="MemoryHeapSize", type="int", default=18*1024*1024)

parser.add_option("--big-override", metavar="PATH", help="Sets path to search for opening files",
		dest="fileOverrideBigPath")

parser.add_option("--settings-path", metavar="PATH", help="Sets the path to store settings, saved games, and screenshots (defaults to ~/.homeworld)",
		dest="fileUserSettingsPath")

parser.add_option("--free-mouse", help="Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play",
		action="store_false", dest="startupClipMouse", default=True)

parser.add_option("--ignore-big", help="don't use anything from bigfiles",
		action="store_true", dest="IgnoreBigfiles", default=False)

parser.add_option("--log-file-loads", help="create log of data files loaded",
		action="store_true", dest="LogFileLoads", default=False)
		#logfileClear(FILELOADSLOG)

# PROCESSOR OPTIONS -----------------------------------------------------

parser.add_option("--enable-sse", help="allow use of SSE if support is detected",
		action="store_true", dest="mainAllowKatmai", default=False)

parser.add_option("--force-sse", help="force usage of SSE even if determined to be unavailable",
		action="store_true", dest="mainForceKatmai", default=False)

parser.add_option("--enable3dnow", help="allow use of 3DNow! if support is detected",
		action="store_true", dest="mainAllow3DNow", default=False)

# SOUND OPTIONS -----------------------------------------------------

parser.add_option("--no-sound", help="turn all sound effects off",
		action="store_false", dest="enableSFX", default=True)

parser.add_option("--no-speech", help="turn all speech off",
		action="store_false", dest="enableSpeech", default=True)

parser.add_option("--dsound", help="forces mixer to write to DirectSound driver, even if driver reports not certified",
		action="store_true", dest="useDSound", default=False)

parser.add_option("--dsoundcoop", help="switches to co-operative mode of DirectSound (if supported) to allow sharing with other applications",
		action="store_true", dest="coopDSound", default=False)

parser.add_option("--waveout", help="forces mixer to write to Waveout even if a DirectSound supported object is available",
		action="store_true", dest="useWaveout", default=False)

parser.add_option("--reversestereo", help="swap the left and right audio channels",
		action="store_true", dest="reverseStereo", default=False)

# DETAIL OPTIONS -----------------------------------------------------

parser.add_option("--raster-skip", help="enable interlaced display with software renderer",
		action="store_true", dest="mainRasterSkip", default=False)

parser.add_option("--no-bg", help="disable display of galaxy backgrounds",
		action="store_false", dest="showBackgrounds", default=True)

parser.add_option("--no-filter", help="disable bi-linear filtering of textures",
		action="store_false", dest="texLinearFiltering", default=True)

parser.add_option("--no-smooth", help="do not use polygon smoothing",
		action="store_false", dest="enableSmoothing", default=True)

parser.add_option("--niltexture", help="don't ever load textures at all",
		action="store_true", dest="GLOBAL_NO_TEXTURES", default=False)

parser.add_option("--no-effects", help="disable all effects (Debug only)",
		action="store_false", dest="etgEffectsEnabled", default=True)

parser.add_option("--no-fetextures", help="turns off front end textures",
		action="store_false", dest="fetEnableTextures", default=True)

parser.add_option("--stipple", help="enable stipple alpha with software renderer",
		action="store_true", dest="enableStipple", default=False)

parser.add_option("--no-showdamage", help="Disables showing ship damage effects",
		action="store_false", dest="gShowDamage", default=True)

# VIDEO MODE OPTIONS -----------------------------------------------------

parser.add_option("--safegl", help="don't use possibly buggy optimized features of OpenGL for rendering",
		action="store_true", dest="mainSafeGL", default=False)

parser.add_option("--enable", help="use when frontend menus are flickering madly",
		action="store_true", dest="mainDoubleIsTriple", default=False)

parser.add_option("--no-drawpixels", help="use when background images don't appear while loading",
		action="store_true", dest="mainNoDrawPixels", default=False)

parser.add_option("--no-swddraw", help="don't use DirectDraw for the software renderer",
		action="store_false", dest="mainSoftwareDirectDraw", default=True)

parser.add_option("--no-glddraw", help="don't use DirectDraw to setup OpenGL renderers",
		action="store_false", dest="mainDirectDraw", default=True)

parser.add_option("--sw", help="reset rendering system to defaults at startup",
		action="store_true", dest="mainForceSoftware", default=False)

parser.add_option("--no-savedmode", help="disable recovery of previous display mode",
		action="store_false", dest="mainAutoRenderer", default=True) # hidden

parser.add_option("--no-fast-fe", help="disable fast frontend rendering",
		action="store_false", dest="mainFastFrontend", default=True)

#parser.add_option("--fullscreen", help="display fullscreen with software renderer (default)",
#		action="store_true", dest="fullScreen")
parser.add_option("--window", help="display in a window",
		action="store_false", dest="fullScreen", default=True)

parser.add_option("--noborder", help="no border on window",
		action="store_false", dest="showBorder", default=True)

parser.add_option("--d3ddevicecrc", help="generate d3dDeviceCRC.txt for video troubleshooting",
		action="store_true", dest="mainOutputCRC", default=False)

parser.add_option("--640", help="run at 640x480 resolution (default)",
		action="store_const", dest="mainWindow", const=(640,480), default=(640,480))
		#selectedRES = true

parser.add_option("--800", help="run at 800x600 resolution",
		action="store_const", dest="mainWindow", const=(800,600))
		#selectedRES = true

parser.add_option("--1024", help="run at 1024x768 resolution",
		action="store_const", dest="mainWindow", const=(1024,768))
		#selectedRES = true

parser.add_option("--1280", help="run at 1280x1024 resolution",
		action="store_const", dest="mainWindow", const=(1280,1024))
		#selectedRES = true

parser.add_option("--1600", help="run at 1600x1200 resolution",
		action="store_const", dest="mainWindow", const=(1600,1200))
		#selectedRES = true

#parser.add_option("--d16", help="run in 16 bits of colour",
#		action="store_const", dest="MAIN_WindowDepth", const=16)

#parser.add_option("--d24", help="run in 24 bits of colour",
#		action="store_const", dest="MAIN_WindowDepth", const=24)

#parser.add_option("--d32", help="run in 32 bits of colour",
#		action="store_const", dest=MAIN_WindowDepth"", const=32)

#parser.add_option("--truecolor", help="try 24bit modes before 15/16bit",
#		action="store_true", dest="trueColor", default=False)

#parser.add_option("--slowblits", help="use slow screen blits if the default is buggy",
#		action="store_true", dest="slowBlits", default=False)

parser.add_option("--device", metavar="N", help="Sets size of global memory heap to [N]",
		dest="deviceToSelect")
		# selectedDEVICE = true

parser.add_option("--no-hint", help="disable usage of OpenGL perspective correction hints",
		action="store_true", dest="mainNoPerspective", default=False)

parser.add_option("--nopause", help="don't pause when you alt-tab",
		action="store_true", dest="noPauseAltTab", default=False) # hidden

parser.add_option("--nominimize", help="don't minimize when you alt-tab",
		action="store_true", dest="noMinimizeAltTab", default=False) # hidden

# CHEATS AND SHORTCUTS -----------------------------------------------------

parser.add_option("--cheapships", help="ships only cost 1 RU",
		action="store_true", dest="cmCheapShips", default=False)

parser.add_option("--sensor-level", metavar="0|1|2", help="set initial sensors level (default 0)",
		dest="initialSensorLevel", type="choice", choices=['0','1','2'], default='0')

parser.add_option("--no-compplayer", help="disable default computer players",
		action="store_true", dest="noDefaultComputerPlayer", default=False)

#parser.add_option("--no-tactics", help="Disables tactics",
#		action="store_false", dest="tacticsOn", default=True)

parser.add_option("--no-retreat", help="disables the 'retreat' feature of tactics",
		action="store_true", dest="noRetreat", default=False)

parser.add_option("--disable-avi", help="don't display intro sequences",
		action="store_false", dest="enableAVI", default=True)

# VISUALIZATION -----------------------------------------------------

parser.add_option("--docklines", help="show dock lines",
		action="store_true", dest="dockLines", default=False)

parser.add_option("--gunlines", help="show gun lines",
		action="store_true", dest="gunLines", default=False)

parser.add_option("--lightlines", help="show light lines (Debug only)",
		action="store_true", dest="RENDER_LIGHTLINES", default=False)

parser.add_option("--boxes", help="render bounding bowties on the ships",
		action="store_true", dest="RENDER_BOXES", default=False)

parser.add_option("--text-feedback", help="enable text feedback for in game commands",
		action="store_true", dest="enableTextFeedback", default=False)

parser.add_option("--special-textures", help="enable special debugging textures",
		action="store_true", dest="trSpecialTextures", default=False)

parser.add_option("--morph-debug", help="enable debugging of morphed mesh rendering code",
		action="store_true", dest="meshMorphDebug", default=False)

parser.add_option("--lod-scale-debug", metavar="N.N", help="enable fixing a LOD scale factor",
		dest="lodDebugScaleFactor", type='float')

parser.add_option("--focusroids", help="enable focussing on asteroids and dust clouds",
		action="store_true", dest="mrCanFocusRoids", default=False)

parser.add_option("--showextents", help="draw elliptical universe extents",
		action="store_true", dest="pieVisualizeExtents", default=False)

parser.add_option("--loadfreelog", help="enable logging of what was loaded and freed between missions",
		action="store_true", dest="univLoadFreeLog", default=False)

parser.add_option("--nobind", help="disable key bindings so that debug keys work",
		action="store_true", dest="bkDisableKeyRemap", default=False) # hidden

# COMPUTER PLAYER AND STATS -----------------------------------------------------

parser.add_option("--aiplayerlog", help="enable AI Player Logging",
		action="store_true", dest="aiplayerLogEnable", default=False)

parser.add_option("--determcompplayer", help="makes computer players deterministic",
		action="store_true", dest="determCompPlayer", default=False)

parser.add_option("--gatherstats", help="enable gathering of stats",
		action="store_true", dest="gatherStats", default=False) # noDefaultComputerPlayer=true

parser.add_option("--showstatsfight", metavar="I J", help="to show stats fight i,j",
		dest="showStatsFight", type="int", nargs=2, default=(0,0)) #showStatsFightI, showStatsFightJ

parser.add_option("--showstatsfancyfight", metavar="FILENAME.script", help="",
		dest="showStatsFancyFightScriptFile") # showStatsFancyFight=true; noDefaultComputerPlayer=true;

# NETWORK PLAY -----------------------------------------------------

parser.add_option("--captaincylogoff", help="turns off captaincy log file",
		action="store_false", dest="captaincyLogEnable", default=True)

parser.add_option("--captaincylogon", help="turns on captaincy log file",
		action="store_true", dest="captaincyLogEnable", default=False)

def set_debugsync(option, opt, value, parser):
	parser.values.recordPackets = True
	parser.values.logEnable = 'LOG_VERBOSE'
	parser.values.autoSaveDebug = True;
parser.add_option("--debugsync", help="autosaves game frequently, records packets, logonverbose",
		action="callback", callback=set_debugsync)

parser.add_option("--nowon", help="no WON stuff",
		action="store_true", dest="SecretWON", default=False) # hidden

parser.add_option("--forcelan", help="allow LAN play regardless of version",
		action="store_true", dest="forceLAN", default=False)

parser.add_option("--noauth", help="Disables WON Login",
		action="store_true", dest="noAuthorization", default=False)  # hidden

parser.add_option("--logoff", help="turns of network logging file",
		action="store_const", dest="logEnable", const='LOG_OFF') # hidden

parser.add_option("--logon", help="turns network logging file on",
		action="store_const", dest="logEnable", const='LOG_ON') # hidden

parser.add_option("--logonverbose", help="turns verbose network logging file on",
		action="store_const", dest="logEnable", const='LOG_VERBOSE') # hidden

parser.add_option("--logfilepath", metavar="FILEPATH.txt", help="",
		dest="logFilePath")  # hidden

parser.add_option("--shortwon", help="short circuit WON stuff",
		action="store_true", dest="ShortCircuitWON", default=False)  # hidden

parser.add_option("--statlogon", help="generates game stats log file",
		action="store_true", dest="statLogOn", default=False)

parser.add_option("--bryceanddrewaregods", metavar="X Y", help="X = size of SyncDumpWindow  Y = granularity in universe Frames",
		dest="syncDump", type="int", nargs=2, default=(640,480)) # syncDumpWindowSize, syncDumpGranularity

# NIS OPTIONS -----------------------------------------------------

parser.add_option("--testnis", metavar="nisFile", help="enables NIS testing mode using [nisFile",
		dest="nisTestNIS")

parser.add_option("--testnisscript", metavar="SCRIPTFILE", help="enables NIS testing mode using [SCRIPTFILE]",
		dest="nisTestScript")

parser.add_option("--niscounter", help="display nis time index info by default",
		action="store_true", dest="nisPrintInfo", default=False)

parser.add_option("--nisnolockout", help="don't lock out the interface when playing an NIS",
		action="store_true", dest="nisNoLockout", default=False)

# RECORDED DEMOS -----------------------------------------------------

parser.add_option("--demorecord", metavar="fileName", help="record a demo",
		dest="demDemoFilename") # demDemoRecording=true

parser.add_option("--demoplay", metavar="fileName", help="play a demo",
		dest="demDemoFilename") # wasDemoPlaying = demDemoPlaying = noPauseAltTab = true;

parser.add_option("--packetrecord", help="record packets of this multiplayer game",
		action="store_true", dest="debugPacketRecord", default=False) # hidden # recordPackets=true

parser.add_option("--packetplay", metavar="fileName", help="play back packet recording",
		dest="recordPacketFileName") # hidden # transferCaptaincyDisabled=playPackets=true

parser.add_option("--comparebigfiles", help="file by file, use most recent (bigfile/filesystem)",
		action="store_true", dest="CompareBigfiles", default=False)

parser.add_option("--disableautodemos", help="don't automatically play demos",
		action="store_false", dest="demAutoDemo", default=True)

parser.add_option("--autodemowait", metavar="N", help="time to wait on main screen before starting a demo",
		dest="demAutoDemoWaitTime", type='float')

parser.add_option("--disablefakerenders", help="disable feature where playback will try to keep up with recorded demo",
		action="store_false", dest="demFakeRenders", default=True)

# TEXTURES -----------------------------------------------------

parser.add_option("--nopal", help="disable paletted texture support",
		action="store_true", dest="mainNoPalettes", default=False)

parser.add_option("--allowpacking", help="use the packed textures if available (default)",
		action="store_true", dest="mainAllowPacking", default=False) # hidden

parser.add_option("--disablepacking", help="don't use the packed textures if available",
		action="store_false", dest="mainAllowPacking", default=True)

parser.add_option("--onlypacking", help="only display packed textures",
		action="store_true", dest="mainOnlyPacking", default=False)

# MISC OPTIONS -----------------------------------------------------

parser.add_option("--smcentrecamera", help="centres the SM world plane about 0,0,0 rather than the camera",
		action="store_false", dest="smCentreWorldPlane", default=True) # hidden

parser.add_option("--noplug", help="don't display relic logo on pause",
		action="store_false", dest="rndShamelessPlugEnabled", default=True)

parser.add_option("--closecaptioned", help="close captioned for the hearing impared",
		action="store_true", dest="subCloseCaptionsEnabled", default=False) # hidden

parser.add_option("--pilotview", help="enable pilot view.  Focus on single ship and hit Q to toggle",
		action="store_true", dest="pilotView", default=False)


options, args = parser.parse_args(['script_name', '--help'])

# cleanup
del args
parser.destroy()
del parser
