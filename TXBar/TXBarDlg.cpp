// TXBarDlg.cpp : implementation file

//***********************************************************
// author : skinui
// website: http://www.skinui.com
// 2007.8.8
//***********************************************************

#include "stdafx.h"
#include "TXBar.h"
#include "TXBarDlg.h"
#include "math.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif


/////////////////////////////////////////////////////////////////////////////
// CTXBarDlg dialog

CTXBarDlg::CTXBarDlg(CWnd* pParent /*=NULL*/)
  : CDialog(CTXBarDlg::IDD, pParent)
{
	rcTool[0].X = 59;
	rcTool[0].Y = 45;
	rcTool[0].Width = 24;
	rcTool[0].Height = 24;

	rcTool[1].X = 95;
	rcTool[1].Y = 45;
	rcTool[1].Width = 24;
	rcTool[1].Height = 24;

	rcTool[2].X = 131;
	rcTool[2].Y = 45;
	rcTool[2].Width = 24;
	rcTool[2].Height = 24;

	rcTool[3].X = 167;
	rcTool[3].Y = 45;
	rcTool[3].Width = 24;
	rcTool[3].Height = 24;

	rcTool[4].X = 203;
	rcTool[4].Y = 45;
	rcTool[4].Width = 24;
	rcTool[4].Height = 24;

	rcTool[5].X = 239;
	rcTool[5].Y = 45;
	rcTool[5].Width = 24;
	rcTool[5].Height = 24;

	rcBack[0].X = 59;
	rcBack[0].Y = 45;
	rcBack[0].Width = 24;
	rcBack[0].Height = 24;
	
	rcBack[1].X = 95;
	rcBack[1].Y = 45;
	rcBack[1].Width = 24;
	rcBack[1].Height = 24;
	
	rcBack[2].X = 131;
	rcBack[2].Y = 45;
	rcBack[2].Width = 24;
	rcBack[2].Height = 24;
	
	rcBack[3].X = 167;
	rcBack[3].Y = 45;
	rcBack[3].Width = 24;
	rcBack[3].Height = 24;
	
	rcBack[4].X = 203;
	rcBack[4].Y = 45;
	rcBack[4].Width = 24;
	rcBack[4].Height = 24;
	
	rcBack[5].X = 239;
	rcBack[5].Y = 45;
	rcBack[5].Width = 24;
	rcBack[5].Height = 24;

	for (int i=0; i<6; i++)
	{
		rcRange[i].left = 53+i*36;
		rcRange[i].top = 40;
		rcRange[i].right = 53+(i+1)*36;
		rcRange[i].bottom = 45+5+5+24;
	}
}


BEGIN_MESSAGE_MAP(CTXBarDlg, CDialog)
	//{{AFX_MSG_MAP(CTXBarDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_ERASEBKGND()
	ON_WM_MOUSEMOVE()
	ON_WM_LBUTTONDOWN()
	ON_WM_TIMER()
	ON_WM_LBUTTONUP()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CTXBarDlg message handlers

BOOL CTXBarDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// TODO: Add extra initialization here
	RECT r;
	GetClientRect(&r);
	SetWindowPos(&wndTopMost, r.left, r.top, r.right, r.bottom, SWP_NOOWNERZORDER);

	BOOL bRet = FALSE;

	// 初始化gdiplus的环境
	// Initialize GDI+.
	m_Blend.BlendOp=0; //the only BlendOp defined in Windows2000
	m_Blend.BlendFlags=0; //nothingelseisspecial...
	m_Blend.AlphaFormat=1; //...
	m_Blend.SourceConstantAlpha=255;//AC_SRC_ALPHA

	DrawTXBar();

	// 去除任务栏窗口对应按钮
	// Excluding the corresponding button on the task bar window
	ModifyStyleEx(WS_EX_APPWINDOW, WS_EX_TOOLWINDOW);

	return TRUE;  // return TRUE  unless you set the focus to a control
}



BOOL CTXBarDlg::OnEraseBkgnd(CDC* pDC)
{
	pDC->SetBkMode(TRANSPARENT);
	return TRUE; 
}


void CTXBarDlg::DrawTXBar()
{
	HDC hdcTemp = GetDC()->m_hDC;
	m_hdcMemory = ::CreateCompatibleDC(hdcTemp);
	HBITMAP hBitMap = ::CreateCompatibleBitmap(hdcTemp, 400, 300);
	::SelectObject(m_hdcMemory, hBitMap);
	
	HDC hdcScreen = ::GetDC(m_hWnd);
	RECT rct;
	GetWindowRect(&rct);
	POINT ptWinPos={rct.left,rct.top};
	
	Graphics graphics(m_hdcMemory);
	RECT rcClient;
	GetClientRect(&rcClient);
	
	Image m_Title(L"toolbarbktop.png");
	graphics.DrawImage(&m_Title,Rect(rcClient.left+50,rcClient.top,m_Title.GetWidth(),m_Title.GetHeight()));
	
	Image m_ToolBK(L"toolbarbkbottom.png");
	graphics.DrawImage(&m_ToolBK,Rect(rcClient.left+50,rcClient.top+m_Title.GetHeight()-4,m_Title.GetWidth(),m_ToolBK.GetHeight()));
	
	if(rcTool[0].Width < 36)
	{
		Image m_Tool0(L"intomain_24.png");
		graphics.DrawImage(&m_Tool0,rcTool[0]);
	}
	else
	{
		Image m_Tool0_1(L"intomain_48.png");
		graphics.DrawImage(&m_Tool0_1,rcTool[0]);
	}
	

	if(rcTool[1].Width <36)
	{
		Image m_Tool1(L"intomini_24.png");
		graphics.DrawImage(&m_Tool1,rcTool[1]);
	}
	else
	{
		Image m_Tool1_1(L"intomini_48.png");
		graphics.DrawImage(&m_Tool1_1,rcTool[1]);
	}

	if(rcTool[2].Width < 36)
	{
		Image m_Tool2(L"todolist_24.png");
		graphics.DrawImage(&m_Tool2,rcTool[2]);
	}
	else
	{
		Image m_Tool2_1(L"todolist_48.png");
		graphics.DrawImage(&m_Tool2_1,rcTool[2]);
	}
	
	if(rcTool[3].Width < 36)
	{
		Image m_Tool3(L"mini_newevent_small.png");
		graphics.DrawImage(&m_Tool3,rcTool[3]);
	}
	else
	{
		Image m_Tool3_1(L"newevent_big.png");
		graphics.DrawImage(&m_Tool3_1,rcTool[3]);
	}
	
	if(rcTool[4].Width < 36)
	{
		Image m_Tool4(L"setting_24.png");
		graphics.DrawImage(&m_Tool4,rcTool[4]);
	}
	else
	{
		Image m_Tool4_1(L"setting_48.png");
		graphics.DrawImage(&m_Tool4_1,rcTool[4]);
	}
	
	if(rcTool[5].Width < 36 )
	{
		Image m_Tool5(L"exit_24.png");
		graphics.DrawImage(&m_Tool5,rcTool[5]);
	}
	else
	{
		Image m_Tool5_1(L"exit_48.png");
		graphics.DrawImage(&m_Tool5_1,rcTool[5]);
	}
	
/*	Pen pen(Color(255,21,164,208),1);
	for (int i=0; i<6; i++)
	{
		Rect rcTemp;
		rcTemp.X = rcRange[i].left;
		rcTemp.Y = rcRange[i].top;
		rcTemp.Width = rcRange[i].right - rcRange[i].left;
		rcTemp.Height = rcRange[i].bottom - rcRange[i].top;
		
		graphics.DrawRectangle(&pen,rcTemp);
	}*/

	SIZE sizeWindow = {400, 300};
	POINT ptSrc = {0, 0};
	
	DWORD dwExStyle = GetWindowLong(m_hWnd,GWL_EXSTYLE);
	if ((dwExStyle&0x80000) != 0x80000)
		SetWindowLong(m_hWnd,GWL_EXSTYLE,dwExStyle^0x80000);
	
	BOOL bRet = FALSE;
	bRet = ::UpdateLayeredWindow(m_hWnd, hdcScreen, &ptWinPos, &sizeWindow, m_hdcMemory, &ptSrc, 0, &m_Blend, 2);
	graphics.ReleaseHDC(m_hdcMemory);
	::ReleaseDC(m_hWnd,hdcScreen);
	hdcScreen=NULL;
	::ReleaseDC(m_hWnd,hdcTemp);
	hdcTemp=NULL;
	DeleteObject(hBitMap);
	DeleteDC(m_hdcMemory);
	m_hdcMemory=NULL;
}

void CTXBarDlg::OnMouseMove(UINT nFlags, CPoint point) 
{
	// TODO: Add your message handler code here and/or call default
	POINT pt;
	pt.x = point.x;
	pt.y = point.y;

	int nBack;

	for (int i=0; i<6; i++)
	{
		if (PtInRect(&(rcRange[i]),pt))
		{
			rcTool[i].X = rcBack[i].X+rcBack[i].Width/2-24+((rcBack[i].X+rcBack[i].Width/2)-point.x);   //
			rcTool[i].Y = rcBack[i].Y;	
			rcTool[i].Width = 48;
			rcTool[i].Height = 48;

			nBack = (rcRange[i].right - rcRange[i].left)/2;  // 区域宽度备份/2
				
			rcRange[i].left = rcTool[i].X - 12;
			rcRange[i].top = rcTool[i].Y;
			rcRange[i].right = rcTool[i].X - 12+72;
			rcRange[i].bottom = rcTool[i].Y+53;
/*
			for(int m=0; m<6; m++)
			{
				if(m > i)
				{
					rcTool[m].X = rcTool[i].X+66+(m-i-1)*36;	
					rcTool[m].Y = rcTool[m].Y;
					rcTool[m].Width = 24;
					rcTool[m].Height = 24;

					rcRange[m].left = rcTool[m].X - 6;
					rcRange[m].top = rcTool[m].Y;
					rcRange[m].right = rcTool[m].X +30;
					rcRange[m].bottom = rcTool[m].Y+53;
				}
				else if(m < i)
				{
					rcTool[m].X = rcTool[i].X-12+(m-i)*36+6;	
					rcTool[m].Y = rcTool[m].Y;
					rcTool[m].Width = 24;
					rcTool[m].Height = 24;
					
					rcRange[m].left = rcTool[m].X - 6;
					rcRange[m].top = rcTool[m].Y;
					rcRange[m].right = rcTool[m].X - 6+36;
					rcRange[m].bottom = rcTool[m].Y+53;
				}

			}
*/

			int nLen = 66;
			int x = point.x - (rcTool[i].X+24);

			int nN = GetMoreInt(x,36);
	
			for(int m=i+1;m<6;m++)
			{
				rcTool[m].X = rcTool[i].X+nLen;
				rcTool[m].Y = rcTool[m].Y;
				if((m-i) == 1)
				{
					rcTool[m].Width = 36+nN;
					rcTool[m].Height = 36+nN;

					nLen += rcTool[m].Width+12;

				}
				else if( (m-i) == 2)
				{
					if((24+nN)>24)
					{
						rcTool[m].Width = 24+nN;
						rcTool[m].Height = 24+nN;
					}
					else
					{
						rcTool[m].Width = 24;
						rcTool[m].Height = 24;
					}
					
					nLen += rcTool[m].Width +12;
				}
				else
				{
					rcTool[m].Width = 24;
					rcTool[m].Height = 24;

					nLen += 24+12;
				}

				rcRange[m].left = rcTool[m].X - 6;
				rcRange[m].top = rcTool[m].Y-5;
				rcRange[m].right = rcTool[m].X + rcTool[m].Width+6;
				rcRange[m].bottom = rcTool[m].Y+ rcTool[m].Height +5;
			}
			
			nLen = 0;
			for (int k=i;k>=0;k--)
			{
				if(k != i)
				{				
				if((i-k) == 1)
				{
					rcTool[k].Width = 36-nN;
					rcTool[k].Height = 36-nN;
					
					nLen += rcTool[k].Width+18;
					
				}
				else if( (i-k) == 2)
				{
					if((24-nN)>24)
					{
						rcTool[k].Width = 24-nN;
						rcTool[k].Height = 24-nN;
					}
					else
					{
						rcTool[k].Width = 24;
						rcTool[k].Height = 24;
					}
										
					nLen += rcTool[k].Width +12;
				}
				else
				{
					rcTool[k].Width = 24;
					rcTool[k].Height = 24;
					
					nLen += 24+12;
				}
				
				rcTool[k].X = rcTool[i].X-nLen;
				rcTool[k].Y = rcTool[k].Y;

				rcRange[k].left = rcTool[k].X - 6;
				rcRange[k].top = rcTool[k].Y-5;
				rcRange[k].right = rcTool[k].X + rcTool[k].Width+6;
				rcRange[k].bottom = rcTool[k].Y+ rcTool[k].Height +5;
				}
			}

/*
			int nLen = 66;
			int nN = 0;
			int m;
			for (m=i+1; m<6; m++)
			{
				if ((m-i) == 1)
				{
					rcTool[m].X = rcTool[i].X + nLen;
					rcTool[m].Y = rcTool[m].Y;

					float ff = ((rcTool[m].X - point.x)/42.0f)*36.0f;
					nN = (int)fabs(ff);
					if (nN > 48)
					{
						nN = 48;
					}
					else if (nN < 24)
					{
						nN = 24;
					}
					rcTool[m].Width = nN;
					rcTool[m].Height = rcTool[m].Width;

					nLen += rcTool[m].Width +12;
				}
				else if ((m-i == 2))
				{
					rcTool[m].X = rcTool[i].X + nLen;
					rcTool[m].Y = rcTool[m].Y;

					float fb = ((rcTool[m].X - point.x)/90.0f)*24.0f;

					nN = (int)fabs(fb);
					if (nN > 48)
					{
						nN = 48;
					}
					else if (nN < 24)
					{
						nN = 24;
					}

					rcTool[m].Width = nN;
					rcTool[m].Height = rcTool[m].Width;

					nLen += rcTool[m].Width +12;
				}
				else
				{
					rcTool[m].X = rcTool[i].X + nLen;
					rcTool[m].Y = rcTool[m].Y;
					rcTool[m].Width = 24;
					rcTool[m].Height = 24;

					nLen += 36;
				}

				rcRange[m].left = rcTool[m].X - 6;
				rcRange[m].top = rcTool[m].Y-5;
				rcRange[m].right = rcTool[m].X + rcTool[m].Width+6;
				rcRange[m].bottom = rcTool[m].Y+ rcTool[m].Height +5;
			}

			nLen = 18;
			for (int k=i; k>=0; k--)
			{
				if (k != i)
				{
					if ((i-k) == 1)
					{
						float fc = ((point.x - (rcTool[i].X - nLen))/42.0f)*36.0f;

						nN = (int)fabs(fc);
						if (nN > 48)
						{
							nN = 48;
						}
						else if (nN < 24)
						{
							nN = 24;
						}
						rcTool[k].Width = nN;
						rcTool[k].Height = rcTool[k].Width;

						rcTool[k].X = rcTool[i].X - nLen - rcTool[k].Width;
						rcTool[k].Y = rcTool[k].Y;

						nLen += rcTool[k].Width+12;
					}
					else if ((i-k) == 2)
					{
						float fd = ((point.x - (rcTool[i].X - nLen))/90.0f)*24.0f;

						nN = (int)fabs(fd);
						if (nN > 48)
						{
							nN = 48;
						}
						else if (nN < 24)
						{
							nN = 24;
						}
						rcTool[k].Width = nN;
						rcTool[k].Height = rcTool[k].Width;

						rcTool[k].X = rcTool[i].X - nLen - rcTool[k].Width;
						rcTool[k].Y = rcTool[k].Y;

						nLen += rcTool[k].Width +12;
					}
					else
					{
						rcTool[k].Width = 24;
						rcTool[k].Height = 24;
						rcTool[k].X = rcTool[i].X - nLen - rcTool[k].Width;
						rcTool[k].Y = rcTool[k].Y;

						nLen += 24+12;
					}

					rcRange[m].left = rcTool[m].X - 6;
					rcRange[m].top = rcTool[m].Y-5;
					rcRange[m].right = rcTool[m].X + rcTool[m].Width+6;
					rcRange[m].bottom = rcTool[m].Y+ rcTool[m].Height +5;
				}
			}
*/
			DrawTXBar();
			SetTimer(1,10,NULL);
			break;
		}
	}
	
	CDialog::OnMouseMove(nFlags, point);
}

void CTXBarDlg::OnLButtonDown(UINT nFlags, CPoint point) 
{
	// TODO: Add your message handler code here and/or call default

	POINT pt;
	pt.x = point.x;
	pt.y = point.y;
	CString m_Box;
	for (int i=0; i<6; i++)
	{
		if (PtInRect(&(rcRange[i]),pt))
		{
			m_Box.Format("%d",i);
			MessageBox(m_Box);
			break;
		}
	}
	CDialog::OnLButtonDown(nFlags, point);
}

void CTXBarDlg::OnTimer(UINT nIDEvent) 
{
	// TODO: Add your message handler code here and/or call default
	POINT pt;
	GetCursorPos(&pt);
	ScreenToClient(&pt);
	int k;

	for (int i=0; i<6; i++)
	{
		if (PtInRect(&(rcRange[i]),pt))
		{
			goto label;
		}
	}
	
	KillTimer(1);

	rcTool[0].X = 59;
	rcTool[0].Y = 45;
	rcTool[0].Width = 24;
	rcTool[0].Height = 24;
	
	rcTool[1].X = 95;
	rcTool[1].Y = 45;
	rcTool[1].Width = 24;
	rcTool[1].Height = 24;
	
	rcTool[2].X = 131;
	rcTool[2].Y = 45;
	rcTool[2].Width = 24;
	rcTool[2].Height = 24;
	
	rcTool[3].X = 167;
	rcTool[3].Y = 45;
	rcTool[3].Width = 24;
	rcTool[3].Height = 24;
	
	rcTool[4].X = 203;
	rcTool[4].Y = 45;
	rcTool[4].Width = 24;
	rcTool[4].Height = 24;
	
	rcTool[5].X = 239;
	rcTool[5].Y = 45;
	rcTool[5].Width = 24;
	rcTool[5].Height = 24;

	for (k=0; k<6; k++)
	{
		rcRange[k].left = 53+k*36;
		rcRange[k].top = 40;
		rcRange[k].right = 53+(k+1)*36;
		rcRange[k].bottom = 45+5+5+24;
	}

	DrawTXBar();

label:

	CDialog::OnTimer(nIDEvent);
}



int GetMoreInt(int x, int nBack)
{
	int ret = 0;
	BOOL bJian = FALSE;

	if (x < 0)
	{
		x = -x;
		bJian = TRUE;
	}

	if (x>=0 && x<(nBack/6))
	{
		ret = 2;
	}
	else if ((x >= (nBack/6)) && (x < (2*nBack/6)))
	{
		ret = 4;
	}
	else if ((x >= (2*nBack/6)) && (x < (3*nBack/6)))
	{
		ret = 6;
	}
	else if ((x >= (3*nBack/6)) && (x < (4*nBack/6)))
	{
		ret = 8;
	}
	else if ((x >= (4*nBack/6)) && (x < (5*nBack/6)))
	{
		ret = 10;
	}
	else if ((x >= (5*nBack/6)) && (x < (6*nBack/6)))
	{
		ret = 12;
	}
	else if (x >= (6*nBack/6))
	{
		ret = 12;
	}

	if (bJian)
	{
		ret = - ret;
	}

	return ret;
}
