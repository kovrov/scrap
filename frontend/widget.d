static import ui;

template base(BASE /* : ui.TargetNode */)
{
	class Widget : BASE
	{
		this(string name, BASE parent=null)
		{
			super(name, parent);
			this.mouseEventMask = ui.MOUSE.MOVE;
		}

		override ui.FEEDBACK onMouse(ref ui.MouseEvent ev) { return ui.FEEDBACK.NONE; }
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
		bool tracked;
		bool pressed;
		override ui.FEEDBACK onMouse(ref ui.MouseEvent ev)
		{
			switch (ev.type)
			{
			case ui.MOUSE.MOVE:
				assert (!this.tracked);
				this.mouseEventMask ^= ui.MOUSE.MOVE;
				this.tracked = true;
				return ui.FEEDBACK.Redraw | ui.FEEDBACK.TrackMouse;
			case ui.MOUSE.LEAVE:
				this.tracked = false;
				this.mouseEventMask |= ui.MOUSE.MOVE;
				return ui.FEEDBACK.Redraw;
			//case ui.MOUSE.DBLCLK:
			case ui.MOUSE.DOWN:
				this.pressed = true;
				return ui.FEEDBACK.Redraw;
			case ui.MOUSE.UP:
				this.pressed = false;
				return ui.FEEDBACK.Redraw;
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
