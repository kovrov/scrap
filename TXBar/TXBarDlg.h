// TXBarDlg.h : header file
//

#if !defined(AFX_TXBARDLG_H__C986C8A1_EAE1_48E4_A750_38A2F01DED0C__INCLUDED_)
#define AFX_TXBARDLG_H__C986C8A1_EAE1_48E4_A750_38A2F01DED0C__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CTXBarDlg dialog

class CTXBarDlg : public CDialog
{
// Construction
public:
	void DrawTXBar();
	CTXBarDlg(CWnd* pParent = NULL);	// standard constructor

	typedef BOOL (WINAPI *MYFUNC)(HWND,HDC,POINT*,SIZE*,HDC,POINT*,COLORREF,BLENDFUNCTION*,DWORD);          

	BLENDFUNCTION m_Blend;
	HDC m_hdcMemory;

	Rect rcTool[6];
	Rect rcBack[6];
	RECT rcRange[6];
// Dialog Data
	enum { IDD = IDD_TXBAR_DIALOG };

// Implementation
protected:
	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnTimer(UINT nIDEvent);
	DECLARE_MESSAGE_MAP()
};

int GetMoreInt(int x, int nBack);

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_TXBARDLG_H__C986C8A1_EAE1_48E4_A750_38A2F01DED0C__INCLUDED_)
