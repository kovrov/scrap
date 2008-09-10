class Fraction
{
	int numerator;
	int denominator;
	init(int n, int d)
	{
		numerator = n;
		denominator = d;
		//TODO: validate/reduce the fraction.
	}
public:
	Fraction() { init(0, 1); }
	Fraction(int n, int d) { init(n, d); }

	Fraction operator+(const Fraction &other) const
	{
		// only like quantities can be added, so we have to have a common denominator.
		int n = numerator * other.denominator + other.numerator * denominator;
		int d = denominator * other.denominator;
		return Fraction(n, d);
	}
	Fraction operator-(const Fraction &other) const
	{
		// subtraction is analogous to addition.
		int n = numerator * other.denominator - other.numerator * denominator;
		int d = denominator * other.denominator;
		return Fraction(n, d);
	}
	Fraction operator*(const Fraction &other) const
	{
		// multiplication is staitforward...
		int n = numerator * other.numerator;
		int d = denominator * other.denominator;
		return Fraction(n, d);
	}
	Fraction operator/(const Fraction &other) const
	{
		// divition is multiplication to inverted other fraction.
		int n = numerator * other.denominator;
		int d = denominator * other.numerator;
		return Fraction(n, d);
	}
};
