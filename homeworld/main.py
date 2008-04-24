
def main():
	#force_single_instance()

	# load in options from the options file
	options_file_read()
	# copy keyboard redefinitions
	op_keyboard_load()
	# process the command line, setting flags to be used later
	process_command_line()

	#initial game systems startup
	game_systems_pre_init()
	#scope exit utyGameSystemsPreShutdown()

	#startup the game window
	init_window()

	if options.DebugWindow:
		# start up the debug window and initialize all panes
		dbgwnd_start()
		# bit-field flags stating which system has started properly
		utyStartedBits[SSA_DebugWindow] = True

	# startup all miscellaneous game systems
	utyGameSystemsInit()

	# main loop
	while True:
		if SDL_PollEvent(&e):
			event_res = HandleEvent(&e) #switch event.type (focus|keys|mouse|quit|serevent|...)
			if e.type == SDL_QUIT:
				break
		else:
			utyTasksDispatch()  #execute all tasks

		if opTimerActive:
			if taskTimeElapsed > (opTimerStart + opTimerLength):
				opTimerExpired()

#---------
		# (Re)draw the screen
		# Handle events (keyboard input, mainly)
		while SDL_PollEvent(&event):
			if event.type == SDL_QUIT || (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE):
				return cleanUp(0)
		# while (handling events)
#---------



def utyGameSystemsInit():
	rndinitdata renderData
	Uint32 sdlSubsystemFlags

	utyToggleKeyStatesSave()
	utySet2(SS2_ToggleKeys)

	strLoadLanguage((strLanguageType) strCurLanguage)  # load in the language strings for messages to player
													   # must be called after file stuff and memory stuff

	# set the default player name based on the current language
	if (utyName[0] == 0)
		strcpy(utyName, strGetString(strDefaultPlayerName))

	utySet2(SS2_Strings)

	dbgMessagef(
		"Homeworld CRCs:\n"
		"%22s = 0x%x\n"    
		"%22s = 0x%x\n"    
		"%22s = 0x%x\n"    
		"%22s = 0x%x"    
		,
		"HomeworldSDL.big TOC", HomeworldCRC[0], # was CRC for code block (WON hacked client check)
		"Update.big TOC",       HomeworldCRC[1],
		"Homeworld.big TOC",    HomeworldCRC[2],
		"(not used)",           HomeworldCRC[3]  # never been used
	)
	
	# startup any SDL systems we want that haven't already been kicked off
	sdlSubsystemFlags = SDL_WasInit(SDL_INIT_EVERYTHING)

	if (!(sdlSubsystemFlags & SDL_INIT_TIMER))
		if (SDL_InitSubSystem(SDL_INIT_TIMER) == -1)
			return "Unable to initialize SDL Timer."
	
	# Joystick used for controlling the 3D camera view. It can be any old
	# joystick but this is primarily intended to support devices used for
	# 3D CAD applications which have more degrees of freedom (6) than typical
	# joysticks (2). For example: 3Dconnexion's SpaceNavigator.
	# http:#www.3dconnexion.com/products/3a1d.php
	if (!(sdlSubsystemFlags & SDL_INIT_JOYSTICK))
		int joystick_i = 0
		
		if (SDL_InitSubSystem(SDL_INIT_JOYSTICK) == -1)
			return "Unable to initialize SDL Joystick."
		
		for (joystick_i = 0; joystick_i < SDL_NumJoysticks(); ++joystick_i)
			if (strcmp(SDL_JoystickName(joystick_i), "SpaceNavigator") == 0)
				SDL_Joystick *joystick
				
				SDL_JoystickEventState(SDL_ENABLE)
				joystick = SDL_JoystickOpen(joystick_i)
				
				dbgMessagef("SpaceNavigator found at index %d", joystick_i)
			}
		}
	}
	
	utyTimerDivisor = 1000 / UTY_TimerResolutionMax
	utySet(SSA_Timer)
	#start the task manager
	taskStartup((udword)(1000 / utyTimerDivisor))
	utySet(SSA_Task)

	if (memStatsTaskHandle == 0xffffffff)
		memStatsTaskHandle = taskStart(memStatsTaskFunction, MEM_TaskStatsPeriod, 0)  #start frame rate task

	# create the autorun lock file
	utyLockFilehandle = 0
	utyLockFilehandle = fileOpen(utyLockFilename, FF_WriteMode|FF_IgnoreBIG|FF_UserSettingsPath)

	if (regStartup() != OKAY)  #startup the region processor
		return("Unable to start the region processor.")
	utySet(SSA_Region)

	# initialize sound engine
	soundEventInit()
	utySet2(SS2_SoundEngine)

	# Intro playing requires a window, which we have not made yet thanks to
	# how the code's been butchered. */

	utilPlayingIntro = FALSE

	renderData.width = MAIN_WindowWidth  #setup data for
	renderData.height = MAIN_WindowHeight  #initializing the
	#renderData.hWnd = ghMainWindow  #rendering system
	renderData.hWnd = 0  #rendering system
	if (rndInit(&renderData) != OKAY)  #startup the rendering system
		#fallback to 640x480@16 rGL+sw, and fatally exit if that doesn't work either
		mainRestoreSoftware()

	if (mouseStartup() != OKAY)
		return("Unable to start mouse.")
	utySet(SSA_Mouse)

	#create a region for the main window
	mrStartup()
	utySet(SSA_MainRegion)

	# Startup the information overlay, must occur after mrStartup()
	ioStartup()
	utySet2(SS2_InfoOverlay)

	utySet(SSA_Render)
	lightStartup()
	utySet(SSA_Lights)
	utyRenderTask = taskStart(rndRenderTask, 1.0f, TF_OncePerFrame)
	trStartup()
	utySet(SSA_TextureRegistry)

	taskCallBackInit()
	utySet2(SS2_BabyCallBackRegistry)

	universeInit()
	utySet(SSA_Universe)

	taskStart(universeUpdateTask, UNIVERSE_UPDATE_PERIOD, 0)

	autodownloadmapStartup()
	KeepAliveStartup()
	InitQueue(&ProcessSyncPktQ,50000)
	InitQueue(&ProcessCmdPktQ,50000)
	InitQueue(&ProcessRequestedSyncPktQ,20000)
	InitQueue(&ProcessCaptaincyPktQ,10000)
	InitLastSyncPktsQ()
	utySet2(SS2_NetworkQueues)
	taskStart(captainServerTask, CAPTAINSERVER_PERIOD, 0)

	gunStartup()
	utySet2(SS2_Guns)

	selStartup()
	utySet(SSA_Selection)

	uicStartup()  #start up UI controls
	utySet(SSA_UIControls)

	meshStartup()

	#startup transformer module
	transStartup()

	if (feStartup() != OKAY) #start the front end
		return("Unable to start front end.")

	utySet(SSA_FEFlow)
	utyClipMouse(startupClipMouse)  #clip mouse to window if needed
	utySet(SSA_MouseClipped)

	utyFrontEndDataLoad()
	utySet(SSA_FrontEndData)

	tacticsStartUp()

	lmStartup()
	utySet2(SS2_LaunchMgr)

	tmStartup()

	rmAPIStartup()
	utySet2(SS2_ResearchMgr)

	smStartup()  #start the sensors manager
	utySet(SSA_SensorsManager)

	svStartup()
	utySet2(SS2_ShipView)

	pingStartup()
	utySet2(SS2_Ping)

	battleChatterStartup()
	utySet2(SS2_BattleChatter)

	teStartup()  #start the team-specific stuff
	if (!cpColorsPicked)
		utyBaseColor   = teColorSchemes[0].textureColor.base
		utyStripeColor = teColorSchemes[0].textureColor.detail

	utySet(SSA_Teams)

	cpStartup(&utyBaseColor, &utyStripeColor)  #start the color picker
	utySet(SSA_ColorPicker)

	subStartup()
	utySet2(SS2_SubTitle)

	tutStartup()
	utySet2(SS2_Tutorial)

	animStartup()  #start the animatics module

	spStartup()  #start the scenario picker
	utySet(SSA_ScenarioPicker)

	gpStartup()
	utySet2(SS2_GamePicker)

	mgStartup()
	lgStartup()
	mgGameTypeScriptInit()
	utySet2(SS2_MultiplayerGame)

	cmStartup()  #start the construction manager
	utySet(SSA_ConstructionManager)

	ranStartup()  #start the random-number generator
	utySet(SSA_RandomNumbers)

	bsStartup()
	utySet2(SS2_BSpline)

	nisStartup()
	utySet2(SS2_NIS)

	udStartup()  #start the undo module
	utySet(SSA_Undo)

	toStartup()  #start the TO module
	utySet(SSA_TacticalOverlay)

	dmgStartup()

	cloudStartup()

	shStartup()

	nebStartup()

	btgStartup()

	alodStartup()

	partStartup()

	pieStartup()

	trailStartup()  #start the trails module
	utySet(SSA_ShipTrails)

	#clear out the task timer.  Make sure this is the last call in this function.
	utyTaskTimerClear()

	if (fetEnableTextures)
		ferStartup()  #start front end texture registry

	prim3dStartup()  #start the prim 3d stuff
	utySet2(SS2_Prim3D)

	utySystemStarted = TRUE

	opUpdateSettings()

	soundEventPlayMusic(SOUND_FRONTEND_TRACK)

	feScreenStart(ghMainRegion, "Main_game_screen")
	mouseCursorShow()

	if (demDemoRecording) #if recording a demo
		sprintf(demDemoFilename + strlen(demDemoFilename), "%ux%u.dem", MAIN_WindowWidth, MAIN_WindowHeight)
		dbgMessagef("Recording demo '%s'.", demDemoFilename)
		determCompPlayer = TRUE  #computer player must be deterministic to record demos
		demRecordStart(demDemoFilename, utyPreDemoStateSaveCB)
	elif (demDemoPlaying) #if playing a demo
		sprintf(demDemoFilename + strlen(demDemoFilename), "%ux%u.dem", MAIN_WindowWidth, MAIN_WindowHeight)
		if (fileExists(demDemoFilename, 0))
			demPlayStart(demDemoFilename, utyPreDemoStateLoadCB, utyDemoFinishedCB)
		else
			dbgMessagef("Demo '%s' not found.", demDemoFilename)
			demDemoPlaying = FALSE

	utySet(SS2_SystemStarted)  #!!! leave this at the end of this function
	return(NULL)  #success, return no error


# SDL event handling for the application
HandleEvent (sdl_event)
    switch sdl_event.type
	case SDL_ACTIVEEVENT: # IntroActivateMe | IntroDeactivateMe | ActivateMe | DeactivateMe
	case SDL_KEYUP: # SDLK_ESCAPE|SDLK_F11|SDLK_F12|keyPressUp
	case SDL_KEYDOWN: # keyPressDown(keyLanguageTranslate();
	case SDL_USEREVENT: # CommandProcess (wtf?)
	case SDL_MOUSEBUTTONDOWN: # keyPressDown(LMOUSE_DOUBLE|LMOUSE_BUTTON|MMOUSE_DOUBLE|MMOUSE_BUTTON|RMOUSE_DOUBLE|RMOUSE_BUTTON)
	case SDL_MOUSEBUTTONUP: # keyPressUp(LMOUSE_BUTTON|LMOUSE_DOUBLE|MMOUSE_BUTTON|MMOUSE_DOUBLE|RMOUSE_BUTTON|RMOUSE_DOUBLE)
	case SDL_QUIT: # WindowsCleanup SDL_PushEvent(SDL_QUIT)


def InitWindow():
	# create a window (Window created in renderer initialization..)

    mainDevStatsInit()
    rinEnumerateDevices()

	d3dToSelect = ""

	if mainAutoRenderer and mainGLToSelect:
        if selectedDEVICE:
			d3dToSelect = ""
        else:
			deviceToSelect = mainDeviceToSelect
			d3dToSelect = mainD3DToSelect

        if not selectedGL:
			glToSelect = mainGLToSelect

	rinDevCRC = rinDeviceCRC()
    if opDeviceCRC != rinDevCRC:
        opDeviceIndex = -1
        if mainAutoRenderer:
            opDeviceCRC = rinDeviceCRC()
            mainForceSoftware = True

	# successfully re-using previous device
	# re-use previous devcaps
	gDevcaps = loadedDevcaps

	if gDevcaps == 0xFFFFFFFF:
		gDevcaps = 0

	gDevcaps2 = loadedDevcaps2

	if gDevcaps2 == 0xFFFFFFFF:
		gDevcaps2 = 0

    if not glCapLoadOpenGL(glToSelect):
        mainSetupSoftware()
        utyForceTopmost(fullScreen)
        mainRescaleMainWindow()

        if not glCapLoadOpenGL(glToSelect):
            raise "Fatal Error: Couldn't initialize default rendering system"

	mainDeviceToSelect = deviceToSelect
    mainGLToSelect = glToSelect

    glCapStartup()

	if deviceToSelect == "d3d":
        mainReinitRenderer = 2

    if RGL:
        if fullScreen:
            rglFeature(RGL_FULLSCREEN)
        else:
            rglFeature(RGL_WINDOWED)

        if mainSoftwareDirectDraw:
            rglFeature(RGL_HICOLOR)
        else:
            rglFeature(RGL_TRUECOLOR)

        if slowBlits:
            rglFeature(RGL_SLOWBLT)
        else:
            rglFeature(RGL_FASTBLT)

        if accelFirst:
            rglSelectDevice("fx", "")
            lodScaleFactor = 1.0

		if deviceToSelect:
            rglSelectDevice(deviceToSelect, d3dToSelect)
            if deviceToSelect == "sw":
                lodScaleFactor = 1.0
    else:
        lodScaleFactor = 1.0
