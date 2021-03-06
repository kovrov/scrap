struct Point(T)
{
	T x, y;
	typeof(this) opAdd(const ref typeof(this) other) const { return typeof(this)(cast(T)(x + other.x), cast(T)(y + other.y)); }
	typeof(this) opSub(const ref typeof(this) other) const { return typeof(this)(cast(T)(x - other.x), cast(T)(y - other.y)); }
	void opAddAssign(const ref typeof(this) other)               { x += other.x; y += other.y; }
	void opSubAssign(const ref typeof(this) other)               { x -= other.x; y -= other.y; }
}

struct Size(T) { T width, height; }

struct Rect(PT, ST)
{
	union
	{
		Point!(PT) position;
		struct{ PT x, y; }
	}
	union
	{
		Size!(ST) size;
		struct{ ST width, height; }
	}

	//this(const ref typeof(this.position) pt, const ref typeof(this.size) sz) { position=pt; size=sz; }
	//this(PT x, PT y, ST width, ST height) { this.x = x; this.y = y; this.width = width; this.height = height; }

	bool contains(const ref typeof(this.position) point) const
	{
		return this.x <= point.x && this.y <= point.y &&
				point.x < this.x + this.width && point.y < this.y + this.height;
	}
}
