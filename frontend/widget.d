static import ui;


template base(BASE /* : ui.TargetNode */)
{
	class Widget : BASE
	{
		this(string name, BASE parent=null)
		{
			super(name, parent);
		}

		override ui.FB onMouseOver(ui.MOUSE_DIRECTION dir) { return ui.FB.NONE; }
		override ui.FB onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button/*, modifiers*/) { return ui.FB.NONE; }
		override ui.FB onMouseScroll(int x, int y) { return ui.FB.NONE; }
	}


	template parent_ctor() { this(string name, BASE parent) { super(name, parent); }}


	class Window : Widget, ui.Activatable
	{
		ui.Focusable focusedChild;
		this(string name, BASE parent)
		{
			super(name, parent);
		}

		override ui.FB activate()
		{
			BASE.focusedNode = focusedChild;
			return ui.FB.StateChanged;
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

	class Button : Widget, ui.Focusable
	{
		bool hot;
		bool pressed;
		this(string name, BASE parent)
		{
			super(name, parent);
		}

		override bool focusOnMouse(ui.MOUSE_ACTION action, uint button)
		{
			return (action == ui.MOUSE_ACTION.PRESS && button == 0) ? true : false;
		}

		override ui.FB onMouseOver(ui.MOUSE_DIRECTION dir)
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
