
enum RSF  // region status flags
{
	ReallyDirty			= 0x0001,  // Draw the region and all its children guaranteed
	CantFocusTo			= 0x0002,  // Can't focus to this region ever
	RegionDisabled		= 0x0004,  // region is disabled, don't pass any info to it
	DrawThisFrame		= 0x0008,  // draw on this frame
	MouseCapture		= 0x0010,  // region has mouse input focus
	KeyCapture			= 0x0020,  // region has keyboard input focus and will be notified of all key events
	ToBeDeleted			= 0x0040,  // region has been deleted
	Processing			= 0x0080,  // this region currently in processing
	PriorityRegion		= 0x0100,  // this region will be on top of sibling regions
	CurrentSelected		= 0x0200,  // the region has input focus
	ScenarioList		= 0x0400,  // the region is a scenario list
	MouseInside			= 0x0800,  // mouse inside region
	LeftPressed			= 0x1000,  // centre mouse pressed state
	RightPressed		= 0x2000,  // right mouse pressed state
	CentrePressed		= 0x4000,  // left mouse pressed state
	KeyPressed			= 0x8000,  // current key state for this region
}

enum RPE  // region processor function event messages (pass these as a filter on creation)
{
	Enter				= 0x00000001,  // entering region
	Exit				= 0x00000002,  // exiting region
	EnterHoldLeft		= 0x00000004,  // entering region with a button pressed
	EnterHoldRight		= 0x00000008,
	EnterHoldCentre		= 0x00000010,
	ExitHoldLeft		= 0x00000020,  // exiting region with a button pressed
	ExitHoldRight		= 0x00000040,
	ExitHoldCentre		= 0x00000080,
	WheelUp				= 0x00000100,  // mouse wheel motion
	WheelDown			= 0x00000200,
	HoldLeft			= 0x00000400,  // button held
	HoldRight			= 0x00000800,
	HoldCentre			= 0x00001000,
	PressLeft			= 0x00002000,  // button pressed
	PressRight			= 0x00004000,
	PressCentre			= 0x00008000,
	ReleaseLeft			= 0x00010000,  // mouse button released
	ReleaseRight		= 0x00020000,
	ReleaseCentre		= 0x00040000,
	KeyDown				= 0x00080000,  // key pressed
	KeyUp				= 0x00100000,  // key released
	KeyRepeat			= 0x00200000,
	KeyHold				= 0x00400000,
//	MouseMoveRel		= 0x00800000,
//	MouseMoveAbs		= 0x01000000,
	DoubleLeft			= 0x00800000,  // double-click left button
	DoubleRight			= 0x01000000,  // double-click right button
	DoubleCentre		= 0x02000000,  // bouble-click centre button

	DrawFunctionAdded	= 0x10000000,
	ModalBreak			= 0x40000000,  // process no parents of this region
	DrawEveryFrame		= 0x80000000,  // draw this region every frame
	//composite event filters for common region types
	LeftClick			= PressLeft | ReleaseLeft,
	RightClick			= PressRight | ReleaseRight,
	LeftClickButton		= LeftClick | EnterHoldLeft | ExitHoldLeft,
	RightClickButton	= RightClick | EnterHoldRight | ExitHoldRight,
}

enum RPM
{
	PressRelease		= 0x0007E000,  // mask for mouse press/release
	MouseEvents			= 0x0007FFFF,  // mask for all mouse events
	KeyEvent			= 0x00780000,  // mask for all key events
	AllEvents			= 0x01FFFFFF,  // mask for all events
}

enum RPR  // region process function return value flags
{
	Redraw		= 0x00002000,  // redraw later this frame
	Continue	= 0x00400000,  // continue to process parent nodes
}

enum REG//generic definitions
{
	NumberKeys				= 4           // max number of keys in validation sequence
	ValidationKey			= 0xF1AB4A55
	RenderEventsDefault		= 512         // default number of loggable render events
	TaskFrequency			= 16          // process regions every update frame
	TaskFrequencyOPF		= 1           // process regions every rendering frame
	TaskStackSize			= 100000      // size of region processing task stack
	OutlineColor			= colRGB(10, 10, 30)  //color of outlines
}

//pointers to region functions
alias void function(Region*) RegionDrawFunction;
alias uint function(Region*, short, uint, uint) RegionFunction;

//structure for a region, the base element of the front end
struct Region
{
	Rectangle rect;						// rectangle defining limits of region
	regiondrawfunction drawFunction;	// render function for region
	regionfunction processFunction;		// logic processing function for region
	Region* parent, child;				// region list links
	Region* previous, next;
	uint flags;							// region control flags (see above)
	ushort status;						// status bits (32 bits not enough)
	short nKeys;
	keyindex[REG_NumberKeys] key;		// accelerator key sequence
	int userID;							// user-assigned ID for processing
	//uint validationKey;				// used for validation of structure integrity
	uint tabstop;						// tabstop for key navigation
	LinkedList cutouts;
	uint[2] drawstyle;
	uint lastframedrawn;
	void* atom;
}