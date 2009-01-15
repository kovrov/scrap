/* 
  TODO:
   * tweak button behaviour (keyboard)
   * implement radio button
   * ...
*/

static import ui;

template base(BASE /* : ui.TargetNode */)
{
	alias BASE Widget;
	template parent_ctor()
	{
		protected static ui.EventHandlers _eventMap;
		this(string name, BASE parent) { super(name, parent); this.handlers = &_eventMap; }
	}


	class Window : Widget
	{
		BASE focusedChild;
		mixin parent_ctor;
		static this()
		{
			_eventMap.mouseButton = &_onMouseButton;
			_eventMap.mouseButtonPropagateUpward = &_onMouseButton;
		}

		//override
		ui.FB activate()
		{
			// goes at the top of the Z order
			this.makeFirstChild();
			return ui.FB.StateChanged;
		}

		// MouseInput
		protected ui.FB _onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button/*, modifiers*/)
		{
			if (action != ui.MOUSE_ACTION.PRESS)
				return ui.FB.NONE;
			this.activate();
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
		// signals
		//mixin Signal!(bool) toggled;
	}

	class Button : Widget
	{
		// state
		bool hot;
		bool pressed;

		mixin parent_ctor;
		static this()
		{
			_eventMap.focusOnClick = &_focusOnClick;
			_eventMap.keyboard     = &_onKeyboard;
			_eventMap.mouseOver    = &_onMouseOver;
			_eventMap.mouseButton  = &_onMouseButton;
		}

		// KeyboardInput
		protected bool _focusOnClick(ui.MOUSE_ACTION action, uint button)
		{
			return (action == ui.MOUSE_ACTION.PRESS && button == 0) ? true : false;
		}
		ui.FB _onKeyboard(uint keycode, ui.KEY_ACTION action)
		{
			//if (keycode == ENTER || keycode == SPACE)
				//return ui.FB.NONE;
			switch (action)
			{
			case ui.KEY_ACTION.PRESS:
				break;
			case ui.KEY_ACTION.RELEASE:
				//clicked.emit();  // call all the connected slots
				break;
			}
			return ui.FB.NONE;
		}

		// MouseInput
		protected ui.FB _onMouseOver(ui.MOUSE_DIRECTION dir)
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
		protected ui.FB _onMouseButton(const ref ui.Point pos, ui.MOUSE_ACTION action, uint button)
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
					// call all the connected slots
					//clicked.emit();
					this.pressed = false;
					return ui.FB.ReleaseMouse | ui.FB.StateChanged;
				}
				return ui.FB.NONE;
			}
		}

		// signals
		//mixin Signal!() clicked;
		/*	usage:
			this.clicked.connect(&observer.watch);
			this.clicked.disconnect(&observer.watch);
		*/
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
