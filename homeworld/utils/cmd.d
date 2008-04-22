
// option entity pattern: mask, name, action, help
void print_help(string str)
{
    long index, length;

    //calc length of help string
    length = "Invalid or unrecognised command line option: '%s'\n".length;
    length += str.length;
    foreach (opt; opt_rules)
    {
        if (!(opt.flags & VISIBLE))
            continue;

        if (!opt.helpString)
		{
            length += strlen(opt.parameter) + 2;  // just length of comment
		}
        else  // it's a real command line option
        {
            length += strlen(opt.helpString);  // length of help string
            length += strlen(opt.parameter) + MCL_IndentSpace;  // parameter string
        }

        length += 2;  // and a newline
    }

	gHelpString.length = length;

    //copy all help strings into one
    sprintf(gHelpString, "Invalid or unrecognised command line option: '%s'\n", str);
    foreach (opt; opt_rules)
    {
        if (!(opt.flags & VISIBLE))
            continue;

        if (!opt.helpString)
        {                                                   //no help string: it's a comment
            strcat(gHelpString, "\n");
            strcat(gHelpString, opt.parameter);
            strcat(gHelpString, "\n");
        }
        else
        {                                                   //else it's a real command line option
            sprintf(gHelpString + strlen(gHelpString), "    %s%s\n", opt.parameter, opt.helpString);
            //                                            ^ MCL_IndentSpace spaces
        }
    }

    /*DialogBox(ghInstance, MAKEINTRESOURCE(IDD_CommandLine), null, CommandLineFunction);*/
    printf(gHelpString);
    free(gHelpString);  // done with string, free it
}


ulong ProcessCommandLine(string[] args)
{
    for (uint i = 1; i < args.length; i++)  // Skip the executable name.
    {
        string str = args[i];
        if (str[0] == '-')
            str[0] = '/';

        foreach (opt; opt_rules)
        {
            if (!opt.helpString)
                continue;  // don't compare against comment lines

            if (!strcasecmp(str, opt.parameter))  //if this is the correct option
            {
                assert (opt.variable is !null || opt.callback is !null);

                if (opt.variable is !null)
                    opt.variable = opt.value;  //set a variable if applicable

                if (opt.callback is !null)  //call the function associated, if applicable
                {
                    if (opt.flags & ARG)  // does the function take next token as a parameter?
                    {
                        if (++i == args.length)  // get next token
                            break;  // if no next token print usage
                        str = args[i];
                    }

                    if (!opt.callback(str))
                        break;  // error occured in parsing function
                }
                break;
            }
        }

        if (!opt.parameter)
        {
            print_help(str);  // no string found, print help
            return(-1);
        }
    }
    return(OKAY);
}



import std.stdio;

void main(string[] args)
{
	foreach (arg ; args)
	{
		writefln("%s", arg);
	}

	Option[string] opt_rules = [
	// DEBUGGING OPTIONS -----------------------------------------------------
		// name           action    dest               help
		"debug"[]:        enable  (&DebugWindow,      "Enable debug window."),
		"nodebugint":     disable (&dbgInt3Enabled,   "Fatal errors don't genereate an int 3 before exiting."),
		"debugtofile":    enable  (&debugToFile,      "output debugging info to a file."),
		"rancallerdebug": enable  (&ranCallerDebug,   "debug non-deterministic calling of random numbers."),
		"autosavedebug":  enable  (&autoSaveDebug,    "autosaves game frequently"),
	// SYSTEM OPTIONS -----------------------------------------------------
		// name           action   dest                  validator  help
		"heap":           store   (&MemoryHeapSize,      &memsize, "<n> - Sets size of global memory heap to [n]."),  // 1 argument of size_t
		"bigoverride":    store   (&fileOverrideBigPath, &path,    "<path> - Sets path to search for opening files."),  // 1 argument of string
		"cdpath":         store   (&fileCDROMPath,       &path,    "<path> - Sets path to CD-ROM in case of ambiguity."),  // 1 argument of string
		"settingspath":   store   (&fileUserSettingsPath,&path,    "<path> - Sets the path to store settings, saved games, and screenshots (defaults to ~/.homeworld)."),  // 1 argument of string
		// name           action   dest                  help
		"freemouse":      disable (&startupClipMouse,   "Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."),
		"ignorebigfiles": enable  (&IgnoreBigfiles,     "don't use anything from bigfile(s)"),
		"logfileloads":   enable  (&LogFileLoads,       "create log of data files loaded"),
    // PROCESSOR OPTIONS -----------------------------------------------------
		// name           action    dest                 help
		"enablesse":      enable  (&mainAllowKatmai,    "allow use of SSE if support is detected."),
		"forcesse":       enable  (&mainForceKatmai,    "force usage of SSE even if determined to be unavailable."),
		"enable3dnow":    enable  (&mainAllow3DNow,     "allow use of 3DNow! if support is detected."),
	// SOUND OPTIONS -----------------------------------------------------
		// name           action    dest                 help
		"nosound":        disable (&enableSFX,          "turn all sound effects off."),
		"nospeech":       disable (&enableSpeech,       "turn all speech off"),
		"dsound":         enable  (&useDSound,          "forces mixer to write to DirectSound driver, even if driver reports not certified."),
		"dsoundcoop":     enable  (&coopDSound,         "switches to co-operative mode of DirectSound (if supported) to allow sharing with other applications."),
		"waveout":        enable  (&useWaveout,         "forces mixer to write to Waveout even if a DirectSound supported object is available."),
		"reversestereo":  enable  (&reverseStereo,      "swap the left and right audio channels."),
	// DETAIL OPTIONS -----------------------------------------------------
		// name           action    dest                 help
		"rasterskip":     enable  (&mainRasterSkip,     "enable interlaced display with software renderer."),
		"nobg":           disable (&showBackgrounds,    "disable display of galaxy backgrounds."),
		"nofilter":       disable (&texLinearFiltering, "disable bi-linear filtering of textures."),
		"nosmooth":       disable (&enableSmoothing,    "do not use polygon smoothing."),
		"niltexture":     enable  (&GLOBAL_NO_TEXTURES, "don't ever load textures at all."),
		"noeffects":      disable (&etgEffectsEnabled,  "disable all effects (Debug only)."),
		"nofetextures":   disable (&fetEnableTextures,  "turns off front end textures"),
		"stipple":        enable  (&enableStipple,      "enable stipple alpha with software renderer."),
		"noshowdamage":   disable (&gShowDamage,        "Disables showing ship damage effects."),
	// VIDEO MODE OPTIONS -----------------------------------------------------
		// name           action    dest                    help
		"safegl":         enable  (&mainSafeGL,            "don't use possibly buggy optimized features of OpenGL for rendering."),
		"triple":         enable  (&mainDoubleIsTriple,    "use when frontend menus are flickering madly."),
		"nodrawpixels":   enable  (&mainNoDrawPixels,      "use when background images don't appear while loading."),
		"noswddraw":      disable (&mainSoftwareDirectDraw,"don't use DirectDraw for the software renderer."),
		"noglddraw":      disable (&mainDirectDraw,        "don't use DirectDraw to setup OpenGL renderers."),
		"sw":             enable  (&mainForceSoftware,     "reset rendering system to defaults at startup."),
		"nosavedmode":    disable (&mainAutoRenderer,      "disable recovery of previous display mode."), // hidden
		"nofastfe":       disable (&mainFastFrontend,      "disable fast frontend rendering."),
		"fullscreen":     enable  (&fullScreen,            "display fullscreen with software renderer (default)."),
		"window":         disable (&fullScreen,            "display in a window."),
		"noborder":       disable (&showBorder,            "no border on window."),
		"d3ddevicecrc":   enable  (&mainOutputCRC,         "generate d3dDeviceCRC.txt for video troubleshooting."), // hidden
		"minny":          set     (&mainWindow, [320,240], "run at 320x240 resolution."), // hidden
		"640":            set     (&mainWindow, [640,480], "run at 640x480 resolution (default)."),
		"800":            set     (&mainWindow, [800,600], "run at 800x600 resolution."),
		"1024":           set     (&mainWindow,[1024,768], "run at 1024x768 resolution."),
		"1280":           set     (&mainWindow,[1280,1024],"run at 1280x1024 resolution."),
		"1600":           set     (&mainWindow,[1600,1200],"run at 1600x1200 resolution."),
//		"d16":            set     (&MAIN_WindowDepth, 16,  "run in 16 bits of colour."),
//		"d24":            set     (&MAIN_WindowDepth, 24,  "run in 24 bits of colour."),
//		"d32":            set     (&MAIN_WindowDepth, 32,  "run in 32 bits of colour."),
//		"truecolor":      enable  (&trueColor,             "try 24bit modes before 15/16bit."),
//		"slowblits":      enable  (&slowBlits,             "use slow screen blits if the default is buggy."),
		"device":         store   (&deviceToSelect, &SelectDevice, "<n> - Sets size of global memory heap to [n]."),  // 1 argument of size_t
		"nohint":         enable  (&mainNoPerspective,      "disable usage of OpenGL perspective correction hints."),
		"nopause":        enable  (&noPauseAltTab,          "don't pause when you alt-tab."), // hidden
		"nominimize":     enable  (&noMinimizeAltTab,       "don't minimize when you alt-tab."), // hidden
	// CHEATS AND SHORTCUTS -----------------------------------------------------
		// name           action    dest                      help
		"cheapships":     enable  (&cmCheapShips,            "ships only cost 1 RU."),
		"sensorlevel":    store   (&initialSensorLevel, &toInt,"<n> - set initial sensors level (0.. 2).  Default is 0."),
		"nocompplayer":   enable  (&noDefaultComputerPlayer, "disable default computer players"),
		"notactics":      disable (&tacticsOn,               "Disables tactics."),
		"noretreat":      enable  (&noRetreat,               "disables the 'retreat' feature of tactics"),
		"disableavi":     disable (&enableAVI,               "don't display intro sequences."),
	// VISUALIZATION -----------------------------------------------------
		// name           action    dest                      help
		"docklines":      enable  (&dockLines,               "show dock lines."),
		"gunlines":       enable  (&gunLines,                "show gun lines."),
		"lightlines":     enable  (&RENDER_LIGHTLINES,       "show light lines (Debug only)."),
		"boxes":          enable  (&RENDER_BOXES,            "render bounding bowties on the ships."),
		"textfeedback":   enable  (&enableTextFeedback,      "enable text feedback for in game commands."),
		"specialtextures":enable  (&trSpecialTextures,       "enable special debugging textures."),
		"morphdebug":     enable  (&meshMorphDebug,          "enable debugging of morphed mesh rendering code."),
		"lodscaledebug":  store   (&lodDebugScaleFactor, &toFloat,"enable fixing a LOD scale factor."),
		"focusroids":     enable  (&mrCanFocusRoids,         "enable focussing on asteroids and dust clouds."),
		"showextents":    enable  (&pieVisualizeExtents,     "draw elliptical universe extents."),
		"loadfreelog":    enable  (&univLoadFreeLog,         "enable logging of what was loaded and freed between missions."),
		"nobind":         enable  (&bkDisableKeyRemap,       "disable key bindings so that debug keys work."),
		"nobind":         enable  (&bkDisableKeyRemap,       "disable key bindings so that debug keys work."), // hidden
	// COMPUTER PLAYER AND STATS -----------------------------------------------------
		// name           action    dest                      help
		"aiplayerlog":    enable  (&aiplayerLogEnable,       "enable AI Player Logging"),
		"determcompplayer":enable (&determCompPlayer,        "makes computer players deterministic"),
		"gatherstats":    enable  (&gatherStats,             "enable gathering of stats"), // noDefaultComputerPlayer=true
		"showstatsfight": store   (&showStatsFight, [&toInt,&toInt],
		                                                     "=<i,j> to show stats fight i,j"), //showStatsFightI, showStatsFightJ
		"showstatsfancyfight":store(&showStatsFancyFightScriptFile, &path, "=filename.script"), // showStatsFancyFight=true; noDefaultComputerPlayer=true;
	// NETWORK PLAY -----------------------------------------------------
		// name           action    dest/validator            help
		"captaincylogoff":disable (&captaincyLogEnable,      "turns off captaincy log file"),
		"captaincylogon": enable  (&captaincyLogEnable,      "turns on captaincy log file"),
		"logoff":         set     (&logEnable, LOG_OFF,      "turns of network logging file"),
		"logon":          set     (&logEnable, LOG_ON,       "turns network logging file on"),
		"logonverbose":   set     (&logEnable, LOG_VERBOSE,  "turns verbose network logging file on"),
		"logfilepath":    store   (&logFilePath,  &path,     "=filepath.txt"),
		"debugsync":      action ({ recordPackets = true;
		                            logEnable = LOG_VERBOSE;
		                            autoSaveDebug = true; }, "autosaves game frequently, records packets, logonverbose"),
		"nowon":          enable  (&SecretWON,               "no WON stuff"), // hidden
		"forcelan":       enable  (&forceLAN,                "allow LAN play regardless of version"),
		"noauth":         enable  (&noAuthorization,         "Disables WON Login"),  // hidden
		"shortwon":       enable  (&ShortCircuitWON,         "short circuit WON stuff"),  // hidden
		"logoff":         set     (&logEnable, LOG_OFF,      "turns of network logging file"),  // hidden
		"logon":          set     (&logEnable, LOG_ON,       "turns network logging file on"),  // hidden
		"logonverbose":   set     (&logEnable, LOG_VERBOSE,  "turns verbose network logging file on"),  // hidden
		"logfilepath":    store   (&logFilePath, &path,      "=filepath.txt"),  // hidden
		"shortwon":       enable  (&ShortCircuitWON,         "short circuit WON stuff"),  // hidden
		"statlogon":      enable  (&statLogOn,               "generates game stats log file"),
		"bryceanddrewaregods":store([&syncDumpWindowSize,&syncDumpGranularity], [&toInt,&toInt],
		                                                     "=<X>!<Y>   X = size of SyncDumpWindow  Y = granularity in universe Frames"),
	// NIS OPTIONS -----------------------------------------------------
		"testnis":        store   (&nisTestNIS, path,        "<nisFile> - enables NIS testing mode using [nisFile]."),
		"testnisscript":  store   (&nisTestScript, path,     "<scriptFile> - enables NIS testing mode using [scriptFile]."),
		"niscounter":     enable  (&nisPrintInfo,            "display nis time index info by default."),
		"nisnolockout":   enable  (&nisNoLockout,            "don't lock out the interface when playing an NIS."),
	// RECORDED DEMOS -----------------------------------------------------
		"demorecord":     store   (&demDemoFilename, &path,      "<fileName> - record a demo."), // demDemoRecording=true
		"demoplay":       store   (&demDemoFilename, &path,      "<fileName> - play a demo."), // wasDemoPlaying = demDemoPlaying = noPauseAltTab = true;
		"packetrecord":   enable  (&debugPacketRecord,           "record packets of this multiplayer game"),
		"packetplay":     store   (&recordPacketFileName, &path, "<fileName> - play back packet recording"), // transferCaptaincyDisabled=playPackets=true
		"packetrecord":   enable  (&debugPacketRecord,           "record packets of this multiplayer game"), // hidden // recordPackets=true
		"packetplay":     store   (&recordPacketFileName, &path, "<fileName> - play back packet recording"),  // hidden // transferCaptaincyDisabled=playPackets=true
		"comparebigfiles":enable  (&CompareBigfiles,             "file by file, use most recent (bigfile/filesystem)"),
		"disableautodemos":disable(&demAutoDemo,                 "don't automatically play demos."),
		"autodemowait":   store   (&demAutoDemoWaitTime,&toFloat,"<seconds> - time to wait on main screen before starting a demo."),
		"disablefakerenders":disable(&demFakeRenders,            "disable feature where playback will try to keep up with recorded demo."),
	// TEXTURES -----------------------------------------------------
		"nopal":          enable  (&mainNoPalettes,          "disable paletted texture support."),
		"allowpacking":   enable  (&mainAllowPacking,        "use the packed textures if available (default)."), // hidden
		"disablepacking": disable (&mainAllowPacking,        "don't use the packed textures if available."),
		"onlypacking":    enable  (&mainOnlyPacking,         "only display packed textures."),
	// MISC OPTIONS -----------------------------------------------------
		"smcentrecamera": disable (&smCentreWorldPlane,      "centres the SM world plane about 0,0,0 rather than the camera."), // hidden
		"noplug":         disable (&rndShamelessPlugEnabled, "don't display relic logo on pause."),
		"closecaptioned": enable  (&subCloseCaptionsEnabled, "close captioned for the hearing impared."), // hidden
		"pilotview":      enable  (&pilotView,               "enable pilot view.  Focus on single ship and hit Q to toggle."),
	];
}
