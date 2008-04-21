//structure for command-line parsing
struct commandoption
{
	//bool visible;                   //is this option visible by using '/?'?
	ulong flags;                      //flags for this entry.  See above for possible values.
	string parameter;                 //parameter string (begins with a slash)
	bool function(string);            //function to call, NULL if none.  Called after variable is set.
	void* variableToModify;           //variable to modify, NULL if none
	ulong valueToSet;                 //value to set variable to
	string helpString;                //string printed in help screen
}

commandoption[] commandOptions =
[
    entryComment("DEBUGGING OPTIONS"),//-----------------------------------------------------
    entryVr("/debug",               DebugWindow, TRUE,                  " - Enable debug window."),
    entryVr("/nodebugInt",          dbgInt3Enabled,FALSE,               " - Fatal errors don't genereate an int 3 before exiting."),
    entryVr("/debugToFile",         debugToFile, TRUE,                  " - output debugging info to a file."),
    entryVrHidden("/debug",         DebugWindow, TRUE,                  " - Enable debug window."),
    entryVrHidden("/nodebugInt",    dbgInt3Enabled,FALSE,               " - Fatal errors don't genereate an int 3 before exiting."),
    entryVrHidden("/debugToFile",   debugToFile, TRUE,                  " - output debugging info to a file."),
    entryVr("/ranCallerDebug",      ranCallerDebug, TRUE,               " - debug non-deterministic calling of random numbers."),
    entryFn("/autosavedebug",       EnableAutoSaveDebug,                " autosaves game frequently"),

    entryComment("SYSTEM OPTIONS"), //-----------------------------------------------------
    entryFnParam("/heap",           HeapSizeSet,                        " <n> - Sets size of global memory heap to [n]."),
    entryFnParam("/bigoverride",    fileOverrideBigPathSet,             " <path> - Sets path to search for opening files."),
    entryFnParam("/CDpath",         fileCDROMPathSet,                   " <path> - Sets path to CD-ROM in case of ambiguity."),
    entryFnParam("/settingspath",   fileUserSettingsPathSet,            " <path> - Sets the path to store settings, saved games, and screenshots (defaults to ~/.homeworld)."),
    entryVr("/freemouse",           startupClipMouse, FALSE,            " - Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."),
    entryVrHidden("/freemouse",     startupClipMouse, FALSE,            " - Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."),
    entryVr("/ignoreBigfiles",      IgnoreBigfiles, TRUE,               " - don't use anything from bigfile(s)"),
    entryFV("/logFileLoads",        EnableFileLoadLog,LogFileLoads,TRUE," - create log of data files loaded"),

    entryComment("PROCESSOR OPTIONS"),//-----------------------------------------------------
    entryVr("/enableSSE",           mainAllowKatmai, TRUE,              " - allow use of SSE if support is detected."),
    entryVr("/forceSSE",            mainForceKatmai, TRUE,              " - force usage of SSE even if determined to be unavailable."),
    entryVr("/enable3DNow",         mainAllow3DNow, TRUE,               " - allow use of 3DNow! if support is detected."),

    entryComment("SOUND OPTIONS"),  //-----------------------------------------------------
    entryVr("/noSound",             enableSFX, FALSE,                   " - turn all sound effects off."),
    entryVr("/noSpeech",            enableSpeech, FALSE,                " - turn all speech off."),
    entryVr("/dsound",              useDSound, TRUE,                    " - forces mixer to write to DirectSound driver, even if driver reports not certified."),
    entryVr("/dsoundCoop",          coopDSound, TRUE,                   " - switches to co-operative mode of DirectSound (if supported) to allow sharing with other applications."),
    entryVr("/waveout",             useWaveout, TRUE,                   " - forces mixer to write to Waveout even if a DirectSound supported object is available."),
    entryVr("/reverseStereo",       reverseStereo, TRUE,                " - swap the left and right audio channels."),

    entryComment("DETAIL OPTIONS"), //-----------------------------------------------------
    entryFn("/rasterSkip",          EnableRasterSkip,                   " - enable interlaced display with software renderer."),
    entryVr("/noBG",                showBackgrounds, FALSE,             " - disable display of galaxy backgrounds."),
    entryVr("/noFilter",            texLinearFiltering,FALSE,           " - disable bi-linear filtering of textures."),
    entryVr("/noSmooth",            enableSmoothing, FALSE,             " - do not use polygon smoothing."),
    entryVr("/nilTexture",          GLOBAL_NO_TEXTURES,TRUE,            " - don't ever load textures at all."),
    entryVr("/noEffects",           etgEffectsEnabled,FALSE,            " - disable all effects (Debug only)."),
    entryVr("/NoFETextures",        fetEnableTextures, FALSE,           " - turns off front end textures"),
    entryVr("/stipple",             enableStipple, TRUE,                " - enable stipple alpha with software renderer."),
    entryVr("/noShowDamage",        gShowDamage, FALSE,                 " - Disables showing ship damage effects."),

    entryComment("VIDEO MODE OPTIONS"),//-----------------------------------------------------
    entryVr("/safeGL",              mainSafeGL, TRUE,                   " - don't use possibly buggy optimized features of OpenGL for rendering."),
    entryFn("/triple",              EnableDoubleIsTriple,               " - use when frontend menus are flickering madly."),
    entryVr("/nodrawpixels",        mainNoDrawPixels, TRUE,             " - use when background images don't appear while loading."),
    entryVr("/noswddraw",           mainSoftwareDirectDraw, FALSE,      " - don't use DirectDraw for the software renderer."),
    entryVr("/noglddraw",           mainDirectDraw, FALSE,              " - don't use DirectDraw to setup OpenGL renderers."),
    entryVr("/sw",                  mainForceSoftware, TRUE,            " - reset rendering system to defaults at startup."),
    entryVrHidden("/noSavedMode",   mainAutoRenderer, FALSE,            " - disable recovery of previous display mode."),
    entryFn("/noFastFE",            DisableFastFrontend,                " - disable fast frontend rendering."),
    entryVr("/fullscreen",          fullScreen, TRUE,                   " - display fullscreen with software renderer (default)."),
    entryVr("/window",              fullScreen, FALSE,                  " - display in a window."),
    entryVr("/noBorder",            showBorder, FALSE,                  " - no border on window."),
    entryVrHidden("/d3dDeviceCRC",  mainOutputCRC, TRUE,                " - generate d3dDeviceCRC.txt for video troubleshooting."),
    entryFnHidden("/minny",           EnableMiniRes,                      " - run at 320x240 resolution."),
    entryFn("/640",                 EnableLoRes,                        " - run at 640x480 resolution (default)."),
    entryFn("/800",                 EnableHiRes,                        " - run at 800x600 resolution."),
    entryFn("/1024",                EnableMegaRes,                      " - run at 1024x768 resolution."),
    entryFn("/1280",                EnableUltraRes,                     " - run at 1280x1024 resolution."),
    entryFn("/1600",                EnableInsaneRes,                    " - run at 1600x1200 resolution."),
//    entryFn("/d16",                 Enable16Bit,                        " - run in 16 bits of colour."),
//    entryFn("/d24",                 Enable24Bit,                        " - run in 24 bits of colour."),
//    entryFn("/d32",                 Enable32Bit,                        " - run in 32 bits of colour."),
//    entryVr("/truecolor",           trueColor, TRUE,                    " - try 24bit modes before 15/16bit."),
//    entryVr("/slowBlits",           slowBlits, TRUE,                    " - use slow screen blits if the default is buggy."),
    entryFnParam("/device",         SelectDevice,                       " <dev> - select an rGL device by name, eg. sw, fx, d3d."),
//    entryFV("/gl",                  SelectMSGL, selectedGL, TRUE,       " - select default OpenGL as renderer."),
//    entryFn("/d3d",                 SelectD3D,                          " - select Direct3D as renderer."),
    entryVr("/nohint",              mainNoPerspective, TRUE,            " - disable usage of OpenGL perspective correction hints."),
    entryVrHidden("/noPause",             noPauseAltTab, TRUE,                " - don't pause when you alt-tab."),
    entryVrHidden("/noMinimize",          noMinimizeAltTab, TRUE,             " - don't minimize when you alt-tab."),

    entryComment("CHEATS AND SHORTCUTS"),         //-----------------------------------------------------
    entryVr("/cheapShips",          cmCheapShips, TRUE,                 " - ships only cost 1 RU."),
    entryFnParam("/sensorLevel" ,   InitialSensorLevelSet,              " <n> - set initial sensors level (0.. 2).  Default is 0."),
    entryVr("/noCompPlayer",        noDefaultComputerPlayer, TRUE,      " - disable default computer players"),
    entryVr("/notactics",           tacticsOn, FALSE,                   " - Disables tactics."),
    entryVr("/noretreat",           noRetreat, TRUE,                    " - disables the 'retreat' feature of tactics"),
    entryVrHidden("/disableAVI",    enableAVI,FALSE,                    " - don't display intro sequences."),

    entryComment("VISUALIZATION"),  //-----------------------------------------------------
    entryVr("/dockLines",           dockLines, TRUE,                    " - show dock lines."),
    entryVr("/gunLines",            gunLines, TRUE,                     " - show gun lines."),
    entryVr("/lightLines",          RENDER_LIGHTLINES, TRUE,            " - show light lines (Debug only)."),
    entryVr("/boxes",               RENDER_BOXES, TRUE,                 " - render bounding bowties on the ships."),
    entryVr("/textFeedback",        enableTextFeedback, TRUE,           " - enable text feedback for in game commands."),
    entryVr("/specialTextures",     trSpecialTextures, TRUE,            " - enable special debugging textures."),
    entryVr("/morphDebug",          meshMorphDebug, TRUE,               " - enable debugging of morphed mesh rendering code."),
    entryFnParam("/lodScaleDebug",  EnableLodScaleDebug,                " - enable fixing a LOD scale factor."),
    entryVr("/focusRoids",          mrCanFocusRoids, TRUE,              " - enable focussing on asteroids and dust clouds."),
    entryVr("/showExtents",         pieVisualizeExtents, TRUE,          " - draw elliptical universe extents."),
    entryVr("/loadFreeLog",         univLoadFreeLog, TRUE,              " - enable logging of what was loaded and freed between missions."),
    entryVr("/NoBind",              bkDisableKeyRemap, TRUE,            " - disable key bindings so that debug keys work."),
    entryVrHidden("/NoBind",        bkDisableKeyRemap, TRUE,            " - disable key bindings so that debug keys work."),

    entryComment("COMPUTER PLAYER AND STATS"),//-----------------------------------------------------
    entryVr("/aiplayerLog",         aiplayerLogEnable, TRUE,            " - enable AI Player Logging"),
    entryVr("/determCompPlayer",    determCompPlayer, TRUE,             " - makes computer players deterministic"),
    entryFV("/gatherStats",         EnableGatherStats, gatherStats, TRUE,"- enable gathering of stats"),
    entryFnParam("/showStatsFight", EnableShowStatsFight,               "=<i,j> to show stats fight i,j"),
    entryFnParam("/showStatsFancyFight", EnableShowStatsFancyFight,     "=filename.script"),

    entryComment("NETWORK PLAY"),   //-----------------------------------------------------
    entryVr("/captaincyLogOff",     captaincyLogEnable, FALSE,          " - turns off captaincy log file" ),
    entryVr("/captaincyLogOn",      captaincyLogEnable, TRUE,           " - turns on captaincy log file" ),
    entryVr("/logOff",              logEnable, LOG_OFF,                 " - turns of network logging file"),
    entryVr("/logOn",               logEnable, LOG_ON,                  " - turns network logging file on"),
    entryVr("/logOnVerbose",        logEnable, LOG_VERBOSE,             " - turns verbose network logging file on"),
    entryFnParam("/logFilePath",    SpecifyLogFilePath,                 "=filepath.txt"),
    entryFn("/debugSync",           EnableDebugSync,                    " autosaves game frequently, records packets, logonverbose" ),
    entryVrHidden("/noWon",         SecretWON, TRUE,                    " - no WON stuff" ),
    entryVr("/forceLAN",            forceLAN, TRUE,                     " - allow LAN play regardless of version" ),
    entryVrHidden("/noAuth",        noAuthorization, TRUE,              " - Disables WON Login"),
    entryVrHidden("/shortWon",      ShortCircuitWON, TRUE,              " - short circuit WON stuff" ),
    entryVrHidden("/logOff",        logEnable, LOG_OFF,                 " - turns of network logging file"),
    entryVrHidden("/logOn",         logEnable, LOG_ON,                  " - turns network logging file on"),
    entryVrHidden("/logOnVerbose",  logEnable, LOG_VERBOSE,             " - turns verbose network logging file on"),
    entryFnParamHidden("/logFilePath",SpecifyLogFilePath,               "=filepath.txt"),
	entryVrHidden("/shortWon",      ShortCircuitWON, TRUE,              " - short circuit WON stuff" ),
    entryVr("/statLogOn",           statLogOn, TRUE,                    " - generates game stats log file"),
    entryFnParam("/BryceAndDrewAreGods", syncDumpInit,                  "=<X>!<Y>   X = size of SyncDumpWindow  Y = granularity in universe Frames"),

    entryComment("NIS OPTIONS"),    //-----------------------------------------------------
    entryFn("/testNIS" ,            TestNISSet,                         " <nisFile> - enables NIS testing mode using [nisFile]."),
    entryFn("/testNISScript",       TestNISScriptSet,                   " <scriptFile> - enables NIS testing mode using [scriptFile]."),
    entryVr("/nisCounter",          nisPrintInfo,TRUE,                  " - display nis time index info by default."),
    entryVr("/nisNoLockout",        nisNoLockout, TRUE,                 " - don't lock out the interface when playing an NIS."),

    entryComment("RECORDED DEMOS"), //-----------------------------------------------------
    entryFnParam("/demoRecord",     EnableDemoRecord,                   " <fileName> - record a demo."),
    entryFnParam("/demoPlay",       EnableDemoPlayback,                 " <fileName> - play a demo."),
    entryFV("/packetRecord",        EnablePacketRecord, recordPackets, TRUE, " - record packets of this multiplayer game"),
    entryFV("/packetPlay",          EnablePacketPlay, playPackets, TRUE," <fileName> - play back packet recording"),
    entryFVHidden("/packetRecord",  EnablePacketRecord, recordPackets, TRUE, " - record packets of this multiplayer game"),
    entryFVHidden("/packetPlay",    EnablePacketPlay, playPackets, TRUE," <fileName> - play back packet recording"),

    entryVr("/compareBigfiles",     CompareBigfiles, TRUE,              " - file by file, use most recent (bigfile/filesystem)"),
    entryVr("/disableAutoDemos",    demAutoDemo,FALSE,                  " - don't automatically play demos."),
    entryFnParam("/autoDemoWait",   AutoDemoWaitSet,                    " <seconds> - time to wait on main screen before starting a demo."),
    entryVr("/disableFakeRenders",  demFakeRenders,FALSE,               " - disable feature where playback will try to keep up with recorded demo."),

    entryComment("TEXTURES"),       //-----------------------------------------------------
    entryVr("/nopal",               mainNoPalettes, TRUE,               " - disable paletted texture support."),
    entryVrHidden("/allowPacking",  mainAllowPacking, TRUE,             " - use the packed textures if available (default)."),
    entryVr("/disablePacking",      mainAllowPacking, FALSE,            " - don't use the packed textures if available."),
    entryVr("/onlyPacking",         mainOnlyPacking, TRUE,              " - only display packed textures."),

    entryComment("MISC OPTIONS"),   //-----------------------------------------------------
    entryVrHidden("/smCentreCamera",      smCentreWorldPlane, FALSE,          " - centres the SM world plane about 0,0,0 rather than the camera."),

    entryVr("/noPlug",              rndShamelessPlugEnabled, FALSE,     " - don't display relic logo on pause."),

    entryVrHidden("/closeCaptioned",      subCloseCaptionsEnabled, TRUE,      " - close captioned for the hearing impared."),
    entryVr("/pilotView",           pilotView, TRUE, " - enable pilot view.  Focus on single ship and hit Q to toggle."),
];
