def IntroActivateMe():
	sounddeactivate(False)
	demDemoPlaying = wasDemoPlaying  # keep playing demo if it was playing when we minimized

	if utySystemStarted:
		utyClipMouse(startupClipMouse)  # optionally trap the mouse

	systemActive = True

	utyForceTopmost(fullScreen)
	SDL_ShowCursor(SDL_DISABLE)
	# make sure that the mouse is rotating properly when we come back
	utyMouseButtonsClear()

	keyClearAll()
	keyBufferClear()
	mrTacticalOverlayState(utyCapsLockToggleState())


def ActivateMe():
    sounddeactivate(False);
    demDemoPlaying = wasDemoPlaying  # keep playing demo if it was playing when we minimized

    if RGL:
        rglFeature(RGL_ACTIVATE)
        mainReinitRenderer = 2

    feRenderEverything = True

    if utySystemStarted:  # if game has started
        utyClipMouse(startupClipMouse)  # optionally trap the mouse
        taskResumeAll()  # resume all tasks

    systemActive = True

    utyForceTopmost(fullScreen)
    SDL_ShowCursor(SDL_DISABLE)
    # make sure that the mouse is rotating proper when we come back
    utyMouseButtonsClear()

    keyClearAll()
    keyBufferClear()

    hrBackgroundReinit = True
    mrTacticalOverlayState(utyCapsLockToggleState())
