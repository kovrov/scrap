#pragma once

struct Config
{
	struct Entity
	{
		unsigned int quantity;
		unsigned int size;
	} *ptr;
	unsigned len;
};


class Game
{
public:
	Game(void);
public:
	~Game(void);
private:
	Config m_conf;
};
