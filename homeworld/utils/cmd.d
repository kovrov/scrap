//structure for command-line parsing
struct CommandOption
{
	//bool visible;                   //is this option visible by using '/?'?
	ulong flags;                      //flags for this entry.  See above for possible values.
	string parameter;                 //parameter string (begins with a slash)
	bool function(string) callback;   //function to call, null if none.  Called after variable is set.
	void* variableToModify;           //variable to modify, null if none
	ulong valueToSet;                 //value to set variable to
	string helpString;                //string printed in help screen
}

CommandOption[] opts =
[
	{VISIBLE, "DEBUGGING OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
	{VISIBLE,     "debug",             null,                   &DebugWindow,      true,  "Enable debug window."},
	{VISIBLE,     "nodebugInt",        null,                   &dbgInt3Enabled,   false, "Fatal errors don't genereate an int 3 before exiting."},
	{VISIBLE,     "debugToFile",       null,                   &debugToFile,      true,  "output debugging info to a file."},
    {0,           "debug",             null,                   &DebugWindow,      true,  "Enable debug window."},
    {0,           "nodebugInt",        null,                   &dbgInt3Enabled,   false, "Fatal errors don't genereate an int 3 before exiting."},
    {0,           "debugToFile",       null,                   &debugToFile,      true,  "output debugging info to a file."},
	{VISIBLE,     "ranCallerDebug",    null,                   &ranCallerDebug,   true,  "debug non-deterministic calling of random numbers."},
	{VISIBLE,     "autosavedebug",     EnableAutoSaveDebug,     null,             0,     "autosaves game frequently"},

    {VISIBLE, "SYSTEM OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE|ARG, "heap",              HeapSizeSet,             null,             0,     "<n> - Sets size of global memory heap to [n]."},
    {VISIBLE|ARG, "bigoverride",       fileOverrideBigPathSet,  null,             0,     "<path> - Sets path to search for opening files."},
    {VISIBLE|ARG, "CDpath",            fileCDROMPathSet,        null,             0,     "<path> - Sets path to CD-ROM in case of ambiguity."},
    {VISIBLE|ARG, "settingspath",      fileUserSettingsPathSet, null,             0,     "<path> - Sets the path to store settings, saved games, and screenshots (defaults to ~/.homeworld)."},
	{VISIBLE,     "freemouse",         null,                   &startupClipMouse, false, "Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."},
    {0,           "freemouse",         null,                   &startupClipMouse, false, "Mouse free to move about entire screen at startup.  Use <CTRL>F11 to toggle during play."},
	{VISIBLE,     "ignoreBigfiles",    null,                   &IgnoreBigfiles,   true,  "don't use anything from bigfile(s)"},
    {VISIBLE,     "logFileLoads",      EnableFileLoadLog,      &LogFileLoads,     true,  "create log of data files loaded"},

    {VISIBLE, "PROCESSOR OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
	{VISIBLE,     "enableSSE",         null,                   &mainAllowKatmai,  true,  "allow use of SSE if support is detected."},
	{VISIBLE,     "forceSSE",          null,                   &mainForceKatmai,  true,  "force usage of SSE even if determined to be unavailable."},
	{VISIBLE,     "enable3DNow",       null,                   &mainAllow3DNow,   true,  "allow use of 3DNow! if support is detected."},

    {VISIBLE, "SOUND OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE,     "noSound",           null,                   &enableSFX,        false, "turn all sound effects off."},
    {VISIBLE,     "noSpeech",          null,                   &enableSpeech,     false, "turn all speech off"},
    {VISIBLE,     "dsound",            null,                   &useDSound,        true,  "forces mixer to write to DirectSound driver, even if driver reports not certified."},
    {VISIBLE,     "dsoundCoop",        null,                   &coopDSound,       true,  "switches to co-operative mode of DirectSound (if supported) to allow sharing with other applications."},
    {VISIBLE,     "waveout",           null,                   &useWaveout,       true,  "forces mixer to write to Waveout even if a DirectSound supported object is available."},
    {VISIBLE,     "reverseStereo",     null,                   &reverseStereo,    true,  "swap the left and right audio channels."},

    {VISIBLE, "DETAIL OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable           value   help
	{VISIBLE,     "rasterSkip",        EnableRasterSkip,        null,              0,     "enable interlaced display with software renderer."},
    {VISIBLE,     "noBG",              null,                   &showBackgrounds,   false, "disable display of galaxy backgrounds."},
    {VISIBLE,     "noFilter",          null,                   &texLinearFiltering,false, "disable bi-linear filtering of textures."},
    {VISIBLE,     "noSmooth",          null,                   &enableSmoothing,   false, "do not use polygon smoothing."},
    {VISIBLE,     "nilTexture",        null,                   &GLOBAL_NO_TEXTURES,true,  "don't ever load textures at all."},
    {VISIBLE,     "noEffects",         null,                   &etgEffectsEnabled, false, "disable all effects (Debug only)."},
    {VISIBLE,     "NoFETextures",      null,                   &fetEnableTextures, false, "turns off front end textures"},
    {VISIBLE,     "stipple",           null,                   &enableStipple,     true,  "enable stipple alpha with software renderer."},
    {VISIBLE,     "noShowDamage",      null,                   &gShowDamage,       false, "Disables showing ship damage effects."},

    {VISIBLE, "VIDEO MODE OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE,     "safeGL",            null,                   &mainSafeGL,       true,  "don't use possibly buggy optimized features of OpenGL for rendering."},
	{VISIBLE,     "triple",            EnableDoubleIsTriple,    null,             0,     "use when frontend menus are flickering madly."},
    {VISIBLE,     "nodrawpixels",      null,                   &mainNoDrawPixels, true,  "use when background images don't appear while loading."},
    {VISIBLE,     "noswddraw",         null,                   &mainSoftwareDirectDraw, false, "don't use DirectDraw for the software renderer."},
    {VISIBLE,     "noglddraw",         null,                   &mainDirectDraw,   false, "don't use DirectDraw to setup OpenGL renderers."},
    {VISIBLE,     "sw",                null,                   &mainForceSoftware,true,  "reset rendering system to defaults at startup."},
    {0,           "noSavedMode",       null,                   &mainAutoRenderer, false, "disable recovery of previous display mode."},
	{VISIBLE,     "noFastFE",          DisableFastFrontend,     null,             0,     "disable fast frontend rendering."},
    {VISIBLE,     "fullscreen",        null,                   &fullScreen,       true,  "display fullscreen with software renderer (default)."},
    {VISIBLE,     "window",            null,                   &fullScreen,       false, "display in a window."},
    {VISIBLE,     "noBorder",          null,                   &showBorder,       false, "no border on window."},
    {0,           "d3dDeviceCRC",      null,                   &mainOutputCRC,    true,  "generate d3dDeviceCRC.txt for video troubleshooting."},
    {0,           "minny",             EnableMiniRes,           null,             0,     "run at 320x240 resolution."},
	{VISIBLE,     "640",               EnableLoRes,             null,             0,     "run at 640x480 resolution (default)."},
	{VISIBLE,     "800",               EnableHiRes,             null,             0,     "run at 800x600 resolution."},
	{VISIBLE,     "1024",              EnableMegaRes,           null,             0,     "run at 1024x768 resolution."},
	{VISIBLE,     "1280",              EnableUltraRes,          null,             0,     "run at 1280x1024 resolution."},
	{VISIBLE,     "1600",              EnableInsaneRes,         null,             0,     "run at 1600x1200 resolution."},
//	{VISIBLE,     "d16",               Enable16Bit,             null,             0,     "run in 16 bits of colour."},
//	{VISIBLE,     "d24",               Enable24Bit,             null,             0,     "run in 24 bits of colour."},
//	{VISIBLE,     "d32",               Enable32Bit,             null,             0,     "run in 32 bits of colour."},
//	{VISIBLE,     "truecolor",         null,                   &trueColor,        true,  "try 24bit modes before 15/16bit."},
//	{VISIBLE,     "slowBlits",         null,                   &slowBlits,        true,  "use slow screen blits if the default is buggy."},
    {VISIBLE|ARG, "device",            SelectDevice,            null,             0,     "<dev> - select an rGL device by name, eg. sw, fx, d3d."},
//	{VISIBLE,     "gl",                SelectMSGL,             &selectedGL,       true,  "select default OpenGL as renderer."},
//	{VISIBLE,     "d3d",               SelectD3D,               null,             0,     "select Direct3D as renderer."},
    {VISIBLE,     "nohint",            null,                   &mainNoPerspective,true,  "disable usage of OpenGL perspective correction hints."},
    {0,           "noPause",           null,                   &noPauseAltTab,    true,  "don't pause when you alt-tab."},
    {0,           "noMinimize",        null,                   &noMinimizeAltTab, true,  "don't minimize when you alt-tab."},

    {VISIBLE, "CHEATS AND SHORTCUTS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE,     "cheapShips",        null,                   &cmCheapShips,     true,  "ships only cost 1 RU."},
    {VISIBLE|ARG, "sensorLevel",       InitialSensorLevelSet,   null,             0,     "<n> - set initial sensors level (0.. 2).  Default is 0."},
    {VISIBLE,     "noCompPlayer",      null,                   &noDefaultComputerPlayer, true, "disable default computer players"},
    {VISIBLE,     "notactics",         null,                   &tacticsOn,        false, "Disables tactics."},
    {VISIBLE,     "noretreat",         null,                   &noRetreat,        true,  "disables the 'retreat' feature of tactics"},
    {0,           "disableAVI",        null,                   &enableAVI,        false, "don't display intro sequences."},

    {VISIBLE, "VISUALIZATION", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback               variable            value   help
    {VISIBLE,     "dockLines",         null,                 &dockLines,          true,  "how dock lines."},
    {VISIBLE,     "gunLines",          null,                 &gunLines,           true,  "how gun lines."},
    {VISIBLE,     "lightLines",        null,                 &RENDER_LIGHTLINES,  true,  "how light lines (Debug only)."},
    {VISIBLE,     "boxes",             null,                 &RENDER_BOXES,       true,  "ender bounding bowties on the ships."},
    {VISIBLE,     "textFeedback",      null,                 &enableTextFeedback, true,  "nable text feedback for in game commands."},
    {VISIBLE,     "specialTextures",   null,                 &trSpecialTextures,  true,  "nable special debugging textures."},
    {VISIBLE,     "morphDebug",        null,                 &meshMorphDebug,     true,  "nable debugging of morphed mesh rendering code."},
    {VISIBLE|ARG, "lodScaleDebug",     EnableLodScaleDebug,   null,               0,     "nable fixing a LOD scale factor."},
    {VISIBLE,     "focusRoids",        null,                 &mrCanFocusRoids,    true,  "nable focussing on asteroids and dust clouds."},
    {VISIBLE,     "showExtents",       null,                 &pieVisualizeExtents,true,  "raw elliptical universe extents."},
    {VISIBLE,     "loadFreeLog",       null,                 &univLoadFreeLog,    true,  "nable logging of what was loaded and freed between missions."},
    {VISIBLE,     "NoBind",            null,                 &bkDisableKeyRemap,  true,  "isable key bindings so that debug keys work."},
    {0,           "NoBind",            null,                 &bkDisableKeyRemap,  true,  "isable key bindings so that debug keys work."},

    {VISIBLE, "COMPUTER PLAYER AND STATS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE,     "aiplayerLog",       null,                   &aiplayerLogEnable,true,  "enable AI Player Logging"},
    {VISIBLE,     "determCompPlayer",  null,                   &determCompPlayer, true,  "makes computer players deterministic"},
    {VISIBLE,     "gatherStats",       EnableGatherStats,      &gatherStats,      true,  "enable gathering of stats"},
    {VISIBLE|ARG, "showStatsFight",    EnableShowStatsFight,    null,             0,     "=<i,j> to show stats fight i,j"},
    {VISIBLE|ARG, "showStatsFancyFight",EnableShowStatsFancyFight,null,           0,     "=filename.script"},

    {VISIBLE, "NETWORK PLAY", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback             variable           value        help
    {VISIBLE,     "captaincyLogOff",   null,               &captaincyLogEnable,false,      "turns off captaincy log file"},
    {VISIBLE,     "captaincyLogOn",    null,               &captaincyLogEnable,true,       "turns on captaincy log file"},
    {VISIBLE,     "logOff",            null,               &logEnable,         LOG_OFF,    "turns of network logging file"},
    {VISIBLE,     "logOn",             null,               &logEnable,         LOG_ON,     "turns network logging file on"},
    {VISIBLE,     "logOnVerbose",      null,               &logEnable,         LOG_VERBOSE,"turns verbose network logging file on"},
    {VISIBLE|ARG, "logFilePath",       SpecifyLogFilePath,  null,              0,          "=filepath.txt"},
	{VISIBLE,     "debugSync",         EnableDebugSync,     null,              0,          "autosaves game frequently, records packets, logonverbose"},
    {0,           "noWon",             null,               &SecretWON,         true,       "no WON stuff"},
    {VISIBLE,     "forceLAN",          null,               &forceLAN,          true,       "allow LAN play regardless of version"},
    {0,           "noAuth",            null,               &noAuthorization,   true,       "Disables WON Login"},
    {0,           "shortWon",          null,               &ShortCircuitWON,   true,       "short circuit WON stuff"},
    {0,           "logOff",            null,               &logEnable,         LOG_OFF,    "turns of network logging file"},
    {0,           "logOn",             null,               &logEnable,         LOG_ON,     "turns network logging file on"},
    {0,           "logOnVerbose",      null,               &logEnable,         LOG_VERBOSE,"turns verbose network logging file on"},
    {ARG,         "logFilePath",       SpecifyLogFilePath,  null,              0,          "=filepath.txt"},
	{0,           "shortWon",          null,               &ShortCircuitWON,   true,       "short circuit WON stuff"},
    {VISIBLE,     "statLogOn",         null,               &statLogOn,         true,       "generates game stats log file"},
    {VISIBLE|ARG, "BryceAndDrewAreGods",syncDumpInit,       null,              0,          "=<X>!<Y>   X = size of SyncDumpWindow  Y = granularity in universe Frames"},

    {VISIBLE, "NIS OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
	{VISIBLE,     "testNIS",           TestNISSet,              null,             0,     "<nisFile> - enables NIS testing mode using [nisFile]."},
	{VISIBLE,     "testNISScript",     TestNISScriptSet,        null,             0,     "<scriptFile> - enables NIS testing mode using [scriptFile]."},
    {VISIBLE,     "nisCounter",        null,                   &nisPrintInfo,     true,  "display nis time index info by default."},
    {VISIBLE,     "nisNoLockout",      null,                   &nisNoLockout,     true,  "don't lock out the interface when playing an NIS."},

    {VISIBLE, "RECORDED DEMOS", null, null, 0, null},//-----------------------------------------------------
//	 flag                param               callback                 variable          value   help
    {VISIBLE|ARG, "demoRecord",        EnableDemoRecord,        null,             0,     "<fileName> - record a demo."},
    {VISIBLE|ARG, "demoPlay",          EnableDemoPlayback,      null,             0,     "<fileName> - play a demo."},
    {VISIBLE,     "packetRecord",      EnablePacketRecord,     &recordPackets,    true,  "record packets of this multiplayer game"},
    {VISIBLE,     "packetPlay",        EnablePacketPlay,       &playPackets,      true,  "<fileName> - play back packet recording"},
	{0,           "packetRecord",      EnablePacketRecord,     &recordPackets,    true,  "record packets of this multiplayer game"},
	{0,           "packetPlay",        EnablePacketPlay,       &playPackets,      true,  "<fileName> - play back packet recording"},

    {VISIBLE,     "compareBigfiles",   null,                   &CompareBigfiles,  true,  "file by file, use most recent (bigfile/filesystem)"},
    {VISIBLE,     "disableAutoDemos",  null,                   &demAutoDemo,      false, "don't automatically play demos."},
    {VISIBLE|ARG, "autoDemoWait",      AutoDemoWaitSet,         null,             0,     "<seconds> - time to wait on main screen before starting a demo."},
    {VISIBLE,     "disableFakeRenders", null,                  &demFakeRenders,   false, "disable feature where playback will try to keep up with recorded demo."},

    {VISIBLE, "TEXTURES", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback                 variable          value   help
    {VISIBLE,     "nopal",             null,                   &mainNoPalettes,   true,  "disable paletted texture support."},
    {0,           "allowPacking",      null,                   &mainAllowPacking, true,  "use the packed textures if available (default)."},
    {VISIBLE,     "disablePacking",    null,                   &mainAllowPacking, false, "don't use the packed textures if available."},
    {VISIBLE,     "onlyPacking",       null,                   &mainOnlyPacking,  true,  "only display packed textures."},

    {VISIBLE, "MISC OPTIONS", null, null, 0, null},//-----------------------------------------------------
//	 flag          param               callback          variable                 value   help
    {0,           "smCentreCamera",    null,            &smCentreWorldPlane,      false, "centres the SM world plane about 0,0,0 rather than the camera."},
    {VISIBLE,     "noPlug",            null,            &rndShamelessPlugEnabled, false, "don't display relic logo on pause."},
    {0,           "closeCaptioned",    null,            &subCloseCaptionsEnabled, true,  "close captioned for the hearing impared."},
    {VISIBLE,     "pilotView",         null,            &pilotView,               true,  "enable pilot view.  Focus on single ship and hit Q to toggle."},
];

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
                assert (opt.variableToModify is !null || opt.callback is !null);

                if (opt.variableToModify is !null)
                    *((udword *)(opt.variableToModify)) = opt.valueToSet;  //set a variable if applicable

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
}
