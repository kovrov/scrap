static import ui;

template base(BASE /* : ui.TargetNode */)
{
	class Widget : BASE
	{
		this(string name, BASE parent=null)
		{
			super(name, parent);
		}

		override ui.FEEDBACK onMousePass(ui.MOUSE_DIRECTION dir) { return ui.FEEDBACK.NONE; }
		override ui.FEEDBACK onMouseMove(const ref ui.Point pos/*, vect*/) { return ui.FEEDBACK.NONE; }
		override ui.FEEDBACK onMouseDrag(const ref ui.Point pos/*, vect*/, uint[] buttons/*, modifiers*/) { return ui.FEEDBACK.NONE; }
		override ui.FEEDBACK onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button/*, modifiers*/) { return ui.FEEDBACK.NONE; }
		override ui.FEEDBACK onMouseScroll(int x, int y) { return ui.FEEDBACK.NONE; }
	}


	template parent_ctor() { this(string name, BASE parent) { super(name, parent); }}


	class Window : Widget
	{
		mixin parent_ctor;
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
		mixin parent_ctor;
		bool hot;
		bool pressed;

		override ui.FEEDBACK onMousePass(ui.MOUSE_DIRECTION dir)
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
			return ui.FEEDBACK.Redraw;
		}

		override ui.FEEDBACK onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button)
		{
			switch (action)
			{
			case ui.MOUSE_ACTION.PRESS:
				assert (!this.pressed);
				this.pressed = true;
				return ui.FEEDBACK.CaptureMouse | ui.FEEDBACK.Redraw;
			case ui.MOUSE_ACTION.RELEASE:
				if (this.pressed)
				{
					this.pressed = false;
					return ui.FEEDBACK.ReleaseMouse | ui.FEEDBACK.Redraw;
				}
				return ui.FEEDBACK.NONE;
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
