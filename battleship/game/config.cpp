#include "game.h"
#include <stdlib.h>
#include <assert.h>


Game::Game(void)
{
	// temproray hardcoded config
	m_conf.len = 4;
	m_conf.ptr = new Config::Entity[m_conf.len];
	m_conf.ptr[0].quantity = 1; m_conf.ptr[0].size = 4;  // one huge
	m_conf.ptr[1].quantity = 2; m_conf.ptr[1].size = 3;  // two bigs
	m_conf.ptr[2].quantity = 3; m_conf.ptr[2].size = 2;  // three mediums
	m_conf.ptr[3].quantity = 4; m_conf.ptr[3].size = 1;  // four smalls
}


Game::~Game(void)
{
	delete[] m_conf.ptr;
}
