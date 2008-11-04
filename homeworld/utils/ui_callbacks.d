import widgets;

void function(widgets.Widget)[string] onCreate;

static this()
{
	onCreate = [

/*
Advanced:
	OP_BattleChatter
	OP_Voice0
	OP_Voice1
	OP_Voice2
	OP_Voice_Chatter
	OP_Voice_Commands
	OP_Voice_Status
Advanced_Options:
	MG_AlliedVictory
	MG_BountySize
	MG_CaptureCapitalShip
	MG_CratesEnabled
	MG_GameType
	MG_Hyperspace
	MG_LastMotherShip
	MG_NoFuelBurn
	MG_ResearchEnabled
	MG_StartShip
	MG_UnitCapsEnabled
	OP_CPU_Attacks
	OP_CPU_Difficulty
Advanced_Options_Change:
	MG_AlliedVictory
	MG_BountySize
	MG_CaptureCapitalShip
	MG_CratesEnabled
	MG_GameType
	MG_Hyperspace
	MG_LastMotherShip
	MG_NoFuelBurn
	MG_ResearchEnabled
	MG_StartShip
	MG_UnitCapsEnabled
	OP_CPU_Attacks
	OP_CPU_Difficulty
Advanced_Options_View:
	MG_AlliedVictory
	MG_BountySize
	MG_CaptureCapitalShip
	MG_CratesEnabled
	MG_GameType
	MG_Hyperspace
	MG_LastMotherShip
	MG_NoFuelBurn
	MG_ResearchEnabled
	MG_StartShip
	MG_UnitCapsEnabled
	OP_CPU_Attacks
	OP_CPU_Difficulty
Advanced_speech:
	OP_BattleChatter
	OP_Voice0
	OP_Voice1
	OP_Voice2
	OP_Voice_Chatter
	OP_Voice_Commands
	OP_Voice_Status
Allies_Chatting_Screen:
	InGameChatEntry
Audio:
*/
	"OP_AutoChannels": function void(widgets.Widget button)
		{
			button.checked = op.autoChannel == SOUND_MODE_AUTO;
			button.flag = DrawThisFrame;
		},
		//"onClick"
		//	delegate(ToggleButton button)
		//	{
		//		opAutoChannel = button.checked ? SOUND_MODE_AUTO : SOUND_MODE_NORM;
		//	}
/+
	"OP_DCTQuality":
		"onCreate"
			delegate(RadioButtonGroup buttons)
			{
				buttons.checked = opSoundQuality;
			}
		"onClick"
			delegate(RadioButtonGroup buttons)
			{
				opSoundQuality = buttons.checked;
			}
	"OP_Music_Volume":
		"onCreate"
			delegate(char* name, featom* atom)
			{
				udword f;
				sliderhandle shandle;
				//feToggleButtonSet(name, texLinearFiltering);
				dbgMessage("opMusicVolume() first call");
				//volumeregion = atom->region;
				shandle = (sliderhandle)atom->region;
				shandle->maxvalue = 100;
				shandle->value = opMusicVol;
				//smoothmusicvol = (real32)opMusicVol;
				f = regFilterSet(atom->region, 0);
				regFilterSet(atom->region, f | RPE_HoldLeft);
				shandle->processFunction  = opMusicVolumeProcess;
				opMusicVolumeProcess(atom->region, 0, 0, 0);
				//shandle->processFunction  = opMusicVolumeProcess;
				//AddSmoothie(&volumesmoothie);
			}
	"OP_NumChannels":
		"onCreate"
			delegate(featom *atom, regionhandle region)
			{
				drawnumchannels = NULL;
			}
		"onClick"
			delegate(featom *atom, regionhandle region)
			{
				fonthandle currentFont;
				sdword min, max;
				drawnumchannels = region;
				currentFont = fontMakeCurrent(opKeyboardFont);
				primRectSolid2(&region->rect, colBlack);
				soundGetVoiceLimits(&min, &max);
				fontPrintf (region->rect.x0, region->rect.y0, colRGB(255,200,0), "%u", opNumChannels + min);
				fontMakeCurrent(currentFont);
			}
	"OP_Num_Channels":
		"onCreate"
			delegate(char* name, featom* atom)
			{
				udword f;
				sdword min, max;
				sliderhandle shandle;
				soundGetVoiceLimits(&min, &max);
				shandle = (sliderhandle)atom->region;
				shandle->maxvalue = max - min;
				shandle->value = opNumChannels;
				f = regFilterSet(atom->region, 0);
				regFilterSet(atom->region, f | RPE_HoldLeft);
				shandle->processFunction  = opNumChannelsProcess;
				opNumChannelsProcess(atom->region, 0, 0, 0);
			}
	"OP_SFX_Volume"
		"onCreate"
			delegate(char* name, featom* atom)
			{
				udword f;
				sliderhandle shandle;
				//feToggleButtonSet(name, texLinearFiltering);
				dbgMessage("opSFXVolume() first call");
				//sfxregion = atom->region;
				shandle = (sliderhandle)atom->region;
				shandle->maxvalue = 100;
				shandle->value = opSFXVol;
				//smoothsfxvol = (real32)opSFXVol;
				f = regFilterSet(atom->region, 0);
				regFilterSet(atom->region, f | RPE_HoldLeft);
				shandle->processFunction  = opSFXVolumeProcess;
				opSFXVolumeProcess(atom->region, 0, 0, 0);
				//AddSmoothie(&sfxsmoothie);
			}

	"OP_Speaker":
		"onCreate"
			delegate(char* name, featom* atom)
			{
				feRadioButtonSet(name, opSpeakerSetting);
				opEQHelper();
			}
		"onClick"
			delegate(char* name, featom* atom)
			{
				opSpeakerSetting = (sdword)atom->pData;
				opEQHelper();
			}
	"OP_Speech_Volume":
		"onCreate"
			void opSpeechVolume(char* name, featom* atom)
			{
				udword f;
				sliderhandle shandle;
				//feToggleButtonSet(name, texLinearFiltering);
				dbgMessage("opSpeechVolume() first call");
				//speechregion = atom->region;
				shandle = (sliderhandle)atom->region;
				shandle->maxvalue = 100;
				shandle->value = opSpeechVol;
				//smoothspeechvol = (real32)opSpeechVol;
				f = regFilterSet(atom->region, 0);
				regFilterSet(atom->region, f | RPE_HoldLeft);
				shandle->processFunction  = opSpeechVolumeProcess;
				opSpeechVolumeProcess(atom->region, 0, 0, 0);
				//AddSmoothie(&speechsmoothie);
			}
+/
/*
Audio_Options:
	"OP_AutoChannels":dupe
	"OP_DCTQuality":dupe
	"OP_Music_Volume":dupe
	"OP_NumChannels":dupe
	"OP_Num_Channels":dupe
	"OP_SFX_Volume":dupe
	"OP_Speaker":dupe
	"OP_Speech_Volume":dupe
Available_Channels:
	MG_ListOfChannels
Available_Games:
	MG_ListOfGames
Basic_Options:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameNameTextEntry
	MG_GamePassword
	MG_GamePasswordConfirm
	MG_GameType
	MG_LastMotherShip
	MG_PasswordProtected
	MG_StartShip
	OP_CPU_Attacks
	OP_CPU_Difficulty
Basic_Options_Change:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameNameTextEntry
	MG_GamePassword
	MG_GamePasswordConfirm
	MG_GameType
	MG_LastMotherShip
	MG_PasswordProtected
	MG_StartShip
	OP_CPU_Attacks
	OP_CPU_Difficulty
Basic_Options_View:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameNameTextEntry
	MG_GamePassword
	MG_GamePasswordConfirm
	MG_GameType
	MG_LastMotherShip
	MG_PasswordProtected
	MG_StartShip
	OP_CPU_Attacks
	OP_CPU_Difficulty
Captain_Wait:
	MG_ChatHistoryWindow
	MG_ChatTextEntry
	MG_GameChatTextEntry
	MG_GameChatWindow
	MG_GameUserName
	MG_UserNameWindow
Channel_Chat:
	MG_ChatHistoryWindow
	MG_ChatTextEntry
	MG_UserNameWindow
ChooseServer:
	MG_ListOfServers
Computer:
	VO_Language
Connecting:
	MG_ConnectingStatus
Connection_Method:
	MG_InternetWON
	MG_LANIPX
	MG_Skirmish
Construction_manager:
	CM_Carrier1Draw
	CM_Carrier2Draw
	CM_Carrier3Draw
	CM_Carrier4Draw
	CM_LeftArrowDraw
	CM_MotherShipDraw
	CM_RightArrowDraw
	CM_Scroller
	SV_Armor
	SV_Coverage
	SV_Firepower
	SV_Maneuver
	SV_Mass
	SV_ShipView
	SV_TopSpeed
Create_Channel:
	MG_ChannelConfirmEntry
	MG_ChannelDescriptionEntry
	MG_ChannelNameEntry
	MG_ChannelPasswordEntry
	MG_ChannelProtected
Create_new_game:
	CP_RaceOne
	CP_RaceTwo
Custom_options:
	VO_Background
	VO_BitmapBackground
	VO_BitmapBullet
	VO_BitmapDamage
	VO_BitmapFilter
	VO_BitmapHitEffects
	VO_BitmapInstantTransition
	VO_BitmapMuzzle
	VO_BitmapSensorsBlobs
	VO_BitmapStipple
	VO_Bullet
	VO_Damage
	VO_Filter
	VO_Hit
	VO_InstantTransition
	VO_Muzzle
	VO_SensorsBlobs
	VO_Stipple
Equalizer:
	OP_Equalizer1
	OP_Equalizer2
	OP_Equalizer3
	OP_Equalizer4
	OP_Equalizer5
	OP_Equalizer6
	OP_Equalizer7
	OP_Equalizer8
Game_Password:
	MG_GamePasswordEntry
Game_lesson_load:
	FE_LessonGameWindowInit
	IG_TextEntryWindowInit
Game_record_save:
	FE_RecordedGameWindowInit
	IG_TextEntryWindowInit
Gameplay:
	OP_Info_Overlay
	OP_Mouse_Sensitivity
Gameplay_Options:
	OP_Info_Overlay
	OP_Mouse_Sensitivity
Horse_Race:
	HR_ChatTextEntry
InGameEqualizer:
	OP_Equalizer1
	OP_Equalizer2
	OP_Equalizer3
	OP_Equalizer4
	OP_Equalizer5
	OP_Equalizer6
	OP_Equalizer7
	OP_Equalizer8
In_Game_Key_Pool:
	OP_KeyBindingsPoolList
In_game_load:
	FE_GameWindowInit
In_game_save:
	FE_GameWindowInit
	IG_TextEntryWindowInit
Internet_Login:
	MG_FirewallButton
	MG_NameEntry
	MG_PasswordEntry
Keyboard:
	OP_KeyBindingsList
Keys:
	OP_KeyBindingsList
LAN_Login:
	MG_NameEntry
LCaptain_Wait:
	LG_ChatHistoryWindow
	LG_ChatTextEntry
	LG_GameChatTextEntry
	LG_GameChatWindow
	LG_GameUserName
	LG_UserNameWindow
LChannel_Chat:
	LG_ChatHistoryWindow
	LG_ChatTextEntry
	LG_ListOfGames
	LG_UserNameWindow
LGame_Password:
	LG_GamePasswordEntry
LLAN_Login:
	LG_LanProtocalButton
	LG_NameEntry
LLoad_a_scenario:
	CS_ScenarioWindowInit
LPlayer_Wait:
	LG_ChatHistoryWindow
	LG_ChatTextEntry
	LG_GameChatTextEntry
	LG_GameChatWindow
	LG_GameUserName
	LG_UserNameWindow
Launch_Manager:
	LM_AutoLaunchC1
	LM_AutoLaunchC2
	LM_AutoLaunchC3
	LM_AutoLaunchC4
	LM_AutoLaunchM
	LM_Carrier1Draw
	LM_Carrier2Draw
	LM_Carrier3Draw
	LM_Carrier4Draw
	LM_MotherShipDraw
	LM_ShipsToLaunch
	SV_Armor
	SV_Coverage
	SV_Firepower
	SV_Maneuver
	SV_Mass
	SV_ShipView
	SV_TopSpeed
List_Mappable_Keys:
	OP_KeyBindingsPoolList
Load_Lesson:
	FE_TutorialGameWindowInit
Load_a_scenario:
	CS_ScenarioBitmap
	CS_ScenarioWindowInit
Load_game:
	FE_GameWindowInit
Main_game_screen:
	SinglePlayerOptions
New_Account:
	MG_NameEntry
	MG_NewAccountConfirm
	MG_NewAccountPassword
Old_Skirmish_Load:
	FE_GameWindowInit
Options_New:
	VO_Background
	VO_BitmapBackground
	VO_BitmapBullet
	VO_BitmapDamage
	VO_BitmapFilter
	VO_BitmapHitEffects
	VO_BitmapInstantTransition
	VO_BitmapMuzzle
	VO_BitmapSensorsBlobs
	VO_BitmapStipple
	VO_Bullet
	VO_Damage
	VO_Filter
	VO_Hit
	VO_InstantTransition
	VO_Muzzle
	VO_SensorsBlobs
	VO_Stipple
Password_Change:
	MG_ConfirmPasswordChangeEntry
	MG_NameEntry
	MG_NewPasswordChangeEntry
	MG_OldPasswordChangeEntry
Player_Drop:
	UTY_PlayerDropped
Player_Options:
	CP_BaseColor
	CP_RaceOne
Player_Wait:
	MG_ChatHistoryWindow
	MG_ChatTextEntry
	MG_GameChatTextEntry
	MG_GameChatWindow
	MG_GameUserName
	MG_UserNameWindow
Recorded_Game:
	FE_RecordedGameWindowInit
Research_Manager:
	RM_Lab1Draw
	RM_Lab2Draw
	RM_Lab3Draw
	RM_Lab4Draw
	RM_Lab5Draw
	RM_Lab6Draw
	RM_LabConnector1Draw
	RM_LabConnector2Draw
	RM_LabConnector3Draw
	RM_LabConnector4Draw
	RM_LabConnector5Draw
	RM_LabConnector6Draw
	RM_TechImageDraw
	RM_TechListWindow
Resource_Options:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameType
	MG_HarvestingEnabled
	MG_LastMotherShip
	MG_ResourceInjectionAmount
	MG_ResourceInjectionInterval
	MG_ResourceInjections
	MG_ResourceLumpSum
	MG_ResourceLumpSumAmount
	MG_ResourceLumpSumInterval
	MG_StartShip
	MG_StartingResources
	OP_CPU_Attacks
	OP_CPU_Difficulty
Resource_Options_Change:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameType
	MG_HarvestingEnabled
	MG_LastMotherShip
	MG_ResourceInjectionAmount
	MG_ResourceInjectionInterval
	MG_ResourceInjections
	MG_ResourceLumpSum
	MG_ResourceLumpSumAmount
	MG_ResourceLumpSumInterval
	MG_StartShip
	MG_StartingResources
	OP_CPU_Attacks
	OP_CPU_Difficulty
Resource_Options_View:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameType
	MG_HarvestingEnabled
	MG_LastMotherShip
	MG_ResourceInjectionAmount
	MG_ResourceInjectionInterval
	MG_ResourceInjections
	MG_ResourceLumpSum
	MG_ResourceLumpSumAmount
	MG_ResourceLumpSumInterval
	MG_StartShip
	MG_StartingResources
	OP_CPU_Attacks
	OP_CPU_Difficulty
Room_Password:
	MG_RoomPasswordEntry
Say_Chatting_Screen:
	InGameChatEntry
Select_Language:
	VO_Language
Select_colour:
	CP_BaseColor
Select_tutorial:
	Tutorial1
Sensors_manager:
	SM_Hyperspace
Single_Player_Objective:
	PO_TextDraw
Skirmish_Advanced:
	MG_AlliedVictory
	MG_BountySize
	MG_CaptureCapitalShip
	MG_CratesEnabled
	MG_GameType
	MG_Hyperspace
	MG_LastMotherShip
	MG_NoFuelBurn
	MG_ResearchEnabled
	MG_StartShip
	MG_UnitCapsEnabled
	OP_CPU_Attacks
	OP_CPU_Difficulty
Skirmish_Basic:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameType
	MG_LastMotherShip
	MG_StartShip
	OP_CPU_Attacks
	OP_CPU_Difficulty
Skirmish_Colour:
	CP_BaseColor
	CP_RaceOne
Skirmish_Load:
	FE_GameWindowInit
Skirmish_Resource:
	MG_AlliedVictory
	MG_CaptureCapitalShip
	MG_GameType
	MG_HarvestingEnabled
	MG_LastMotherShip
	MG_ResourceInjectionAmount
	MG_ResourceInjectionInterval
	MG_ResourceInjections
	MG_ResourceLumpSum
	MG_ResourceLumpSumAmount
	MG_ResourceLumpSumInterval
	MG_StartShip
	MG_StartingResources
	OP_CPU_Attacks
	OP_CPU_Difficulty
Task_Bar:
	CSM_Hyperspace
	TB_ObjectivesWindowInit
Video:
	OP_Brightness
	OP_Detail_Threshold
	OP_Effects
	OP_NoLOD
	OP_NumEffects
Video_Options:
	OP_Brightness
	OP_Detail_Threshold
	OP_Effects
	OP_NoLOD
	OP_NumEffects
	OP_Render
	OP_Resolution
*/
		];
}
