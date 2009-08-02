/* 
  TODO:
   * finalize activatable concept
   * integrate focus interface
   * tweak button behaviour (keyboard)
   * implement radio button
   * introduce layout managers concept
   * ...
*/

static import ui;
import std.signals;


template base(BASE /* : ui.TargetNode */)
{
	alias BASE Widget;
	template parent_ctor()
	{
		protected static ui.EventHandlers!(BASE) _eventMap;
		this(string name, BASE parent) { super(name, parent); this.handlers = &_eventMap; }
	}


	class Window : Widget
	{
		BASE focusedChild;
		mixin parent_ctor;
		static this()
		{
			_eventMap.focus = &_onFocus;
			_eventMap.focusPropagateUpward = &_onFocusPropagateUpward;  // or downward?
		}

		protected ui.FB _onFocus(inout ui.FocusEvent!(BASE) ev)
		{
			this.activate();
			ev.target = this.focusedChild;
			return ui.FB.StateChanged;
		}
		protected ui.FB _onFocusPropagateUpward(inout ui.FocusEvent!(BASE) ev)
		{
			// set new focus (save)
			if (ev.accepted)
				this.focusedChild = ev.target;
			else
				ev.target = this.focusedChild;
			this.activate();
			return ui.FB.StateChanged;
		}

		// Activatable
		void activate()
		{
			// restore focus
			focusedNode = this.focusedChild; //FIXME: hack
			this.makeFirstChild();  // Z-order
			//activated.emit();
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
		mixin Signal!(bool) toggled;
	}

	class Button : Widget
	{
		// state
		bool hot;
		bool pressed;

		mixin parent_ctor;
		static this()
		{
			_eventMap.focus       = &_onFocus;
			_eventMap.keyboard    = &_onKeyboard;
			_eventMap.mouseOver   = &_onMouseOver;
			_eventMap.mouseButton = &_onMouseButton;
		}

		// KeyboardInput
		protected ui.FB _onFocus(inout ui.FocusEvent!(BASE) ev) //ui.MOUSE_ACTION action, uint button
		{
			//ev.accepted = (action == ui.MOUSE_ACTION.PRESS && button == 0) ? true : false;
			ev.accepted = true;
			return ui.FB.NONE;
		}
		ui.FB _onKeyboard(uint keycode, ui.KEY_ACTION action)
		{
			//if (keycode != SPACE)
			//	return ui.FB.NONE;
			switch (action)
			{
			case ui.KEY_ACTION.PRESS:
				break;
			case ui.KEY_ACTION.RELEASE:
				clicked.emit();  // call all the connected slots
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
					clicked.emit();
					this.pressed = false;
					return ui.FB.ReleaseMouse | ui.FB.StateChanged;
				}
				return ui.FB.NONE;
			default:
				assert (false);
			}
		}

		// signals
		mixin Signal!() clicked;
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
