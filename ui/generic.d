struct Point(T)
{
	T x, y;
	const Point opAdd(const ref Point other) { return Point(x +  other.x, y +  other.y); }
	const Point opSub(const ref Point other) { return Point(x -  other.x, y -  other.y); }
	void opAddAssign(const ref Point other)               { x += other.x; y += other.y; }
	void opSubAssign(const ref Point other)               { x -= other.x; y -= other.y; }
}

struct Size(T) { T width, height; }

struct Rect(PT, ST)
{
	//union
	//{
		generic.Point!(PT) position;//origin;
	//	struct{ PT x, y; }
	//}
	//union
	//{
		generic.Size!(ST) size;
	//	struct{ ST width, height; }
	//}

	bool contains(const ref typeof(this.position) point)
	{
		return position.x <= point.x && position.y <= point.y &&
				point.x <= position.x + size.width && point.y <= position.y + size.height;
	}
}
