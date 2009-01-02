static import ui;

interface TopLevelWindow  // active window interface
{
	ui.FB activate();
	//ui.FB deactivate();
}

template base(BASE /* : ui.TargetNode */)
{
	class Widget : BASE
	{
		this(string name, BASE parent=null)
		{
			super(name, parent);
		}

		override ui.FB onMousePass(ui.MOUSE_DIRECTION dir) { return ui.FB.NONE; }
		override ui.FB onMouseMove(const ref ui.Point pos/*, vect*/) { return ui.FB.NONE; }
		override ui.FB onMouseDrag(const ref ui.Point pos/*, vect*/, uint[] buttons/*, modifiers*/) { return ui.FB.NONE; }
		override ui.FB onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button/*, modifiers*/) { return ui.FB.NONE; }
		override ui.FB onMouseScroll(int x, int y) { return ui.FB.NONE; }
	}


	template parent_ctor() { this(string name, BASE parent) { super(name, parent); }}


	class Window : Widget, TopLevelWindow
	{
		BASE focusedChild;
		this(string name, BASE parent)
		{
			super(name, parent);
		}
		override ui.FB activate()
		{
			BASE.focusedNode = focusedChild;
			return ui.FB.NONE;
		}
	}

	class Group : Widget
	{
		mixin parent_ctor;
	}

	class Radio : Widget
	{
		mixin parent_ctor;
	}

	class Button : Widget
	{
		bool hot;
		bool pressed;
		this(string name, BASE parent)
		{
			super(name, parent);
			this.focusPolicy = ui.FOCUS.TAB|ui.FOCUS.CLICK;
		}

		override ui.FB onMousePass(ui.MOUSE_DIRECTION dir)
		{
			switch (dir)
			{
			case ui.MOUSE_DIRECTION.ENTER:
				assert (!this.hot);
				this.hot = true;
				break;
			case ui.MOUSE_DIRECTION.LEAVE:
				assert (this.hot);
				this.hot = false;
				break;
			}
			return ui.FB.StateChanged;
		}

		override ui.FB onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button)
		{
			if (button != 0)
				return ui.FB.NONE;

			switch (action)
			{
			case ui.MOUSE_ACTION.PRESS:
				assert (!this.pressed);
				this.pressed = true;
				return ui.FB.CaptureMouse | ui.FB.StateChanged;
			case ui.MOUSE_ACTION.RELEASE:
				if (this.pressed)
				{
					this.pressed = false;
					return ui.FB.ReleaseMouse | ui.FB.StateChanged;
				}
				return ui.FB.NONE;
			}
		}
	}

	class Label : Widget
	{
		mixin parent_ctor;
	}

	class Dialog : Widget
	{
		mixin parent_ctor;
	}
}
