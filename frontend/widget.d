static import ui;



template base(BASE /* : ui.TargetNode */)
{
	alias BASE Widget;
	template parent_ctor() { this(string name, BASE parent) { super(name, parent); }}


	class Window : Widget, ui.UpwardEventListener, ui.MouseHandler
	{
		ui.Focusable focusedChild;
		mixin parent_ctor;

		//override
		ui.FB activate()
		{
			// goes at the top of the Z order
			this.makeFirstChild();
			return ui.FB.StateChanged;
		}

		override void handleUpwardEvent(ref ui.MouseButtonEvent ev)
		{
			if (ev.action == ui.MOUSE_ACTION.PRESS)
				this.activate();
		}

		// MouseHandler
		override ui.FB onMouseOver(ui.MOUSE_DIRECTION dir) { return ui.FB.NONE; }
		override ui.FB onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button/*, modifiers*/)
		{
			this.activate();
			return ui.FB.StateChanged;
		}
		override ui.FB onMouseScroll(int x, int y) { return ui.FB.NONE; }
	}

	class Group : Widget
	{
		mixin parent_ctor;
	}

	class Radio : Widget
	{
		mixin parent_ctor;
	}

	class Button : Widget, ui.Focusable, ui.MouseHandler
	{
		bool hot;
		bool pressed;
		mixin parent_ctor;

		ui.FB onKey(uint keycode)
		{
			return ui.FB.NONE;
		}

		// Focusable
		override bool focusOnMouse(ui.MOUSE_ACTION action, uint button)
		{
			return (action == ui.MOUSE_ACTION.PRESS && button == 0) ? true : false;
		}

		// MouseHandler
		override ui.FB onMouseOver(ui.MOUSE_DIRECTION dir)
		{
			switch (dir)
			{
			case ui.MOUSE_DIRECTION.ENTER:
				assert (!this.hot);
				this.hot = true;
				return ui.FB.StateChanged;
			case ui.MOUSE_DIRECTION.LEAVE:
				assert (this.hot);
				this.hot = false;
				return ui.FB.StateChanged;
			}
			return ui.FB.NONE;
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
		override ui.FB onMouseScroll(int x, int y) { return ui.FB.NONE; }
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
