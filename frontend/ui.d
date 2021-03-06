/* 
  TODO:
   * overhul event interfaces
   * implement focus interface (with event propagation)
   * ...
   * keyboard state / API (set focus, etc.)
   * mouse state / API (capture, etc.)
*/

import std.typecons;
static import sys;
static import tree;
static import generic;
alias generic.Point!(short) Point;


enum FB
{
	NONE         = 0,
	StateChanged = 1,
	CaptureMouse = 1<<1,
	ReleaseMouse = 1<<2,
}
enum MOUSE_DIRECTION { ENTER, LEAVE }
enum MOUSE_ACTION { PRESS, RELEASE, DOUBLECLICK }
enum KEY_ACTION { PRESS, RELEASE }


/* all possible events should be described here */
struct FocusEvent(T)
{
	T target;
	bool accepted;
	uint button;
}

struct EventHandlers(T)
{
	// keyboard input
	FB function(uint key, KEY_ACTION action)
			keyboard,
			keyboardPropagateUpward,
			keyboardPropagateDownward;
	//bool function(MOUSE_ACTION action, uint button)
	//		focusOnClick,
	//		focusOnClickPropagateUpward,
	//		focusOnClickPropagateDownward;
	FB function(inout FocusEvent!(T)) //TODO:implement
			focusPropagateDownward,
			focus,
			focusPropagateUpward;
	// mouse input
	FB function(const ref Point pos, MOUSE_ACTION action, uint button)
			mouseButton,
			mouseButtonPropagateUpward,
			mouseButtonPropagateDownward;
	FB function(int x, int y)
			mouseScroll,
			mouseScrollPropagateUpward,
			mouseScrollPropagateDownward;
	FB function(MOUSE_DIRECTION dir)
			mouseOver,
			mouseOverPropagateUpward,
			mouseOverPropagateDownward;
}


/* this is important concept - injecting an interface into root of the class hierarchy */
class TargetNode(alias PAINT_INTERFACE)
{
	mixin PAINT_INTERFACE;

	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.makeFirstChild;
	mixin tree.opApply!(`!node.hidden`);  // for mouse cursor hit test (with a condition mixin)
	mixin tree.opApplyReverse!(`!node.hidden`);  // for drawing (with a condition mixin)

	static typeof(this) focusedNode;

	bool hidden;
	bool disabled;

	string name;

	bool nested = true;
	union
	{
		protected generic.Rect!(short, ushort) _rect;
		struct
		{
			short x, y;
			ushort width, height;
		}
		static assert (_rect.sizeof == short.sizeof*2 + ushort.sizeof*2);
	}

	EventHandlers!(typeof(this))* handlers;
	invariant() { assert (handlers !is null); }
	protected static EventHandlers!(typeof(this)) _eventMap;
	this(string name, typeof(this) parent)
	{
		this.handlers = &_eventMap;
		if (parent)
			this.setParent(parent);
		this.name = name;
	}

	Point position_abs() const
	{
		Point abs_pos = this._rect.position;
		auto parent = Rebindable!(const TargetNode)(this.nested ? this.parent : null);
		while (parent.opDot !is null)
		{
			abs_pos += parent._rect.position;
			parent = parent.nested ? parent.parent : null;
		}
		return abs_pos;
	}

	void resize(ushort w, ushort h)
	{
		this._rect.size.width = w;
		this._rect.size.height = h;
	}
}

class EventManager(T /* : TargetNode */)
{
	T root;
	T mouseOldTarget;
	T mouseHolder;
	sys.Window window;  // used to force native window to redraw itself (temp design hack)

	this(sys.Window window)
	{
		this.window = window;
	}

	// native window notifications
	// http://msdn.microsoft.com/ms674887

	/* native window being hidden (minimized) or shown (restored, maximized)
	   http://msdn.microsoft.com/ms632645 */
	void notify_SHOW_state_change(bool show, bool maximized) { this.root.hidden = !show; }

	/* native window gained/loses keyboard focus
	   (most likeky native window being activated or deactivated)
	   http://msdn.microsoft.com/ms646312
	   http://msdn.microsoft.com/ms646274 */
	void notify_FOCUS_state_change(bool focused)
	{
		this.setFocus(focused ? this.root : null);
	}

	/* native window being resized (possibly maximized)
	   http://msdn.microsoft.com/ms632646 */
	void notify_SIZE_state_change(ushort w, ushort h, bool maximized)
	{
		this.root.resize(w, h);
	}

	/* size or position of native window is about to change 
	   http://msdn.microsoft.com/ms632626 */
	bool query_MINMAX_info(inout sys.Size size) { size.width = 640; size.height = 480; return true; }

	/* native window asked to be destroyed
	   http://msdn.microsoft.com/ms632617 */
	bool confirm_CLOSE_action() { return true; }

	/* http://msdn.microsoft.com/ms632650 */
	void notify_THEMECHANGED_event() {}

	/* native window received mouse input */
	void dispatch_MOUSE_input(const ref Point pos, sys.MOUSE type, int button = -1)
	{
		T[32] event_path_stack;
		T[] get_event_path(T target_node)
		{
			auto i = event_path_stack.length;
			for (auto node=target_node.parent; node !is null; node=node.parent)
				event_path_stack[--i] = node;
			return event_path_stack[i..event_path_stack.length];
		}
		auto nodeUnderCursor = findControl(this.root, pos);
		auto target = (this.mouseHolder !is null) ? this.mouseHolder : nodeUnderCursor;

		switch (type)
		{
		case sys.MOUSE.PRESS:
			assert (button > -1);
			if (target is null || target.disabled)
				return;
			auto event_path = get_event_path(target);

			//// Set focus first...
			FocusEvent!(T) ev;
			ev.target = target;
			// Downward Propagation a.k.a. Sinking/Tunneling/Preview/Capturing phase
			foreach (ref node; event_path)
			{
				if (node.handlers.focusPropagateDownward !is null)
				{
					FB delegate(inout FocusEvent!(T)) handler;
					handler.funcptr = node.handlers.focusPropagateDownward;
					handler.ptr = cast(void*)node;
					this.process(handler(ev), node, pos);
				}
			}
			// Delivering phase
			if (target.handlers.focus !is null)
			{
				FB delegate(inout FocusEvent!(T)) handler;
				handler.funcptr = target.handlers.focus;
				handler.ptr = cast(void*)target;
				this.process(handler(ev), target, pos);
			}
			// Upward Propagation a.k.a. Bubbling phase
			foreach_reverse (ref node; event_path)
			{
				if (node.handlers.focusPropagateUpward !is null)
				{
					FB delegate(inout FocusEvent!(T)) handler;
					handler.funcptr = node.handlers.focusPropagateUpward;
					handler.ptr = cast(void*)node;
					this.process(handler(ev), node, pos);
				}
			}
			//TODO: implement
			this.setFocus(ev.target);

			// Proceed with mouse press ...
			// Downward Propagation a.k.a. Sinking/Tunneling/Preview/Capturing phase
			foreach (ref node; event_path)
			{
				if (node.handlers.mouseButtonPropagateDownward !is null)
				{
					FB delegate(const ref Point pos, MOUSE_ACTION action, uint button) handler;
					handler.funcptr = node.handlers.mouseButtonPropagateDownward;
					handler.ptr = cast(void*)node;
					this.process(handler(pos, MOUSE_ACTION.PRESS, button), node, pos);
				}
			}
			// Delivering phase
			if (target.handlers.mouseButton !is null)
			{
				FB delegate(const ref Point pos, MOUSE_ACTION action, uint button) handler;
				handler.funcptr = target.handlers.mouseButton;
				handler.ptr = cast(void*)target;
				this.process(handler(pos, MOUSE_ACTION.PRESS, button/*, modifiers*/), target, pos);
			}
			// Upward Propagation a.k.a. Bubbling phase
			foreach_reverse (ref node; event_path)
			{
				if (node.handlers.mouseButtonPropagateUpward !is null)
				{
					FB delegate(const ref Point pos, MOUSE_ACTION action, uint button) handler;
					handler.funcptr = node.handlers.mouseButtonPropagateUpward;
					handler.ptr = cast(void*)node;
					this.process(handler(pos, MOUSE_ACTION.PRESS, button), node, pos);
				}
			}
			break;

		case sys.MOUSE.RELEASE:
			assert (button > -1);
			if (target is null || target.disabled)
				return;

			// process mouse button release if thhere is a handler
			if (target.handlers.mouseButton !is null)
			{
				FB delegate(const ref Point pos, MOUSE_ACTION action, uint button) handler;
				handler.funcptr = target.handlers.mouseButton;
				handler.ptr = cast(void*)target;
				this.process(handler(pos, MOUSE_ACTION.RELEASE, button/*, modifiers*/), target, pos);
			}
			break;

		case sys.MOUSE.MOVE:
			auto newTarget = (this.mouseHolder is null || this.mouseHolder is nodeUnderCursor) ? nodeUnderCursor : null;
			if (this.mouseOldTarget !is newTarget)
				passMouse(newTarget, pos);
			if (target is null || target.disabled)
				return;
			//TODO: subscription (tracking) of mouse movement
			//this.process(target.onMouseMove(pos), target, pos);
			break;

		case sys.MOUSE.LEAVE:
			passMouse(null, pos);
			break;
		}
	}

	void setFocus(T target)
	{
		if (T.focusedNode is target)
			return;
		T.focusedNode = target;
		this.window.redraw();  // FB.StateChanged
	}

	bool dispatch_KEYBOARD_input(uint key, sys.KEY type)
	{
		if (T.focusedNode is null || T.focusedNode.handlers.keyboard is null)
			return false;

		FB delegate(uint key, KEY_ACTION action) handler;
		handler.funcptr = T.focusedNode.handlers.keyboard;
		handler.ptr = cast(void*)T.focusedNode;
		auto res = handler(key, type == sys.KEY.PRESS ? KEY_ACTION.PRESS : KEY_ACTION.RELEASE);

		return res == FB.NONE ? false : true;
	}

	protected
	void passMouse(T target, const ref Point pos)
	{
		assert (this.mouseOldTarget !is target);

		if (this.mouseOldTarget !is null)
		{
			if (mouseOldTarget.handlers.mouseOver !is null)
			{
				FB delegate(MOUSE_DIRECTION dir) handler;
				handler.funcptr = mouseOldTarget.handlers.mouseOver;
				handler.ptr = cast(void*)mouseOldTarget;
				this.process(handler(MOUSE_DIRECTION.LEAVE), this.mouseOldTarget, pos);
			}
			//TODO: check if this.mouseOldTarget just captured mouse
		}

		if (target !is null && !target.disabled)
		{
			if (target.handlers.mouseOver !is null)
			{
				FB delegate(MOUSE_DIRECTION dir) handler;
				handler.funcptr = target.handlers.mouseOver;
				handler.ptr = cast(void*)target;
				this.process(handler(MOUSE_DIRECTION.ENTER), target, pos);
			}
		}

		this.mouseOldTarget = target;
	}

	protected
	void process(FB feedback, T target, const ref Point pos)
	{
		assert (target !is null);
		if (feedback & FB.CaptureMouse)
		{
			assert (this.mouseHolder is null);
			this.mouseHolder = target;
		}
		if (feedback & FB.ReleaseMouse)
		{
			assert (this.mouseHolder is target);
			this.mouseHolder = null;
			//TODO: get rid of recursion
			target = findControl(this.root, pos);
			if (this.mouseOldTarget !is target)
				passMouse(target, pos);
		}
		if (feedback & FB.StateChanged)
			this.window.redraw();  // render manager - redraw scene
	}
}


T findControl(T)(T root, const ref Point point)
{
	foreach (ref node; root)
	{
		Point translated_point = point;
		if ((node.nested && node.parent !is null))
		{
			auto position_abs = node.parent.position_abs();
			translated_point = point - position_abs;
		}
		//Point translated_point = (!node.nested || node.parent is null) ?
		//		point :
		//		point - node.parent.position_abs();
		if (node._rect.contains(translated_point))
			return node;
	}
	return null;
}
