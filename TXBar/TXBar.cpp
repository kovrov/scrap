// TXBar.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"
#include "TXBar.h"
#include "TXBarDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CTXBarApp

BEGIN_MESSAGE_MAP(CTXBarApp, CWinApp)
	//{{AFX_MSG_MAP(CTXBarApp)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code!
	//}}AFX_MSG
	ON_COMMAND(ID_HELP, CWinApp::OnHelp)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CTXBarApp construction

CTXBarApp::CTXBarApp()
{
	// TODO: add construction code here,
	// Place all significant initialization in InitInstance
}

/////////////////////////////////////////////////////////////////////////////
// The one and only CTXBarApp object

CTXBarApp theApp;

/////////////////////////////////////////////////////////////////////////////
// CTXBarApp initialization

BOOL CTXBarApp::InitInstance()
{
	AfxEnableControlContainer();

	// Standard initialization
	// If you are not using these features and wish to reduce the size
	//  of your final executable, you should remove from the following
	//  the specific initialization routines you do not need.

	GdiplusStartupInput m_gdiplusstartupinput;
	GdiplusStartup(&m_gdiplusToken, &m_gdiplusstartupinput, NULL);

	CTXBarDlg dlg;
	m_pMainWnd = &dlg;
	int nResponse = dlg.DoModal();

	// Since the dialog has been closed, return FALSE so that we exit the
	//  application, rather than start the application's message pump.
	return FALSE;
}

int CTXBarApp::ExitInstance() 
{
	// TODO: Add your specialized code here and/or call the base class
	GdiplusShutdown(m_gdiplusToken);
	return CWinApp::ExitInstance();
}
