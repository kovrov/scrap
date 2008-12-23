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

		//override void onMouse(ref ui.MouseEvent ev) {}
		override void onMouse(ref BASE.EventType ev) {}
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
		//override void onMouse(ref ui.MouseEvent ev)
		override void onMouse(ref BASE.EventType ev)
		{
			this.tracked = true;
			//window.redraw
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
