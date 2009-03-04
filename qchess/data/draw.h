
struct DrawData
{
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
    QPainterPath *path = NULL;
    cachedDrawData[BLACK_BISHOP].pen = QPen(QColor(0x00,0x00,0x00), 0.033333333);
    cachedDrawData[BLACK_BISHOP].brush = QBrush(QColor(0x00,0x00,0x00));
    path = &cachedDrawData[BLACK_BISHOP].path;
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
    cachedDrawData[BLACK_BISHOP].pen2 = QPen(QColor(0xFF,0xFF,0xFF), 0.033333333);
    cachedDrawData[BLACK_BISHOP].pen2.setCapStyle(Qt::RoundCap);
    path = &cachedDrawData[BLACK_BISHOP].path2;
    path->moveTo(0.38888889, 0.57777778);
    path->lineTo(0.61111111, 0.57777778);
    path->moveTo(0.33333333, 0.66666667);
    path->lineTo(0.66666667, 0.66666667);
    path->moveTo(0.50, 0.34444444);
    path->lineTo(0.50, 0.45555556);
    path->moveTo(0.44444444, 0.40);
    path->lineTo(0.55555556, 0.40);

    //
    cachedDrawData[WHITE_BISHOP].pen = QPen(QColor(0x00,0x00,0x00), 0.033333333);
    cachedDrawData[WHITE_BISHOP].brush = QBrush(QColor(0xFF,0xFF,0xFF));
    cachedDrawData[WHITE_BISHOP].path = cachedDrawData[BLACK_BISHOP].path;
    cachedDrawData[WHITE_BISHOP].pen2 = QPen(QColor(0x00,0x00,0x00), 0.033333333);
    cachedDrawData[WHITE_BISHOP].pen2.setCapStyle(Qt::RoundCap);
    cachedDrawData[WHITE_BISHOP].path2 = cachedDrawData[BLACK_BISHOP].path2;

    //
    cachedDrawData[WHITE_KNIGHT].pen = QPen(QColor(0x00,0x00,0x00), 0.033333333);
    cachedDrawData[WHITE_KNIGHT].brush = QBrush(QColor(0xFF,0xFF,0xFF));
    path = &cachedDrawData[WHITE_KNIGHT].path;
    path->moveTo(22.0/45.0, 10.0/45.0);
    path->cubicTo(32.5/45.0, 11.0/45.0,  38.5/45.0, 18.0/45.0,  38.0/45.0, 39.0/45.0);
    path->lineTo(15.0/45.0, 39.0/45.0);
    path->cubicTo(15.0/45.0, 30.0/45.0,  25.0/45.0, 32.5/45.0,  23.0/45.0, 18.0/45.0);
    //path->moveTo(24.0/45.0, 18.0/45.0);
    path->cubicTo(24.384461/45.0, 20.911278/45.0,  18.447064/45.0, 25.368624/45.0,  16.0/45.0, 27.0/45.0);
    path->cubicTo(13.0/45.0, 29.0/45.0,            13.180802/45.0, 31.342892/45.0,  11.0/45.0, 31.0/45.0);
    path->cubicTo(9.95828/45.0, 30.055984/45.0,    12.413429/45.0, 27.962451/45.0,  11.0/45.0, 28.0/45.0);
    path->cubicTo(10.0/45.0, 28.0/45.0,            11.187332/45.0, 29.231727/45.0,  10.0/45.0, 30.0/45.0);
    path->cubicTo(9.0/45.0, 30.0/45.0,             5.9968392/45.0, 30.999999/45.0,  6.0/45.0, 26.0/45.0);
    path->cubicTo(6.0/45.0, 24.0/45.0,             12.0/45.0, 14.0/45.0,            12.0/45.0, 14.0/45.0);
    path->cubicTo(12.0/45.0, 14.0/45.0,            13.885866/45.0, 12.097871/45.0,  14.0/45.0, 10.5/45.0);
    path->cubicTo(13.273953/45.0, 9.505631/45.0,   13.5/45.0, 8.5/45.0,   13.5/45.0, 7.5/45.0);
    path->cubicTo(14.5/45.0, 6.5/45.0,             16.5/45.0, 10.0/45.0,  16.5/45.0, 10.0/45.0);
    path->lineTo(18.5/45.0, 10.0/45.0);
    path->cubicTo(18.5/45.0, 10.0/45.0,  19.281781/45.0, 8.0/45.0,  21.0/45.0, 7.0/45.0);
    path->cubicTo(22.0/45.0, 7.0/45.0,   22.0/45.0, 10.0/45.0,            22.0/45.0, 10.0/45.0);
    //path->closeSubpath();
    cachedDrawData[WHITE_KNIGHT].pen2 = QPen(Qt::NoPen);
    cachedDrawData[WHITE_KNIGHT].brush2 = QBrush(QColor(0x00,0x00,0x00));
    path = &cachedDrawData[WHITE_KNIGHT].path2;
    path->addEllipse(8.0/45.0, 23.5/45,  2.0/45.0, 2.0/45.0);
    path->addEllipse(14.0/45.0, 15.5/45.0,  3.0/45.0, 2.0/45.0);

    //
    cachedDrawData[BLACK_KNIGHT].pen = QPen(QColor(0x00,0x00,0x00), 0.033333333);
    cachedDrawData[BLACK_KNIGHT].brush = QBrush(QColor(0x00,0x00,0x00));
    cachedDrawData[BLACK_KNIGHT].path = cachedDrawData[WHITE_KNIGHT].path;
    cachedDrawData[BLACK_KNIGHT].pen2 = QPen(Qt::NoPen);
    cachedDrawData[BLACK_KNIGHT].brush2 = QBrush(QColor(0xFF,0xFF,0xFF));
    cachedDrawData[BLACK_KNIGHT].path2 = cachedDrawData[WHITE_KNIGHT].path2;
    path = &cachedDrawData[BLACK_KNIGHT].path2;
    path->moveTo(24.55/45.0, 10.4/45.0);
    path->lineTo(24.1/45.0, 11.85/45.0);
    path->lineTo(24.6/45.0, 12.0/45.0);
    path->cubicTo(27.75/45.0, 13.0/45.0,  30.248526/45.0, 14.490454/45.0,  32.5/45.0, 18.75/45.0);
    path->cubicTo(34.751474/45.0, 23.009546/45.0,  35.747157/45.0, 29.05687/45.0,  35.25/45.0, 39.0/45.0);
    path->lineTo(35.2/45.0, 39.5/45.0);
    path->lineTo(37.45/45.0, 39.5/45.0);
    path->lineTo(37.5/45.0, 39.0/45.0);
    path->cubicTo(38.002843/45.0, 28.94313/45.0,  36.623526/45.0, 22.146704/45.0,  34.25/45.0, 17.65625/45.0);
    path->cubicTo(31.876474/45.0, 13.165796/45.0,  28.461041/45.0, 11.022853/45.0,  25.0625/45.0, 10.5/45.0);
    path->lineTo(24.55/45.0, 10.4/45.0);
    path->closeSubpath();
}
