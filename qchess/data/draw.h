
struct DrawData
{
    qreal strokeWidth;
    QPen pen;
    QBrush brush;
    QPainterPath path;
    QPen pen2;
    QBrush brush2;
    QPainterPath path2;
};

DrawData cachedDrawData[BLACK_KING+1];

void initDraw()
{
    cachedDrawData[BLACK_BISHOP].strokeWidth = 0.033333333;

    cachedDrawData[BLACK_BISHOP].pen = QPen(QColor(0xFF,0x00,0x00));
    cachedDrawData[BLACK_BISHOP].brush = QBrush(QColor(0x00,0x00,0x00));

    cachedDrawData[BLACK_BISHOP].pen2 = QPen(QColor(0xFF,0xFF,0xFF));
    cachedDrawData[BLACK_BISHOP].brush2 = QBrush(QColor(0x00,0x00,0x00));

    QPainterPath *path = &cachedDrawData[BLACK_BISHOP].path;
    path->moveTo(0.20, 0.80);
    path->cubicTo(0.27522789, 0.77839269, 0.42477209, 0.8095738, 0.5, 0.75555555);
    path->cubicTo(0.57522791, 0.8095738, 0.72477211, 0.77839269, 0.8, 0.8);
    path->cubicTo(0.8, 0.8, 0.83657551, 0.81203349, 0.86666667, 0.84444444);
    path->cubicTo(0.85162109, 0.86605173, 0.83009115, 0.8663592, 0.8, 0.85555556);
    path->cubicTo(0.72477211, 0.83394827, 0.57522791, 0.86574429, 0.5, 0.83333333);
    path->cubicTo(0.42477209, 0.86574429, 0.27522789, 0.83394827, 0.2, 0.85555556);
    path->cubicTo(0.16990884, 0.8663592, 0.14837891, 0.86605173, 0.13333333, 0.84444444);
    path->cubicTo(0.16342449, 0.80122984, 0.2, 0.8, 0.2, 0.8);
    path->closeSubpath();
    path->moveTo(0.33333333, 0.71111111);
    path->cubicTo(0.38888888, 0.76666667, 0.61111111, 0.76666667, 0.66666667, 0.71111111);
    path->cubicTo(0.67777778, 0.67777778, 0.66666667, 0.66666667, 0.66666667, 0.66666667);
    path->cubicTo(0.66666667, 0.61111111, 0.61111111, 0.57777778, 0.61111111, 0.57777778);
    path->cubicTo(0.73333333, 0.54444444, 0.74444444, 0.32222222, 0.50, 0.23333333);
    path->cubicTo(0.25555556, 0.32222222, 0.26666667, 0.54444444, 0.38888888, 0.57777778);
    path->cubicTo(0.38888888, 0.57777778, 0.33333333, 0.61111111, 0.33333333, 0.66666667);
    path->cubicTo(0.33333333, 0.66666667, 0.32222222, 0.67777778, 0.33333333, 0.71111111);
    path->closeSubpath();
    path->addEllipse(0.44444444, 0.1111111, 0.11111112, 0.11111112);

    QPainterPath *path2 = &cachedDrawData[BLACK_BISHOP].path2;
    path2->moveTo(0.38888889, 0.57777778);
    path2->lineTo(0.61111111, 0.57777778);
    path2->moveTo(0.33333333, 0.66666667);
    path2->lineTo(0.66666667, 0.66666667);
    path2->moveTo(0.50, 0.34444444);
    path2->lineTo(0.50, 0.45555556);
    path2->moveTo(0.44444444, 0.40);
    path2->lineTo(0.55555556, 0.40);
}

void draw_pawn(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-180, -110);
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

void draw_knight(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-222, -85);
    QPainterPath path;
    path.moveTo(213.18227,65.21189);
    path.lineTo(195.93227,81.33689);
    path.lineTo(204.18227,90.83689);
    path.lineTo(222.43227,84.58689);
    path.cubicTo(222.43227,84.58689, 212.23368,90.28548, 203.43227,99.08689);
    path.cubicTo(194.55124,107.96792, 196.37897,124.76582, 199.56095,131.83689);
    path.lineTo(249.18227,131.83689);
    path.cubicTo(229.68227,107.83689, 265.87264,84.25027, 252.93227,61.83689);
    path.cubicTo(240.33234,40.01315, 220.0502,43.39299, 207.81044,59.46479);
    path.cubicTo(209.67754,61.33189, 211.45587,63.48549, 213.18227,65.21189);
    path.closeSubpath();
    painter->drawPath(path);
    painter->restore();
}

void draw_bishop(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-301, -100);
    QPainterPath path;
    path.moveTo(301.40625,46.4375);
    path.lineTo(280.03125,64.1875);
    path.lineTo(287.90625,86.78125);
    path.cubicTo(283.81111,90.47127, 281.21875,95.80724, 281.21875,101.75);
    path.cubicTo(281.21875,108.59041, 284.65986,114.64059, 289.875,118.28125);
    path.cubicTo(282.33354,118.91733, 277.15625,120.1414, 277.15625,121.5625);
    path.cubicTo(277.15625,123.2381, 284.31251,124.61345, 294.125,125.09375);
    path.cubicTo(292.45077,145.71238, 276.40625,128.80123, 276.40625,148.28125);
    path.lineTo(276.40625,154.25);
    path.lineTo(326.34375,154.25);
    path.lineTo(326.34375,148.28125);
    path.cubicTo(326.34375,128.80773, 310.30823,145.66256, 308.625,125.09375);
    path.cubicTo(318.45364,124.61494, 325.65625,123.23988, 325.65625,121.5625);
    path.cubicTo(325.65625,120.1414, 320.44771,118.91733, 312.90625,118.28125);
    path.cubicTo(318.13297,114.64468, 321.53125,108.59863, 321.53125,101.75);
    path.cubicTo(321.53125,95.82301, 318.98247,90.50148, 314.90625,86.8125);
    path.lineTo(322.78125,64.1875);
    path.lineTo(301.40625,46.4375);
    path.closeSubpath();
    path.moveTo(301.375,59.875);
    path.cubicTo(301.99825,59.875, 302.5,60.37675, 302.5,61);
    path.lineTo(302.5,66.4375);
    path.lineTo(308.15625,66.4375);
    path.cubicTo(308.7795,66.4375, 309.28125,66.85563, 309.28125,67.375);
    path.cubicTo(309.28125,67.89438, 308.7795,68.3125, 308.15625,68.3125);
    path.lineTo(302.5,68.3125);
    path.lineTo(302.5,77.75);
    path.cubicTo(302.5,78.37325, 301.99825,78.875, 301.375,78.875);
    path.cubicTo(300.75175,78.875, 300.25,78.37325, 300.25,77.75);
    path.lineTo(300.25,68.3125);
    path.lineTo(294.59375,68.3125);
    path.cubicTo(293.9705,68.3125, 293.46875,67.89438, 293.46875,67.375);
    path.cubicTo(293.46875,66.85563, 293.9705,66.4375, 294.59375,66.4375);
    path.lineTo(300.25,66.4375);
    path.lineTo(300.25,61);
    path.cubicTo(300.25,60.37675, 300.75175,59.875, 301.375,59.875);
    path.closeSubpath();
    painter->drawPath(path);
    painter->restore();
}

void draw_rook(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-147, -80);
    QPainterPath path;
    path.moveTo(122.28835, 46.4375);
    path.lineTo(122.3196,52.4375);
    path.cubicTo(122.3196,82.63614, 123.0779,107.3422, 147.25709,121.30207);
    path.cubicTo(171.78325,107.14188, 172.22584,83.5788, 172.22584,52.4375);
    path.lineTo(172.22584,46.4375);
    path.lineTo(163.60084,46.4375);
    path.lineTo(163.60084,54.84007);
    path.lineTo(151.60084,54.84007);
    path.lineTo(151.60084,46.4375);
    path.lineTo(142.94459,46.4375);
    path.lineTo(142.94459,54.84007);
    path.lineTo(130.91335,54.84007);
    path.lineTo(130.91335,46.4375);
    path.lineTo(122.28835,46.4375);
    path.closeSubpath();
    painter->drawPath(path);
    painter->restore();
}

void draw_queen(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-378, -110);
    QPainterPath path;
    path.moveTo(378.42367,46.4375);
    path.lineTo(373.07992,66.28125);
    path.lineTo(362.42367,59);
    path.lineTo(361.17367,75.71875);
    path.lineTo(350.95492,74.03125);
    path.lineTo(361.36117,98.1875);
    path.lineTo(361.73617,98.1875);
    path.cubicTo(359.56222,101.4046, 358.26742,105.29613, 358.26742,109.46875);
    path.cubicTo(358.26743,116.62489, 362.0162,122.86388, 367.64242,126.4375);
    path.cubicTo(359.54286,127.05246, 353.92366,128.33154, 353.92367,129.8125);
    path.cubicTo(353.92367,131.4988, 361.18936,132.8957, 371.14242,133.375);
    path.cubicTo(369.29106,155.3638, 353.45492,158.04561, 353.45492,168.6875);
    path.lineTo(353.45492,174.65625);
    path.lineTo(403.39242,174.65625);
    path.lineTo(403.36117,168.6875);
    path.cubicTo(403.36118,158.94586, 387.53383,155.76356, 385.70492,133.375);
    path.cubicTo(395.66615,132.89645, 402.95491,131.4997, 402.95492,129.8125);
    path.cubicTo(402.95492,128.33154, 397.33573,127.05246, 389.23617,126.4375);
    path.cubicTo(394.85347,122.86443, 398.57992,116.61742, 398.57992,109.46875);
    path.cubicTo(398.57992,105.29613, 397.31637,101.4046, 395.14242,98.1875);
    path.lineTo(395.51742,98.1875);
    path.lineTo(405.92367,74.03125);
    path.lineTo(395.70492,75.71875);
    path.lineTo(394.42367,59);
    path.lineTo(383.76742,66.28125);
    path.lineTo(378.42367,46.4375);
    path.closeSubpath();
    painter->drawPath(path);
    painter->restore();
}

void draw_king(QPainter *painter)
{
    painter->save();
	painter->scale(0.0066, 0.0066);
    painter->translate(-452, -120);
    QPainterPath path;
    path.moveTo(452.53128,46.4375);
    path.lineTo(452.53128,57.3125);
    path.lineTo(439.12503,57.3125);
    path.lineTo(439.12503,64.5625);
    path.lineTo(452.53128,64.5625);
    path.lineTo(452.53128,77.9375);
    path.lineTo(434.43753,87.22367);
    path.lineTo(440.93753,102.5625);
    path.cubicTo(437.47008,106.18321, 435.34378,111.09423, 435.34378,116.5);
    path.cubicTo(435.34379,124.00033, 439.44838,130.5316, 445.53128,134);
    path.cubicTo(436.83527,134.81534, 430.75003,136.66596, 430.75003,138.8125);
    path.cubicTo(430.75003,141.1369, 437.88863,143.08896, 447.75003,143.78125);
    path.cubicTo(444.60114,162.06426, 430.53128,164.77694, 430.53128,183.03125);
    path.lineTo(430.53128,189);
    path.lineTo(480.46878,189);
    path.lineTo(480.43753,183.03125);
    path.cubicTo(480.43754,164.62878, 466.15027,163.43737, 463.15628,143.78125);
    path.cubicTo(473.06664,143.09496, 480.25003,141.14431, 480.25003,138.8125);
    path.cubicTo(480.25003,136.66336, 474.15043,134.81383, 465.43753,134);
    path.cubicTo(471.53325,130.53687, 475.65628,124.00934, 475.65628,116.5);
    path.cubicTo(475.65628,111.34731, 473.71547,106.65842, 470.53128,103.09375);
    path.lineTo(477.56253,87.22367);
    path.lineTo(459.46878,77.9375);
    path.lineTo(459.46878,64.5625);
    path.lineTo(472.87503,64.5625);
    path.lineTo(472.87503,57.3125);
    path.lineTo(459.46878,57.3125);
    path.lineTo(459.46878,46.4375);
    path.lineTo(452.53128,46.4375);
    path.closeSubpath();
    painter->drawPath(path);
    painter->restore();
}
