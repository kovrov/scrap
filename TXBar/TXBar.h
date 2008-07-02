// TXBar.h : main header file for the TXBAR application
//

#if !defined(AFX_TXBAR_H__EF0ED8CE_ABA2_4FF4_9C85_3DA9296C86E0__INCLUDED_)
#define AFX_TXBAR_H__EF0ED8CE_ABA2_4FF4_9C85_3DA9296C86E0__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CTXBarApp:
// See TXBar.cpp for the implementation of this class
//

class CTXBarApp : public CWinApp
{
public:
	CTXBarApp();
	ULONG_PTR m_gdiplusToken;

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CTXBarApp)
	public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CTXBarApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_TXBAR_H__EF0ED8CE_ABA2_4FF4_9C85_3DA9296C86E0__INCLUDED_)
