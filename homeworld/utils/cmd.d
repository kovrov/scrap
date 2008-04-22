
// option entity pattern: mask, name, action, help
void print_help(string str)
{
    sdword index, length;

    //calc length of help string
    length = strlen("Invalid or unrecognised command line option: '%s'\n");
    length += strlen(str);
    foreach (opt; opts)
    {
        if (!(opt.flags & VISIBLE))
            continue;

        if (opt.helpString == null)
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

    if ((gHelpString = malloc(length)) == null)              //allocate string
    {
        /*MessageBox(null, "Cannot allocate memory for help.", "Command-Line Usage", MB_OK | MB_APPLMODAL);*/
        fprintf(stderr, "Cannot allocate memory for help.\n");
        return;
    }

    //copy all help strings into one
    sprintf(gHelpString, "Invalid or unrecognised command line option: '%s'\n", str);
    foreach (opt; opts)
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

        foreach (opt; opts)
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

	Option[string] opts = [
	// DEBUGGING OPTIONS
		// name            action    dest                  help
		"debug"[]:         enable  (&DebugWindow,         "Enable debug window."),
		"nodebugint":      disable (&dbgInt3Enabled,      "Fatal errors don't genereate an int 3 before exiting."),
		"debugtofile":     enable  (&debugToFile,         "output debugging info to a file."),
		"rancallerdebug":  enable  (&ranCallerDebug,      "debug non-deterministic calling of random numbers."),
		"autosavedebug":   enable  (&autoSaveDebug,       "autosaves game frequently"),
	// SYSTEM OPTIONS
		// name          action  dest                  validator   help
		"heap":            set (&MemoryHeapSize,       &memsize,  "<n> - Sets size of global memory heap to [n]."),  // 1 argument of size_t
		"bigoverride",     set (&fileOverrideBigPath,  &path,     "<path> - Sets path to search for opening files."),  // 1 argument of string
		"cdpath",          set (&fileCDROMPath,        &path,     "<path> - Sets path to CD-ROM in case of ambiguity."),  // 1 argument of string
		"settingspath",    set (&fileUserSettingsPath, &path,     "<path> - Sets the path to store settings, saved games, and screenshots (defaults to ~/.homeworld)."),  // 1 argument of string
		// name            action    dest                  help
		"freemouse",       disable (&startupClipMouse,    "Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."),
		"ignorebigfiles",  enable  (&IgnoreBigfiles,      "don't use anything from bigfile(s)"),
		"logfileloads",    enable  (&LogFileLoads,        "create log of data files loaded"),
/+
    Option(VISIBLE, "PROCESSOR OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
	Option(VISIBLE,     "enableSSE",         null,                   &mainAllowKatmai,  true,  "allow use of SSE if support is detected."),
	Option(VISIBLE,     "forceSSE",          null,                   &mainForceKatmai,  true,  "force usage of SSE even if determined to be unavailable."),
	Option(VISIBLE,     "enable3DNow",       null,                   &mainAllow3DNow,   true,  "allow use of 3DNow! if support is detected."),

    Option(VISIBLE, "SOUND OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    Option(VISIBLE,     "noSound",           null,                   &enableSFX,        false, "turn all sound effects off."),
    Option(VISIBLE,     "noSpeech",          null,                   &enableSpeech,     false, "turn all speech off"),
    Option(VISIBLE,     "dsound",            null,                   &useDSound,        true,  "forces mixer to write to DirectSound driver, even if driver reports not certified."),
    Option(VISIBLE,     "dsoundCoop",        null,                   &coopDSound,       true,  "switches to co-operative mode of DirectSound (if supported) to allow sharing with other applications."),
    Option(VISIBLE,     "waveout",           null,                   &useWaveout,       true,  "forces mixer to write to Waveout even if a DirectSound supported object is available."),
    Option(VISIBLE,     "reverseStereo",     null,                   &reverseStereo,    true,  "swap the left and right audio channels."),

    Option(VISIBLE, "DETAIL OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable           value   help
	Option(VISIBLE,     "rasterSkip",        EnableRasterSkip,        null,              0,     "enable interlaced display with software renderer."),
    Option(VISIBLE,     "noBG",              null,                   &showBackgrounds,   false, "disable display of galaxy backgrounds."),
    Option(VISIBLE,     "noFilter",          null,                   &texLinearFiltering,false, "disable bi-linear filtering of textures."),
    Option(VISIBLE,     "noSmooth",          null,                   &enableSmoothing,   false, "do not use polygon smoothing."),
    Option(VISIBLE,     "nilTexture",        null,                   &GLOBAL_NO_TEXTURES,true,  "don't ever load textures at all."),
    Option(VISIBLE,     "noEffects",         null,                   &etgEffectsEnabled, false, "disable all effects (Debug only)."),
    Option(VISIBLE,     "NoFETextures",      null,                   &fetEnableTextures, false, "turns off front end textures"),
    Option(VISIBLE,     "stipple",           null,                   &enableStipple,     true,  "enable stipple alpha with software renderer."),
    Option(VISIBLE,     "noShowDamage",      null,                   &gShowDamage,       false, "Disables showing ship damage effects."),

    Option(VISIBLE, "VIDEO MODE OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    Option(VISIBLE,     "safeGL",            null,                   &mainSafeGL,       true,  "don't use possibly buggy optimized features of OpenGL for rendering."),
	Option(VISIBLE,     "triple",            EnableDoubleIsTriple,    null,             0,     "use when frontend menus are flickering madly."),
    Option(VISIBLE,     "nodrawpixels",      null,                   &mainNoDrawPixels, true,  "use when background images don't appear while loading."),
    Option(VISIBLE,     "noswddraw",         null,                   &mainSoftwareDirectDraw, false, "don't use DirectDraw for the software renderer."),
    Option(VISIBLE,     "noglddraw",         null,                   &mainDirectDraw,   false, "don't use DirectDraw to setup OpenGL renderers."),
    Option(VISIBLE,     "sw",                null,                   &mainForceSoftware,true,  "reset rendering system to defaults at startup."),
    Option(0,           "noSavedMode",       null,                   &mainAutoRenderer, false, "disable recovery of previous display mode."),
	Option(VISIBLE,     "noFastFE",          DisableFastFrontend,     null,             0,     "disable fast frontend rendering."),
    Option(VISIBLE,     "fullscreen",        null,                   &fullScreen,       true,  "display fullscreen with software renderer (default)."),
    Option(VISIBLE,     "window",            null,                   &fullScreen,       false, "display in a window."),
    Option(VISIBLE,     "noBorder",          null,                   &showBorder,       false, "no border on window."),
    Option(0,           "d3dDeviceCRC",      null,                   &mainOutputCRC,    true,  "generate d3dDeviceCRC.txt for video troubleshooting."),
    Option(0,           "minny",             EnableMiniRes,           null,             0,     "run at 320x240 resolution."),
	Option(VISIBLE,     "640",               EnableLoRes,             null,             0,     "run at 640x480 resolution (default)."),
	Option(VISIBLE,     "800",               EnableHiRes,             null,             0,     "run at 800x600 resolution."),
	Option(VISIBLE,     "1024",              EnableMegaRes,           null,             0,     "run at 1024x768 resolution."),
	Option(VISIBLE,     "1280",              EnableUltraRes,          null,             0,     "run at 1280x1024 resolution."),
	Option(VISIBLE,     "1600",              EnableInsaneRes,         null,             0,     "run at 1600x1200 resolution."),
//	Option(VISIBLE,     "d16",               Enable16Bit,             null,             0,     "run in 16 bits of colour."),
//	Option(VISIBLE,     "d24",               Enable24Bit,             null,             0,     "run in 24 bits of colour."),
//	Option(VISIBLE,     "d32",               Enable32Bit,             null,             0,     "run in 32 bits of colour."),
//	Option(VISIBLE,     "truecolor",         null,                   &trueColor,        true,  "try 24bit modes before 15/16bit."),
//	Option(VISIBLE,     "slowBlits",         null,                   &slowBlits,        true,  "use slow screen blits if the default is buggy."),
    Option(VISIBLE|ARG, "device",            SelectDevice,            null,             0,     "<dev> - select an rGL device by name, eg. sw, fx, d3d."),
//	Option(VISIBLE,     "gl",                SelectMSGL,             &selectedGL,       true,  "select default OpenGL as renderer."),
//	Option(VISIBLE,     "d3d",               SelectD3D,               null,             0,     "select Direct3D as renderer."),
    Option(VISIBLE,     "nohint",            null,                   &mainNoPerspective,true,  "disable usage of OpenGL perspective correction hints."),
    Option(0,           "noPause",           null,                   &noPauseAltTab,    true,  "don't pause when you alt-tab."),
    Option(0,           "noMinimize",        null,                   &noMinimizeAltTab, true,  "don't minimize when you alt-tab."),

    Option(VISIBLE, "CHEATS AND SHORTCUTS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    Option(VISIBLE,     "cheapShips",        null,                   &cmCheapShips,     true,  "ships only cost 1 RU."),
    Option(VISIBLE|ARG, "sensorLevel",       InitialSensorLevelSet,   null,             0,     "<n> - set initial sensors level (0.. 2).  Default is 0."),
    Option(VISIBLE,     "noCompPlayer",      null,                   &noDefaultComputerPlayer, true, "disable default computer players"),
    Option(VISIBLE,     "notactics",         null,                   &tacticsOn,        false, "Disables tactics."),
    Option(VISIBLE,     "noretreat",         null,                   &noRetreat,        true,  "disables the 'retreat' feature of tactics"),
    Option(0,           "disableAVI",        null,                   &enableAVI,        false, "don't display intro sequences."),

    Option(VISIBLE, "VISUALIZATION", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback               variable            value   help
    Option(VISIBLE,     "dockLines",         null,                 &dockLines,          true,  "how dock lines."),
    Option(VISIBLE,     "gunLines",          null,                 &gunLines,           true,  "how gun lines."),
    Option(VISIBLE,     "lightLines",        null,                 &RENDER_LIGHTLINES,  true,  "how light lines (Debug only)."),
    Option(VISIBLE,     "boxes",             null,                 &RENDER_BOXES,       true,  "ender bounding bowties on the ships."),
    Option(VISIBLE,     "textFeedback",      null,                 &enableTextFeedback, true,  "nable text feedback for in game commands."),
    Option(VISIBLE,     "specialTextures",   null,                 &trSpecialTextures,  true,  "nable special debugging textures."),
    Option(VISIBLE,     "morphDebug",        null,                 &meshMorphDebug,     true,  "nable debugging of morphed mesh rendering code."),
    Option(VISIBLE|ARG, "lodScaleDebug",     EnableLodScaleDebug,   null,               0,     "nable fixing a LOD scale factor."),
    Option(VISIBLE,     "focusRoids",        null,                 &mrCanFocusRoids,    true,  "nable focussing on asteroids and dust clouds."),
    Option(VISIBLE,     "showExtents",       null,                 &pieVisualizeExtents,true,  "raw elliptical universe extents."),
    Option(VISIBLE,     "loadFreeLog",       null,                 &univLoadFreeLog,    true,  "nable logging of what was loaded and freed between missions."),
    Option(VISIBLE,     "NoBind",            null,                 &bkDisableKeyRemap,  true,  "isable key bindings so that debug keys work."),
    Option(0,           "NoBind",            null,                 &bkDisableKeyRemap,  true,  "isable key bindings so that debug keys work."),

    Option(VISIBLE, "COMPUTER PLAYER AND STATS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    Option(VISIBLE,     "aiplayerLog",       null,                   &aiplayerLogEnable,true,  "enable AI Player Logging"),
    Option(VISIBLE,     "determCompPlayer",  null,                   &determCompPlayer, true,  "makes computer players deterministic"),
    Option(VISIBLE,     "gatherStats",       EnableGatherStats,      &gatherStats,      true,  "enable gathering of stats"),
    Option(VISIBLE|ARG, "showStatsFight",    EnableShowStatsFight,    null,             0,     "=<i,j> to show stats fight i,j"),
    Option(VISIBLE|ARG, "showStatsFancyFight",EnableShowStatsFancyFight,null,           0,     "=filename.script"),

    Option(VISIBLE, "NETWORK PLAY", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback             variable           value        help
    Option(VISIBLE,     "captaincyLogOff",   null,               &captaincyLogEnable,false,      "turns off captaincy log file"),
    Option(VISIBLE,     "captaincyLogOn",    null,               &captaincyLogEnable,true,       "turns on captaincy log file"),
    Option(VISIBLE,     "logOff",            null,               &logEnable,         LOG_OFF,    "turns of network logging file"),
    Option(VISIBLE,     "logOn",             null,               &logEnable,         LOG_ON,     "turns network logging file on"),
    Option(VISIBLE,     "logOnVerbose",      null,               &logEnable,         LOG_VERBOSE,"turns verbose network logging file on"),
    Option(VISIBLE|ARG, "logFilePath",       SpecifyLogFilePath,  null,              0,          "=filepath.txt"),
	Option(VISIBLE,     "debugSync",         EnableDebugSync,     null,              0,          "autosaves game frequently, records packets, logonverbose"),
    Option(0,           "noWon",             null,               &SecretWON,         true,       "no WON stuff"),
    Option(VISIBLE,     "forceLAN",          null,               &forceLAN,          true,       "allow LAN play regardless of version"),
    Option(0,           "noAuth",            null,               &noAuthorization,   true,       "Disables WON Login"),
    Option(0,           "shortWon",          null,               &ShortCircuitWON,   true,       "short circuit WON stuff"),
    Option(0,           "logOff",            null,               &logEnable,         LOG_OFF,    "turns of network logging file"),
    Option(0,           "logOn",             null,               &logEnable,         LOG_ON,     "turns network logging file on"),
    Option(0,           "logOnVerbose",      null,               &logEnable,         LOG_VERBOSE,"turns verbose network logging file on"),
    Option(ARG,         "logFilePath",       SpecifyLogFilePath,  null,              0,          "=filepath.txt"),
	Option(0,           "shortWon",          null,               &ShortCircuitWON,   true,       "short circuit WON stuff"),
    Option(VISIBLE,     "statLogOn",         null,               &statLogOn,         true,       "generates game stats log file"),
    Option(VISIBLE|ARG, "BryceAndDrewAreGods",syncDumpInit,       null,              0,          "=<X>!<Y>   X = size of SyncDumpWindow  Y = granularity in universe Frames"),

    Option(VISIBLE, "NIS OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
	Option(VISIBLE,     "testNIS",           TestNISSet,              null,             0,     "<nisFile> - enables NIS testing mode using [nisFile]."),
	Option(VISIBLE,     "testNISScript",     TestNISScriptSet,        null,             0,     "<scriptFile> - enables NIS testing mode using [scriptFile]."),
    Option(VISIBLE,     "nisCounter",        null,                   &nisPrintInfo,     true,  "display nis time index info by default."),
    Option(VISIBLE,     "nisNoLockout",      null,                   &nisNoLockout,     true,  "don't lock out the interface when playing an NIS."),

    Option(VISIBLE, "RECORDED DEMOS", null, null, 0, null),//-----------------------------------------------------
//	 flag                param               callback                 variable          value   help
    Option(VISIBLE|ARG, "demoRecord",        EnableDemoRecord,        null,             0,     "<fileName> - record a demo."),
    Option(VISIBLE|ARG, "demoPlay",          EnableDemoPlayback,      null,             0,     "<fileName> - play a demo."),
    Option(VISIBLE,     "packetRecord",      EnablePacketRecord,     &recordPackets,    true,  "record packets of this multiplayer game"),
    Option(VISIBLE,     "packetPlay",        EnablePacketPlay,       &playPackets,      true,  "<fileName> - play back packet recording"),
	Option(0,           "packetRecord",      EnablePacketRecord,     &recordPackets,    true,  "record packets of this multiplayer game"),
	Option(0,           "packetPlay",        EnablePacketPlay,       &playPackets,      true,  "<fileName> - play back packet recording"),

    Option(VISIBLE,     "compareBigfiles",   null,                   &CompareBigfiles,  true,  "file by file, use most recent (bigfile/filesystem)"),
    Option(VISIBLE,     "disableAutoDemos",  null,                   &demAutoDemo,      false, "don't automatically play demos."),
    Option(VISIBLE|ARG, "autoDemoWait",      AutoDemoWaitSet,         null,             0,     "<seconds> - time to wait on main screen before starting a demo."),
    Option(VISIBLE,     "disableFakeRenders", null,                  &demFakeRenders,   false, "disable feature where playback will try to keep up with recorded demo."),

    Option(VISIBLE, "TEXTURES", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    Option(VISIBLE,     "nopal",             null,                   &mainNoPalettes,   true,  "disable paletted texture support."),
    Option(0,           "allowPacking",      null,                   &mainAllowPacking, true,  "use the packed textures if available (default)."),
    Option(VISIBLE,     "disablePacking",    null,                   &mainAllowPacking, false, "don't use the packed textures if available."),
    Option(VISIBLE,     "onlyPacking",       null,                   &mainOnlyPacking,  true,  "only display packed textures."),

    Option(VISIBLE, "MISC OPTIONS", null, null, 0, null),//-----------------------------------------------------
//	 flag          param               callback          variable                 value   help
    Option(0,           "smCentreCamera",    null,            &smCentreWorldPlane,      false, "centres the SM world plane about 0,0,0 rather than the camera."),
    Option(VISIBLE,     "noPlug",            null,            &rndShamelessPlugEnabled, false, "don't display relic logo on pause."),
    Option(0,           "closeCaptioned",    null,            &subCloseCaptionsEnabled, true,  "close captioned for the hearing impared."),
    Option(VISIBLE,     "pilotView",         null,            &pilotView,               true,  "enable pilot view.  Focus on single ship and hit Q to toggle."),
+/
	];
}
