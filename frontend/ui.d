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
struct EventHandlers
{
	// keyboard input
	FB function(uint key, KEY_ACTION action)
			keyboard,
			keyboardPropagateUpward,
			keyboardPropagateDownward;
	bool function(MOUSE_ACTION action, uint button)
			focusOnClick,
			focusOnClickPropagateUpward,
			focusOnClickPropagateDownward;
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
	mixin tree.opApply!(`!node.hidden`);  // for mouse cursor hit test (with condition mixin)
	mixin tree.opApplyReverse!(`!node.hidden`);  // for drawing (with condition mixin)

	static typeof(this) activeNode;
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

	EventHandlers* handlers;
	invariant() { assert (handlers !is null); }
	protected static EventHandlers _eventMap;
	this(string name, typeof(this) parent)
	{
		this.handlers = &_eventMap;
		if (parent)
			this.setParent(parent);
		this.name = name;
	}

	Point position_abs()
	{
		auto abs_pos = this._rect.position;
		auto parent = this.nested ? this.parent : null;
		while (parent)
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
	sys.Window window;

	this(sys.Window window)
	{
		this.window = window;
	}

	void dispatch_mouse_input(const ref Point pos, sys.MOUSE type, int button = -1)
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
			// set focus...
			if (target.handlers.focusOnClick !is null && T.focusedNode !is target)
			{
				bool delegate(MOUSE_ACTION action, uint button) handler;
				handler.funcptr = target.handlers.focusOnClick;
				handler.ptr = cast(void*)target;
				if (handler(MOUSE_ACTION.PRESS, button))
				{
					T.focusedNode = target;
					this.window.redraw();  // FB.StateChanged
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

			// arguable focus stuff...
			if (target.handlers.focusOnClick !is null && T.focusedNode !is target)
			{
				bool delegate(MOUSE_ACTION action, uint button) handler;
				handler.funcptr = target.handlers.focusOnClick;
				handler.ptr = cast(void*)target;
				if (handler(MOUSE_ACTION.RELEASE, button))
				{
					T.focusedNode = target;
					this.window.redraw();  // FB.StateChanged
				}
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
		}
	}

	protected
	void passMouse(ref T target, const ref Point pos)
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
		auto translated_point = (!node.nested || node.parent is null) ?
				point :
				point - node.parent.position_abs();
		if (node._rect.contains(translated_point))
			return node;
	}
	return null;
}
