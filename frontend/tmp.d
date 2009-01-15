enum VKEY
{
// Modifier keys	
	Control       = 0x11,
	Shift         = 0x10,
	//AltGr
	Alt           = 0x12,
	//Command/Meta (Apple/MIT/Sun keyboards)
	LeftWindows   = 0x5B,  // super?
	RightWindows  = 0x5C,  // super?
	//Fn (compact keyboards)
	LeftShift     = 0xA0,
	RightShift    = 0xA1,
	LeftControl   = 0xA2,
	RightControl  = 0xA3,
// Lock keys	
	CapsLock      = 0x14,
	NumLock       = 0x90,
	ScrollLock    = 0x91,
// Navigation	
	LeftArrow     = 0x25,
	UpArrow       = 0x26,
	RightArrow    = 0x27,
	DownArrow     = 0x28,
	PageUp        = 0x21,
	PageDown      = 0x22,
	End           = 0x23,
	Home          = 0x24,
// Editing	
	Enter         = 0x0D,  // Return
	Backspace     = 0x08,
	Insert        = 0x2D,
	Delete        = 0x2E,
	Tab           = 0x09,
	Spacebar      = 0x20,
// Misc.	
	PrintScreen   = 0x2C,
	Print         = 0x2A,
	PauseBreak    = 0x13,
	Break         = 0x03,  // cancel
	Escape        = 0x1B,
	LeftMenu      = 0xA4,
	RightMenu     = 0xA5,
// numeric
	Num_0         = 0x60,
	Num_1         = 0x61,
	Num_2         = 0x62,
	Num_3         = 0x63,
	Num_4         = 0x64,
	Num_5         = 0x65,
	Num_6         = 0x66,
	Num_7         = 0x67,
	Num_8         = 0x68,
	Num_9         = 0x69,
	Multiply      = 0x6A,
	Add           = 0x6B,
	Separator     = 0x6C,
	Subtract      = 0x6D,
	Decimal       = 0x6E,
	Divide        = 0x6F,
// Function
	F1            = 0x70,
	F2            = 0x71,
	F3            = 0x72,
	F4            = 0x73,
	F5            = 0x74,
	F6            = 0x75,
	F7            = 0x76,
	F8            = 0x77,
	F9            = 0x78,
	F10           = 0x79,
	F11           = 0x7A,
	F12           = 0x7B,
	F13           = 0x7C,
	F14           = 0x7D,
	F15           = 0x7E,
	F16           = 0x7F,
	F17           = 0x80,
	F18           = 0x81,
	F19           = 0x82,
	F20           = 0x83,
	F21           = 0x84,
	F22           = 0x85,
	F23           = 0x86,
	F24           = 0x87,
// Power management (Power, Sleep, Wake)
	Sleep,        = 0x5F,
// Language input
	Kana_mode     = 0x15,
	Hangul_mode   = 0x15,
	Junja_mode    = 0x17,
	final_mode    = 0x18,
	Hanja_mode    = 0x19,
	Kanji_mode    = 0x19,
	CONVERT       = 0x1C,
	NONCONVERT    = 0x1D,
	ACCEPT        = 0x1E,
	mode_change   = 0x1F,
	Process       = 0xE5,
// common
	key_0         = 0x30,
	key_1         = 0x31,
	key_2         = 0x32,
	key_3         = 0x33,
	key_4         = 0x34,
	key_5         = 0x35,
	key_6         = 0x36,
	key_7         = 0x37,
	key_8         = 0x38,
	key_9         = 0x39,
	A             = 0x41,
	B             = 0x42,
	C             = 0x43,
	D             = 0x44,
	E             = 0x45,
	F             = 0x46,
	G             = 0x47,
	H             = 0x48,
	I             = 0x49,
	J             = 0x4A,
	K             = 0x4B,
	L             = 0x4C,
	M             = 0x4D,
	N             = 0x4E,
	O             = 0x4F,
	P             = 0x50,
	Q             = 0x51,
	R             = 0x52,
	S             = 0x53,
	T             = 0x54,
	U             = 0x55,
	V             = 0x56,
	W             = 0x57,
	X             = 0x58,
	Y             = 0x59,
	Z             = 0x5A,
	// oem
	OEM_1         = 0xBA,  // ;:
	OEM_PLUS      = 0xBB,  // =+
	OEM_COMMA     = 0xBC   // ,	
	OEM_MINUS     = 0xBD,  // -_
	OEM_PERIOD    = 0xBE,  // .	
	OEM_2         = 0xBF,  // /?
	OEM_3         = 0xC0,  // `~
	OEM_4         = 0xDB,  // [{
	OEM_5         = 0xDC,  // \|
	OEM_6         = 0xDD,  // ]}
	OEM_7         = 0xDE,  //"'	
	OEM_8         = 0xDF,
	OEM_102       = 0xE2,  // <\

	// rest
	Left_mouse,						0x01,
	Right_mouse,					0x02,
	Middle_mouse,					0x04,
	XBUTTON1,						0x05,
	XBUTTON2,						0x06,
	Clear,							0x0C,

	Select,							0x29,
	Execute,						0x2B,
	Help                    = 0x2F,

	BROWSER_BACK = 0xA6,
	BROWSER_FORWARD = 0xA7,
	BROWSER_REFRESH = 0xA8,
	BROWSER_STOP = 0xA9,
	BROWSER_SEARCH = 0xAA,
	BROWSER_FAVORITES = 0xAB,
	BROWSER_HOME = 0xAC,
// multimedia keys
	VOLUME_MUTE = 0xAD,
	VOLUME_DOWN = 0xAE,
	VOLUME_UP = 0xAF,
	MEDIA_NEXT_TRACK = 0xB0,
	MEDIA_PREV_TRACK = 0xB1,
	MEDIA_STOP = 0xB2,
	MEDIA_PLAY_PAUSE = 0xB3,
// app
	Applications = 0x5D,
	LAUNCH_MAIL = 0xB4,
	LAUNCH_MEDIA_SELECT = 0xB5,
	LAUNCH_APP1 = 0xB6,
	LAUNCH_APP2 = 0xB7,

	PACKET,	0xE7,  // unicode keystrokes
	Attn = 0xF6,
	CrSel = 0xF7,
	ExSel = 0xF8,
	EraseEOF = 0xF9,
	Play = 0xFA,
	Zoom = 0xFB,
	PA1 = 0xFD,
	Clear = 0xFE,  // OEM
}
