
void draw_white_pawn(QPainter *painter)
{
	painter->save();
	QPainterPath path;
	path.moveTo(180.01563, 79.906825);
	path.cubicTo(170.90762, 79.906825, 163.51562, 87.298825, 163.51562, 96.406825);
	path.cubicTo(163.51562, 102.96328, 167.34695, 108.58985, 172.89063, 111.25058);
	path.cubicTo(172.46695, 149.02276, 155.04687, 124.25971, 155.04687, 144.56308);
	path.lineTo(155.01562, 150.53183);
	path.lineTo(204.98438, 150.53183);
	path.lineTo(204.95313, 144.56308);
	path.cubicTo(204.95313, 124.25975, 187.56438, 149.02243, 187.14063, 111.25058);
	path.cubicTo(192.67052, 108.58472, 196.51563, 102.95321, 196.51563, 96.406825);
	path.cubicTo(196.51563, 87.298825, 189.12363, 79.906825, 180.01563, 79.906825);
	path.closeSubpath();
	painter->drawPath(path);
	painter->restore();
}
