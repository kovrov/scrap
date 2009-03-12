import math
import pyglet
from pyglet.gl import *


def main():
	pyglet.resource.path = ['chromium-data']
	pyglet.resource.reindex()
	window = pyglet.window.Window(resizable=True)
	game = Game(window.width)

	@window.event
	def on_draw():
		window.clear()
		game.draw()

	@window.event
	def on_resize(width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)
		game.resize(width, height)

	#pyglet.clock.schedule(game.update)
	pyglet.clock.schedule_interval(game.update, 1/60.)
	pyglet.app.run()



class Game:
	"""
	actual game state and logic
	"""
	def __init__(self, width):
		#self.level = LevelOne()
		self.background = Background("png/gndMetalBase00.png", width)

	def resize(self, width, height):
		self.background.resize(width, height)

	def update(self, dt):
		# Add items to scene
		self.background.update(dt)
		# Update scene
		'''
		self.enemyFleet_update()
		self.powerUps_update()
		self.heroAmmo_updateAmmo()
		self.enemyAmmo.update()
		self.heroAmmo_checkForHits(game.enemyFleet)
		self.enemyAmmo.checkForHits(game.hero)
		self.hero_checkForCollisions(game.enemyFleet)
		self.hero_checkForPowerUps(game.powerUps)
		self.explosions_update()
		self.hero_update()
		'''

	def draw(self):
		self.background.draw()
		'''
		# Place camera
		glLoadIdentity(); glTranslatef(0f, 0f, config.zTrans())
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		# Draw background
		self.ground_drawGL()  # draw/update
		# Draw actors
		self.enemyFleet_drawGL()
		self.hero_drawGL()
		if config.gfxLevel() > 0:
			self.statusDisplay_darkenGL()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)
		self.powerUps_drawGL()
		# Draw ammo
		self.heroAmmo_drawGL()
		self.enemyAmmo.draw()
		# Draw explosions
		self.explosions_drawGL()
		# Draw stats
		self.statusDisplay_drawGL(game.hero)
		'''



class Background:
	""" animated tiles """
	def __init__(self, image, width):
		# texture quadrants
		self.tex2 = pyglet.resource.image(image).get_texture()
		self.tex1 = self.tex2.get_transform(flip_x=True)
		self.tex1.anchor_x = 0
		self.tex4 = self.tex2.get_transform(flip_x=True, flip_y=True)
		self.tex4.anchor_x = self.tex4.anchor_y = 0
		self.tex3 = self.tex2.get_transform(flip_y=True)
		self.tex3.anchor_y = 0
		self.totaltime = 0.
		self.scroll = 0.
		self.speed = 0.05

	def resize(self, width, height):
		self.scale = 1. / width if width > height else 1. / height

	def update(self, dt):
		self.totaltime += dt
		self.scroll -= dt * self.speed
		if self.scroll < -1.:
			self.scroll = 0.

	def draw_tiles(self, offset=0.):
		y = (self.scroll + offset) / self.scale
		size = 0.5/self.scale
		self.tex1.blit(size, y+size, width=size, height=size)
		self.tex2.blit(0, y+size,    width=size, height=size)
		self.tex3.blit(0, y,         width=size, height=size)
		self.tex4.blit(size, y,      width=size, height=size)

	def draw(self):
		# Set background color for low and med gfx
		pulse = math.sin(self.totaltime * 0.5)
		if pulse < 0.:
			pulse = 0.
		glClearColor(0.2+pulse, 0.2, 0.25, 1.)
		self.draw_tiles()
		self.draw_tiles(1.)


#-------------------------------------------------------------------------------

'''
def WTF():
	Global	*game = Global::getInstance()
	Config	*config = Config::instance()
	float targetAdj		= 1.0
	Uint32 now_time		= 0
	Uint32 last_time	= 0
	if not (game.gameFrame % 10):
		now_time = SDL_GetTicks()
		if last_time:
			game.fps = (10.0/(now_time-last_time))*1000.0
		last_time = now_time
		if game.gameMode != Global::Menu:
			if game.gameFrame < 400:
				if game.fps < 48.0 && game.gameSpeed < 1.0:
					game.gameSpeed += 0.02
					fprintf(stdout, "init---. %3.2ffps gameSpeed = %g\n", game.fps, game.gameSpeed)
				elif game.gameFrame > 20:
					float tmp = 50.0/game.fps
					tmp = 0.8*targetAdj + 0.2*tmp
					targetAdj = floor(100.0*(tmp+0.005))/100.0
					fprintf(stdout, "init---. %3.2ffps targetAdj = %g, tmp = %g\n", game.fps, targetAdj, tmp)
			elif config.autoSpeed() && (game.fps > 30.0 && game.fps < 100.0):  # discount any wacky fps from pausing
				# Everything was originally based on 50fps - attempt to adjust
				# if we're outside a reasonable range
				float tmp = 50.0/game.fps
				if fabs(targetAdj-tmp) > 0.1:
					adjCount += 1
					game.speedAdj = tmp
					fprintf(stdout, "adjust-. %3.2f targetAdj = %g -- game.speedAdj = %g\n", game.fps, targetAdj, game.speedAdj)
				else:
					game.speedAdj = targetAdj
			else:
				game.speedAdj = targetAdj


def process(SDL_Event *event):
	Global	*game = Global::getInstance()
	switch (event.type)
	    case SDL_ACTIVEEVENT:
			activation(event)
			break
	    case SDL_KEYDOWN:
			keyDown(event)
			break
	    case SDL_KEYUP:
			keyUp(event)
			break
	    case SDL_MOUSEMOTION:
			mouseMotion(event)
			break
	    case SDL_MOUSEBUTTONDOWN:
			mouseButtonDown(event)
			break
	    case SDL_MOUSEBUTTONUP:
			mouseButtonUp(event)
			break
		case SDL_JOYBUTTONDOWN:
			joystickButtonDown(event)
			break
		case SDL_JOYBUTTONUP:
			joystickButtonUp(event)
			break
		case SDL_QUIT:
			return true
		default:
			break
	return game.game_quit



class EnemyAmmo:
	def checkForHits(self, hero):
		minDist = (hero.getSize(0) + hero.getSize(1)) * 0.5
		if !hero.isVisible():
			return
		#-- Go through all the ammunition and check for hits
		for ammo_type in self.enemy_ammo_types:
			for ammo in ammo_type[:]:
				p = ammo.pos
				dist = abs(p[0]-hero.pos[0]) + abs(p[1]-hero.pos[1])
				if dist < minDist:
					#do damage
					hero.ammoDamage(ammoDamage[i], ammo.vel)
					#add explosion
					explo = game.explosions.addExplo(ammo_type, ammo.pos)
					if ammo_type == BUG_GUN:  # add second explosion for the bug guns...
						explo = game.explosions.addExplo(ammo_type, ammo.pos, -5)
					elif explo:
						explo.vel[1] = -0.1
					ammo_type.remove(ammo)
					killAmmo(ammo)
	def update(self):
		conf = Config()
		for ammo_type in self.enemy_ammo_types:
			for ammo in ammo_type[:]:  # clean up ammo
				if not intersects(conf.screenBound, ammo.pos):
					ammo_type.remove(ammo)
					killAmmo(ammo)
				else:
					ammo.updatePos()
	def draw(self):
		for ammo_type in self.enemy_ammo_types:
			glColor4f(1.0, 1.0, 1.0, 1.0)
			glBindTexture(GL_TEXTURE_2D, ammo_type.ammoTex)
			glBegin(GL_QUADS)
			for ammo in ammo_type:
				pos = ammo.pos
				ammoSize = ammo_type.ammoSize
				if 0 == IRAND % 4:
					glTexCoord2f(0.0, 0.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]+ammoSize[1], pos[2])
					glTexCoord2f(0.0, 1.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(1.0, 1.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(1.0, 0.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]+ammoSize[1], pos[2])
				elif 1 == IRAND % 4:
					glTexCoord2f(1.0, 0.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]+ammoSize[1], pos[2])
					glTexCoord2f(1.0, 1.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(0.0, 1.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(0.0, 0.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]+ammoSize[1], pos[2])
				elif 2 == IRAND % 4:
					glTexCoord2f(0.0, 1.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]+ammoSize[1], pos[2])
					glTexCoord2f(0.0, 0.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(1.0, 0.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(1.0, 1.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]+ammoSize[1], pos[2])
				elif 3 == IRAND % 4:
					glTexCoord2f(1.0, 1.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]+ammoSize[1], pos[2])
					glTexCoord2f(1.0, 0.0)
					glVertex3f(pos[0]-ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(0.0, 0.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]-ammoSize[1], pos[2])
					glTexCoord2f(0.0, 1.0)
					glVertex3f(pos[0]+ammoSize[0], pos[1]+ammoSize[1], pos[2])
			glEnd()



#-update------------------------------------------------------------------------


def put_screen_items(self): # ScreenItemAdd
	"""
	frame-based queue of game objects for current level
	"""
	for curItem in self.itemQueue[:]:
		if game.gameFrame < curItem.releaseTime:
			break
		if ScreenItem::ItemEnemy == curItem.item.itemType():
			game.enemyFleet.addEnemy(curItem.item)
		elif ScreenItem::ItemPowerUp == curItem.item.itemType():
			game.powerUps.addPowerUp(curItem.item)
		self.itemQueue.remove(curItem)


def enemyFleet_update(): # EnemyFleet
	EnemyAircraft	*thisEnemy;
	EnemyAircraft	*backEnemy;
	EnemyAircraft	*nextEnemy;
	#-- clean up enemies
	thisEnemy = squadRoot->next;

	while(thisEnemy)
	{
		thisEnemy->update();
		float p[3] = { thisEnemy->pos[0], thisEnemy->pos[1], thisEnemy->pos[2] };

		#-------------- Add some damage explosions to the bosses so
		#               we know when they're hurting...
		if((int)thisEnemy->type >= (int)EnemyBoss00)
		{
			float s[2] = { thisEnemy->size[0]*0.7, thisEnemy->size[1]*0.7 };
			if( thisEnemy->damage > thisEnemy->baseDamage*0.7 )
				if( !(game->gameFrame%18) )
				{
					p[0] = thisEnemy->pos[0] + SRAND*s[0];
					p[1] = thisEnemy->pos[1] + SRAND*s[1];
					p[2] = thisEnemy->pos[2];
					game->explosions->addExplo(Explosions::EnemyDamage, p, 0, 1.0);
				}
			if( thisEnemy->damage > thisEnemy->baseDamage*0.5 )
				if( !(game->gameFrame%10) )
				{
					p[0] = thisEnemy->pos[0] + SRAND*s[0];
					p[1] = thisEnemy->pos[1] + SRAND*s[1];
					p[2] = thisEnemy->pos[2];
					game->explosions->addExplo(Explosions::EnemyDamage, p, 0, 1.0);
				}
			if( thisEnemy->damage > thisEnemy->baseDamage*0.3 )
				if( !(game->gameFrame%4) )
				{
					p[0] = thisEnemy->pos[0] + SRAND*s[0];
					p[1] = thisEnemy->pos[1] + SRAND*s[1];
					p[2] = thisEnemy->pos[2];
					game->explosions->addExplo(Explosions::EnemyDamage, p, 0, 1.0);
				}
		}
		#-------------- Delete enemies that got through...

		if( thisEnemy->pos[1] < -8.0 && thisEnemy->type != EnemyGnat)
			game->statusDisplay->enemyWarning( 1.0-((thisEnemy->pos[1]+14.0)/6.0) );
		if( thisEnemy->pos[1] < -14.0 )
		{
			thisEnemy->damage = 1;
			thisEnemy->age = 0;
			game->hero->loseLife();
			game->tipShipPast++;
		}

		#-------------- If enemies are critically damaged, destroy them...
		if( thisEnemy->damage > 0 )
		{

			backEnemy = thisEnemy->back;
			nextEnemy = thisEnemy->next;
			backEnemy->next = nextEnemy;
			if(nextEnemy)
				nextEnemy->back = backEnemy;

			if(	thisEnemy->age ) #-- set age to 0 for silent deletion...
			{
				switch(thisEnemy->type)
				{
					case EnemyBoss01: #-- BIG explosion for the Boss...
					case EnemyBoss00: #-- BIG explosion for the Boss...
						#-- now for the BIG one...
						destroyAll();
						bossExplosion(thisEnemy);

						if( game->gameMode != Global::HeroDead )
						{
							#--*** TRIGGER END OF LEVEL ***--#
							game->hero->addScore(5000.0);
							game->gameMode = Global::LevelOver;
							game->heroSuccess = 0;
						}
						break;
					case EnemyOmni:
						game->hero->addScore(25.0);
						game->explosions->addExplo(Explosions::EnemyDamage, thisEnemy->pos);
						game->explosions->addExplo(Explosions::EnemyDamage, thisEnemy->pos, -3, 0.7);
						game->explosions->addExplo(Explosions::EnemyAmmo04, thisEnemy->pos);
						game->audio->playSound(Audio::ExploPop, thisEnemy->pos);
						break;
					case EnemyRayGun:
						game->hero->addScore(1000.0);
						game->explosions->addExplo(Explosions::EnemyDestroyed, p);
						p[0] = thisEnemy->pos[0]+0.55;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -5, 1.5);
						p[0] = thisEnemy->pos[0]-0.5;
						p[1] = thisEnemy->pos[1]+0.2;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -15);
						p[0] = thisEnemy->pos[0];
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -20, 2.0);
						game->explosions->addExplo(Explosions::EnemyDamage, p, -30, 2.0);
						game->audio->playSound(Audio::Explosion, thisEnemy->pos);
						game->audio->playSound(Audio::ExploBig, thisEnemy->pos);
						break;
					case EnemyTank:
						game->hero->addScore(1500.0);
						p[0] = thisEnemy->pos[0];
						p[1] = thisEnemy->pos[1];
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -5, 2.5);
						p[0] = thisEnemy->pos[0]-0.9;
						p[1] = thisEnemy->pos[1]-1.0;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -0, 1.5);
						p[0] = thisEnemy->pos[0]+1.0;
						p[1] = thisEnemy->pos[1]-0.8;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -13, 2.0);
						game->explosions->addExplo(Explosions::EnemyDestroyed, p,  -2, 1.0);
						p[0] = thisEnemy->pos[0]+0.7;
						p[1] = thisEnemy->pos[1]+0.7;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -20, 1.7);
						p[0] = thisEnemy->pos[0]-0.7;
						p[1] = thisEnemy->pos[1]+0.9;
						game->explosions->addExplo(Explosions::EnemyDestroyed, p, -8, 1.5);
						game->audio->playSound(Audio::Explosion, thisEnemy->pos);
						game->audio->playSound(Audio::ExploBig, thisEnemy->pos);
						break;
					case EnemyGnat:
						game->hero->addScore(10.0);
						game->explosions->addExplo(Explosions::EnemyAmmo04, thisEnemy->pos);
						game->audio->playSound(Audio::ExploPop, thisEnemy->pos);
						break;
					default:	#-- Add extra Damage explosion delayed for nice bloom
						game->hero->addScore(75.0);
						game->explosions->addExplo(Explosions::EnemyDestroyed, thisEnemy->pos);
						game->explosions->addExplo(Explosions::EnemyDamage, thisEnemy->pos, -15);
						game->audio->playSound(Audio::Explosion, thisEnemy->pos);
						break;
				}
			}

			killEnemy(thisEnemy);

			thisEnemy = backEnemy;
		}
		thisEnemy = thisEnemy->next;
	}


def powerUps_update(): # PowerUps
	Config	*config = Config::instance();

	PowerUp	*pwrUp;
	PowerUp *delUp;
	pwrUp = pwrUpRoot->next;
	while( pwrUp  )
	{
		pwrUp->age++;
		pwrUp->pos[1] += (speed*game->speedAdj);
		if(pwrUp->vel[0] || pwrUp->vel[1])
		{
			float s = (1.0-game->speedAdj)+(game->speedAdj*0.982);
			pwrUp->vel[0] *= s;
			pwrUp->vel[1] *= s;
			pwrUp->pos[0] += pwrUp->vel[0];
			pwrUp->pos[1] += pwrUp->vel[1];
			if(pwrUp->vel[0] < 0.01) pwrUp->vel[0] = 0.0;
			if(pwrUp->vel[1] < 0.01) pwrUp->vel[1] = 0.0;
		}
		float b = config->screenBoundX()-1.0;
		if(pwrUp->pos[0] < -b)
			pwrUp->pos[0] = -b;
		if(pwrUp->pos[0] >  b)
			pwrUp->pos[0] =  b;

		if(pwrUp->pos[1] < -12)
		{
			if(game->gameMode == Global::Game)
				switch(pwrUp->type)
				{
					case PowerUps::SuperShields:
						game->hero->addLife();
						game->hero->addScore(2500.0);
						break;
					case PowerUps::Shields:
					case PowerUps::Repair:
						game->hero->addScore(10000.0);
						break;
					default:
						game->hero->addScore(2500.0);
						break;
				}
			delUp = pwrUp;
			pwrUp = pwrUp->next;
			remove(delUp);
		}
		else
		{
			pwrUp = pwrUp->next;
		}
	}


def heroAmmo_updateAmmo(): # HeroAmmo
	Config *config = Config::instance();
	int i;
	ActiveAmmo *thisAmmo;

	for(i = 0; i < NUM_HERO_AMMO_TYPES; i++)
	{
		thisAmmo = ammoRoot[i]->next;
		while(thisAmmo)
		{
			#-- clean up ammo
			if(thisAmmo->pos[1] > config->screenBoundY()) # remove ammo
			{
				ActiveAmmo *backAmmo = thisAmmo->back;
				ActiveAmmo *nextAmmo = thisAmmo->next;
				backAmmo->next = nextAmmo;
				if(nextAmmo)
					 nextAmmo->back = backAmmo;
				killAmmo(thisAmmo);
				thisAmmo = nextAmmo; #ADVANCE
			}
			else
			{
				thisAmmo->updatePos();
				thisAmmo = thisAmmo->next; #ADVANCE
			}
		}
	}


def heroAmmo_checkForHits(EnemyFleet *fleet): # HeroAmmo
	int		i;
	float	minShipY = 100.0;
	ActiveAmmo		*thisAmmo;
	ActiveAmmo		*backAmmo;
	ActiveAmmo		*nextAmmo;
	EnemyAircraft	*enemy;

	#-- Get minimum ship Y location so we can ignore some of the ammunition
	fleet->toFirst();
	enemy = fleet->getShip();
	if(!enemy) #-- no ships - return immediately
		return;
	while(enemy)
	{
		if(enemy->pos[1]-3.0 < minShipY)
			minShipY = enemy->pos[1]-3.0;
		enemy = fleet->getShip();
	}

	#-- Go through all the ammunition and check for hits
	for(i = 0; i < NUM_HERO_AMMO_TYPES; i++)
	{
		thisAmmo = ammoRoot[i]->next;
		while(thisAmmo)
		{
			if(thisAmmo->pos[1] < minShipY)
			{
				thisAmmo = thisAmmo->next;
				continue;
			}
			fleet->toFirst();
			enemy = fleet->getShip();
			while(enemy)
			{
				if(enemy->checkHit(thisAmmo) == true)
				{
					#do damage
					if(i == 1)
						enemy->damage += ammoDamage[i]*game->speedAdj;
					else
						enemy->damage += ammoDamage[i];

					#add explosion
					game->explosions->addExplo((Explosions::ExploType)(Explosions::HeroAmmo00+i), thisAmmo->pos);

					if(i != 1) # ammo type 1 doesn't get killed
					{
						backAmmo = thisAmmo->back;
						nextAmmo = thisAmmo->next;
						backAmmo->next = nextAmmo;
						if(nextAmmo)
							 nextAmmo->back = backAmmo;
						killAmmo(thisAmmo);
						thisAmmo = backAmmo;
						enemy = 0; #-- break out of enemy loop
					}
					else
						enemy = fleet->getShip();
				}
				else
					enemy = fleet->getShip();
			}
			thisAmmo = thisAmmo->next;
		}
	}


def hero_checkForCollisions(EnemyFleet *fleet): # HeroAircraft
	float	p[3];
	float	r1,r2;
	float	diffX, diffY;
	float	dist;
	float	power;
	EnemyAircraft *enemy;

	fleet->toFirst();
	while( (enemy = fleet->getShip()) )
	{
		diffX = pos[0]-enemy->pos[0];
		diffY = pos[1]-enemy->pos[1];
		dist = fabs(diffX) + fabs(diffY);
		if(!dontShow && dist < enemy->size[0]+size[0])
		{
			#-- damage
			power = -enemy->damage*0.5;
			if(power > 35.0)
				power = 35.0;
			doDamage(power);
			if(shields > HERO_SHIELDS)
			{
				power*=0.5;	# reduce secondary movement when super shields are enabled
				enemy->damage += 70.0;
			}
			else
				enemy->damage += 40.0; # normal collision

			#-- explosions
			r1 = SRAND*0.3;
			r2 = SRAND*0.4;
			p[0] = enemy->pos[0]+r1;
			p[1] = enemy->pos[1]+r2;
			p[2] = enemy->pos[2];
			game->explosions->addExplo(Explosions::EnemyDamage, p);
			p[0] = pos[0]+r1;
			p[1] = pos[1]+0.2+r2;
			p[2] = pos[2];
			if(shields > 0.0)
				game->explosions->addExplo(Explosions::HeroShields, p);
			else
				game->explosions->addExplo(Explosions::HeroDamage, p);

			secondaryMove[0] =  diffX*power*0.03;
			secondaryMove[1] =  diffY*power*0.03;
			enemy->secondaryMove[0] -= diffX* enemy->collisionMove;
			enemy->secondaryMove[1] -= diffY*(enemy->collisionMove*0.5);

		}
		if(superBomb)
		{
			diffX = -enemy->pos[0];
			diffY = -15.0-enemy->pos[1];
			float dist = sqrt(diffX*diffX + diffY*diffY);
			if( (dist < superBomb*0.1 && enemy->type < EnemyBoss00) ||
				(enemy->pos[1] < -11.0) )
			{
				enemy->damage += 5000.0;
			}
			if(superBomb > 300)
				superBomb = 0;
		}
	}
	if(superBomb)
		superBomb += 2;


def hero_checkForPowerUps(PowerUps *powerUps): # HeroAircraft
	if(dontShow)
		return;
	float	dist;
	float	stock;
	PowerUp *pwrUp;
	PowerUp *delUp;

	if(score > scoreTarget)
	{
		scoreTarget += scoreStep;
		addLife(true);
	}

	float p0[3] = {10.4,-8.30, 25.0 };
	float v0[3] = { 0.0, 0.08, 0.0 };
	float clr[4] = { 1.0, 1.0, 1.0, 1.0 };
	if(game->gameMode == Global::Game)
		pwrUp = powerUps->getFirst();
	else
		pwrUp = 0;
	while( pwrUp )
	{
		dist = fabs(pos[0]-pwrUp->pos[0]) + fabs(pos[1]-pwrUp->pos[1]);
		if(dist < size[1])
		{
			game->audio->playSound(Audio::PowerUp, pos);
			switch(pwrUp->type)
			{
				case PowerUps::Shields:
					if(shields < HERO_SHIELDS)
						shields = HERO_SHIELDS;
					game->statusDisplay->setShieldAlpha(5.0);
					p0[0] = -10.4;
					game->explosions->addElectric(p0, v0, clr,  0);
					game->explosions->addElectric(p0, v0, clr, -1);
					game->explosions->addElectric(p0, v0, clr, -3);
					game->explosions->addElectric(p0, v0, clr, -4);
					break;
				case PowerUps::SuperShields:
					game->tipSuperShield++;
					damage -= shields;
					if(damage < HERO_DAMAGE)
						damage = HERO_DAMAGE;
					shields = HERO_SHIELDS*2;
					game->statusDisplay->setDamageAlpha(5.0);
					game->statusDisplay->setShieldAlpha(5.0);
					p0[0] = -10.4;
					game->explosions->addElectric(p0, v0, clr,  0);
					game->explosions->addElectric(p0, v0, clr, -1);
					game->explosions->addElectric(p0, v0, clr, -3);
					game->explosions->addElectric(p0, v0, clr, -4);
					game->explosions->addElectric(p0, v0, clr, -10);
					game->explosions->addElectric(p0, v0, clr, -11);
					game->explosions->addElectric(p0, v0, clr, -13);
					game->explosions->addElectric(p0, v0, clr, -14);
					p0[0] = 10.4;
					game->explosions->addElectric(p0, v0, clr,  0);
					game->explosions->addElectric(p0, v0, clr, -1);
					game->explosions->addElectric(p0, v0, clr, -3);
					game->explosions->addElectric(p0, v0, clr, -4);
					game->explosions->addElectric(p0, v0, clr, -10);
					game->explosions->addElectric(p0, v0, clr, -11);
					game->explosions->addElectric(p0, v0, clr, -13);
					game->explosions->addElectric(p0, v0, clr, -14);
					break;
				case PowerUps::Repair:
					game->statusDisplay->setDamageAlpha(5.0);
					damage = HERO_DAMAGE;
					p0[0] = 10.4;
					game->explosions->addElectric(p0, v0, clr,  0);
					game->explosions->addElectric(p0, v0, clr, -1);
					game->explosions->addElectric(p0, v0, clr, -3);
					game->explosions->addElectric(p0, v0, clr, -4);
					break;
				case PowerUps::HeroAmmo00:
					addScore(100.0);
					stock = ammoStock[0] + pwrUp->power*AMMO_REFILL;
					if(stock > AMMO_REFILL)
						stock = AMMO_REFILL;
					setAmmoStock(0, stock);
					break;
				case PowerUps::HeroAmmo01:
					addScore(100.0);
					stock = ammoStock[1] + pwrUp->power*AMMO_REFILL;
					if(stock > AMMO_REFILL)
						stock = AMMO_REFILL;
					setAmmoStock(1, stock);
					break;
				case PowerUps::HeroAmmo02:
					addScore(100.0);
					stock = ammoStock[2] + pwrUp->power*AMMO_REFILL;
					if(stock > AMMO_REFILL)
						stock = AMMO_REFILL;
					setAmmoStock(2, stock);
					break;
				default:
					break;
			}
			game->explosions->addExplo(Explosions::PowerBurst, pwrUp->pos);
			delUp = pwrUp;
			pwrUp = pwrUp->next;
			powerUps->remove(delUp);
		}
		else
		{
			pwrUp = pwrUp->next;
		}
	}


def explosions_update(): # Explosions
	Explo	*explo;
	Explo	*backExplo;
	Explo	*nextExplo;
	for(int i = 0; i < NumExploTypes; i++)
	{
		if(exploPause[i][0] > 0.0)
			exploPause[i][0] -= game->speedAdj;
		else
			exploPause[i][0] = 0.0;
		if(exploPause[i][2]) #-- if flag was set, init count
		{
			exploPause[i][0] = exploPause[i][1];
			exploPause[i][2] = 0.0;
		}

		explo = exploRoot[i]->next;
		while(explo)
		{
			explo->age++;
			if(explo->age > 0)
			{
				explo->pos[0] += explo->vel[0]*game->speedAdj;
				explo->pos[1] += explo->vel[1]*game->speedAdj;
				explo->pos[2] += explo->vel[2]*game->speedAdj;
			}
			if(explo->age > (exploStay[i]/game->speedAdj))
			{
				backExplo = explo->back;
				nextExplo = explo->next;
				backExplo->next = nextExplo;
				if(nextExplo)
					nextExplo->back = backExplo;
				killExplo(explo);
				explo = nextExplo;
			}
			else
				explo = explo->next;
		}
	}


def hero_update(): # HeroAircraft
	if(dontShow > 1)
	{
		pos[0] =  		cos(game->frame*0.02) * 9.0;
		pos[1] =  4.0 + sin(game->frame*0.07) * 2.0;
	}
	else if(dontShow == 1)
	{
		pos[0] =  0.0f;
		pos[1] = -3.0f;
	}

	#-- Gun flashes are drawn in StatusDisplay
	if(gunTrigger)
		shootGun();
	for(int i = 0; i < NUM_HERO_AMMO_TYPES; i++)
	{
		if(gunPause[i] >= 0)
			gunPause[i] -= game->speedAdj;
		if(gunTrigger)
		{
			float flash;
			float pause;
			switch(i)
			{
				case 0:
					flash = 5.0/game->speedAdj;
					pause = gunPause[i]/game->speedAdj;
					gunFlash0[i] = (flash-pause)/flash;
					if(gunActive[i])
						gunFlash1[i] = (flash-pause)/flash;
					else
						gunFlash1[i] = 0.0;
					break;
				case 1:
					flash = 10.0/game->speedAdj;
					pause = gunPause[i]/game->speedAdj;
					if(gunActive[i] && gunPause[i] < flash)
						gunFlash0[i] = (flash-pause)/flash;
					else
						gunFlash0[i] = 0.0;
					break;
				case 2:
					flash = 5.0/game->speedAdj;
					pause = gunPause[i]/game->speedAdj;
					if(gunActive[i])
					{
						if(gunPause[i] < flash)
						{
							if(gunSwap)
							{
								gunFlash0[i] = (flash-pause)/flash;
								gunFlash1[i] = 0.0;
							}
							else
							{
								gunFlash0[i] = 0.0;
								gunFlash1[i] = (flash-pause)/flash;
							}
						}
					}
					else
					{
						gunFlash0[i] = 0.0;
						gunFlash1[i] = 0.0;
					}
					break;
			}
		}
		else
		{
			if(gunFlash0[i] > 0.0)	gunFlash0[i] -= 0.075*game->speedAdj;
			else	gunFlash0[i] = 0.0;

			if(gunFlash1[i] > 0.0)	gunFlash1[i] -= 0.075*game->speedAdj;
			else	gunFlash1[i] = 0.0;
		}
	}

	#-- decrement item activation
	switch(currentItemIndex)
	{
		case 0: # self destruct
			useItemArmed -= 0.02;
			break;
		case 1:
			if(useItemArmed)
				doDamage(1);
			break;
	}
	if(useItemArmed < 0.0)
		useItemArmed = 0.0;

	#-- decrement supershields
	if(shields >= HERO_SHIELDS)
	{
		shields -= 0.15*game->speedAdj;

	}

	float s = (1.0-game->speedAdj)+(game->speedAdj*0.8);
	secondaryMove[0] *= s;
	secondaryMove[1] *= s;
	pos[0] += secondaryMove[0]*game->speedAdj;
	pos[1] += secondaryMove[1]*game->speedAdj;
	moveEvent(0,0);


#-draw--------------------------------------------------------------------------


def ground_drawGL(): # GroundMetal
	GroundSegment	*seg;
	GroundSegment	*tmp;
	float	s2 = size * 2.0;

	#-- Set background color for low and med gfx
	float	pulse = sin(game->gameFrame*0.03);
	if(pulse < 0.0)
		pulse = 0.0;
	glClearColor( 0.2+pulse, 0.2, 0.25, 1.0 );

	#-- draw ground segments
	if( !game->game_pause || game->gameMode == Global::Menu)
	{
		seg = rootSeg->next;
		while(seg)
		{
			seg->pos[1] += game->scrollSpeed*game->speedAdj;
			seg = seg->next;
		}
	}

	seg = rootSeg->next;
	while(seg)
	{
		seg->drawGL();

		if(seg->pos[1] < -s2)
		{
			float p[3] = { 0.0, seg->pos[1]+s2+s2, 0.0};
			float s[2] = { size, size };
			seg->back->next = 0;
			delete seg;
			tmp = new GroundMetalSegment(p, s, this);
			rootSeg->next->back = tmp;
			tmp->next = rootSeg->next;
			tmp->back = rootSeg;
			rootSeg->next = tmp;
			break;
		}
		seg = seg->next;
	}


def enemyFleet_drawGL(): # EnemyFleet
	float szx, szy;
	float *p;
	EnemyAircraft	*thisEnemy;

	glColor4f(1.0, 1.0, 1.0, 1.0);

	thisEnemy = squadRoot->next;
	while(thisEnemy)
	{
		p = thisEnemy->pos;
		szx = thisEnemy->size[0];
		szy = thisEnemy->size[1];
		glBindTexture(GL_TEXTURE_2D, shipTex[(int)thisEnemy->type]);
		glColor4f(1.0, 1.0, 1.0, 1.0);

		glPushMatrix();
		glTranslatef( p[0],  p[1],  p[2] );
		glBegin(GL_TRIANGLE_STRIP);
			glTexCoord2f(1.0, 0.0); glVertex3f( szx,  szy, 0.0);
			glTexCoord2f(0.0, 0.0); glVertex3f(-szx,  szy, 0.0);
			glTexCoord2f(1.0, 1.0); glVertex3f( szx, -szy, 0.0);
			glTexCoord2f(0.0, 1.0); glVertex3f(-szx, -szy, 0.0);
		glEnd();
		glPopMatrix();

		switch(thisEnemy->type)
		{
			case EnemyStraight:
				if(thisEnemy->preFire)
				{
					glBlendFunc(GL_SRC_ALPHA, GL_ONE);
					glBindTexture(GL_TEXTURE_2D, extraTex[EnemyStraight]);
					glColor4f(1.0, 1.0, 1.0, thisEnemy->preFire);
					szx = 0.55*thisEnemy->preFire;
					glPushMatrix();
					glTranslatef(p[0], p[1]-0.9, p[2]);
					glRotatef(IRAND, 0.0, 0.0, 1.0);
					drawQuad(szx,szx+0.1);
					glPopMatrix();
					glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
					glColor4f(1.0, 1.0, 1.0, 1.0);
				}
			 	if(!((thisEnemy->age-192)%256))
				{
					retarget(EnemyGnat, game->hero);
				}
				break;
			case EnemyOmni:
				glColor4f(1.0, 0.0, 0.0, 1.0);
				glBindTexture(GL_TEXTURE_2D, extraTex[EnemyOmni]);
				glPushMatrix();
				glTranslatef(p[0], p[1], p[2]);
				glRotatef(-(thisEnemy->age*8), 0.0, 0.0, 1.0);
				drawQuad(szx,szy);
				glPopMatrix();
				glColor4f(1.0, 1.0, 1.0, 1.0);
				break;
			case EnemyTank:
				if(thisEnemy->preFire)
				{
					glBlendFunc(GL_SRC_ALPHA, GL_ONE);
					glBindTexture(GL_TEXTURE_2D, extraTex[EnemyTank]);
					glColor4f(1.0, 1.0, 1.0, thisEnemy->preFire);
					glPushMatrix();
					glTranslatef(p[0], p[1]-0.63, p[2]);#NOTE: offset is ~szy*0.3
					glRotatef(IRAND, 0.0, 0.0, 1.0);
					szx = 0.4+0.6*thisEnemy->preFire;
					drawQuad(szx,szx);
					glPopMatrix();
					glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
					glColor4f(1.0, 1.0, 1.0, 1.0);
				}
				break;
			case EnemyBoss00:
				if(thisEnemy->preFire)
				{
					glBlendFunc(GL_SRC_ALPHA, GL_ONE);
					glBindTexture(GL_TEXTURE_2D, extraTex[EnemyBoss00]);
					glColor4f(1.0, 1.0, 1.0, thisEnemy->preFire);
					szx = 0.4+0.6*thisEnemy->preFire;
					glPushMatrix();
					glTranslatef(p[0]+1.1, p[1]-0.4, p[2]);
					glRotatef(IRAND, 0.0, 0.0, 1.0);
					drawQuad(szx,szx);
					glPopMatrix();
					glPushMatrix();
					glTranslatef(p[0]-1.1, p[1]-0.4, p[2]);
					glRotatef(IRAND, 0.0, 0.0, 1.0);
					drawQuad(szx,szx);
					glPopMatrix();
					glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
					glColor4f(1.0, 1.0, 1.0, 1.0);
				}
				break;
			case EnemyBoss01:
				if(thisEnemy->preFire)
				{
					glBlendFunc(GL_SRC_ALPHA, GL_ONE);
					glBindTexture(GL_TEXTURE_2D, extraTex[EnemyBoss01]);
					glColor4f(1.0, 1.0, 1.0, thisEnemy->preFire);
					szx = 0.9*thisEnemy->preFire;
					if(thisEnemy->shootSwap)
					{
						glPushMatrix();
						glTranslatef(p[0]-1.22, p[1]-1.22, p[2]);
						glRotatef(IRAND, 0.0, 0.0, 1.0);
						drawQuad(szx,szx);
						drawQuad(szx+0.2,szx+0.2);
						glPopMatrix();
					}
					else
					{
						glPushMatrix();
						glTranslatef(p[0]+0.55, p[1]-1.7, p[2]);
						glRotatef(IRAND, 0.0, 0.0, 1.0);
						drawQuad(szx,szx);
						drawQuad(szx+0.3,szx+0.3);
						glPopMatrix();
					}
					glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
					glColor4f(1.0, 1.0, 1.0, 1.0);
				}
			 	if(!((thisEnemy->age-272)%256))
				{
					retarget(EnemyGnat, game->hero);
				}
				break;
			default:
				break;
		}
		thisEnemy = thisEnemy->next;
	}


def hero_drawGL(): # HeroAircraft
	#-- draw hero
	glPushMatrix();
	glTranslatef(pos[0], pos[1], pos[2]);
	if(!dontShow)
	{
		glColor4f(1.0, 1.0, 1.0, 1.0);
		glBindTexture(GL_TEXTURE_2D, heroTex);
		drawQuad(size[0], size[1]);
	}
	else
	{
		dontShow--;
	}
	#-- draw super shields in StatusDisplay to get better blend mode...
	glPopMatrix();

	if(superBomb)
	{
		float s = superBomb*0.1;
		glBlendFunc(GL_SRC_ALPHA, GL_ONE);
		glBindTexture(GL_TEXTURE_2D, bombTex);
		glPushMatrix();
		glTranslatef(0.0, -15.0, HERO_Z);
		glRotatef(IRAND, 0.0, 0.0, 1.0);
		drawQuad(s,s);
		glPopMatrix();
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	}


def statusDisplay_darkenGL(): # StatusDisplay
	#-- sidebars
	glBindTexture(GL_TEXTURE_2D, shldTex);
	glBegin(GL_QUADS);
	glColor4f(0.25, 0.2, 0.2, 0.6);
		glTexCoord2f(0.0,  0.0); glVertex3f( -9.2,  8.5, 25.0);
		glTexCoord2f(1.0,  0.0); glVertex3f(-11.5,  8.5, 25.0);
	glColor4f(0.25, 0.25, 0.35, 0.6);
		glTexCoord2f(1.0,  1.7); glVertex3f(-11.5, -8.5, 25.0);
		glTexCoord2f(0.0,  1.7); glVertex3f( -9.2, -8.5, 25.0);

	glColor4f(0.25, 0.2, 0.2, 0.6);
		glTexCoord2f(1.0, 0.0); glVertex3f( 11.5,  8.5, 25.0);
		glTexCoord2f(0.0, 0.0); glVertex3f(  9.2,  8.5, 25.0);
	glColor4f(0.25, 0.25, 0.35, 0.6);
		glTexCoord2f(0.0, 1.7); glVertex3f(  9.2, -8.5, 25.0);
		glTexCoord2f(1.0, 1.7); glVertex3f( 11.5, -8.5, 25.0);

	glEnd();


def powerUps_drawGL(): # PowerUps
	float	*pos, *sz, szp;
	PowerUp	*pwrUp;

	pwrUp = pwrUpRoot->next;
	while(pwrUp)
	{
		pos	= pwrUp->pos;
		sz	= pwrUpSize[pwrUp->type];
		szp = sz[0]*2.5;

		glColor4fv(pwrUpColor[pwrUp->type]);
		glBindTexture(GL_TEXTURE_2D, pwrTex);
		glPushMatrix();
		glTranslatef(	pos[0]+wobble_0[pwrUp->age%WOBBLE_0],
						pos[1]+wobble_1[pwrUp->age%WOBBLE_1],
						pos[2]);
		glRotatef(IRAND, 0.0, 0.0, 1.0);
		glBegin(GL_QUADS);
		glTexCoord2f(0.0, 0.0); glVertex3f(-szp,  szp, 0.0 );
		glTexCoord2f(0.0, 1.0); glVertex3f(-szp, -szp, 0.0 );
		glTexCoord2f(1.0, 1.0); glVertex3f( szp, -szp, 0.0 );
		glTexCoord2f(1.0, 0.0); glVertex3f( szp,  szp, 0.0 );
		glEnd();
		glPopMatrix();

		pwrUp = pwrUp->next; #ADVANCE
	}

	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	pwrUp = pwrUpRoot->next;
	while(pwrUp)
	{
		pos	= pwrUp->pos;
		sz	= pwrUpSize[pwrUp->type];

		glColor4f(1.0, 1.0, 1.0, 1.0);
		glBindTexture(GL_TEXTURE_2D, tex[pwrUp->type]);
		glPushMatrix();
		glTranslatef(	pos[0]+wobble_0[pwrUp->age%WOBBLE_0],
						pos[1]+wobble_1[pwrUp->age%WOBBLE_1],
						pos[2]);
		glBegin(GL_QUADS);
		glTexCoord2f(0.0, 0.0); glVertex3f(-sz[0],  sz[1], 0.0);
		glTexCoord2f(0.0, 1.0); glVertex3f(-sz[0], -sz[1], 0.0);
		glTexCoord2f(1.0, 1.0); glVertex3f( sz[0], -sz[1], 0.0);
		glTexCoord2f(1.0, 0.0); glVertex3f( sz[0],  sz[1], 0.0);
		glEnd();
		glPopMatrix();

		pwrUp = pwrUp->next; #ADVANCE
	}

	glBlendFunc(GL_SRC_ALPHA, GL_ONE);


def heroAmmo_drawGL(): # HeroAmmo
	int i;
	float	*pos;
	ActiveAmmo 	*thisAmmo;

	for(i = 0; i < NUM_HERO_AMMO_TYPES; i++)
	{
		glColor4f(1.0, 1.0, 1.0, 1.0);
		glBindTexture(GL_TEXTURE_2D, ammoTex[i]);
		thisAmmo = ammoRoot[i]->next;
		glBegin(GL_QUADS);
		while(thisAmmo)
		{
			pos = thisAmmo->pos;
			glTexCoord2f(0.0, 0.0); glVertex3f(pos[0]-ammoSize[i][0], pos[1],     pos[2]);
			glTexCoord2f(0.0, 1.0); glVertex3f(pos[0]-ammoSize[i][0], pos[1]-ammoSize[i][1], pos[2]);
			glTexCoord2f(1.0, 1.0); glVertex3f(pos[0]+ammoSize[i][0], pos[1]-ammoSize[i][1], pos[2]);
			glTexCoord2f(1.0, 0.0); glVertex3f(pos[0]+ammoSize[i][0], pos[1],     pos[2]);
			thisAmmo = thisAmmo->next; #ADVANCE
		}
		glEnd()
	}


def explosions_drawGL(): # Explosions
	if(exploRoot[EnemyDestroyed]->next)	drawExplo(EnemyDestroyed);
	if(exploRoot[EnemyDamage]->next)	drawExplo(EnemyDamage);
	if(exploRoot[EnemyAmmo00]->next)	drawAmmo(EnemyAmmo00);
	if(exploRoot[EnemyAmmo01]->next)	drawAmmo(EnemyAmmo01);
	if(exploRoot[EnemyAmmo02]->next)	drawAmmo(EnemyAmmo02);
	if(exploRoot[EnemyAmmo03]->next)	drawAmmo(EnemyAmmo03);
	if(exploRoot[EnemyAmmo04]->next)	drawAmmo(EnemyAmmo04);

	if(exploRoot[HeroDestroyed]->next)	drawExplo(HeroDestroyed);
	if(exploRoot[HeroDamage]->next)		drawExplo(HeroDamage);
	if(exploRoot[HeroAmmo00]->next)		drawAmmo(HeroAmmo00);
	if(exploRoot[HeroAmmo01]->next)		drawAmmo(HeroAmmo01);
	if(exploRoot[HeroAmmo02]->next)		drawAmmo(HeroAmmo02);

	if(exploRoot[HeroShields]->next)	drawShields(HeroShields);
	if(exploRoot[PowerBurst]->next)		drawBurst(PowerBurst);

	if(exploRoot[AddLife]->next)		drawLife(AddLife);
	if(exploRoot[LoseLife]->next)		drawLife(LoseLife);
	if(exploRoot[ScoreLife]->next)		drawLife(ScoreLife);

	if(exploRoot[Electric]->next)		drawElectric(Electric);
	if(exploRoot[Glitter]->next)		drawGlitter(Glitter);


def statusDisplay_drawGL(HeroAircraft *hero): # StatusDisplay
	Config	*config = Config::instance();
	static	char scoreBuf[32];
	int 	i;
	bool 	statClrWarnAmmo = false;
	float	w = 0.1;
	float	x = 0.0,y,y3;
	float	size[2];
	float	ammoStock;

	if(!hero)
		return;
	if(!(game->frame%15) )
		blink = !blink;

	ammoAlpha *= 0.96;

	float	shields = hero->getShields();
	float	superShields = 0.0;
	float	damage	= hero->getDamage();
	if(shields > HERO_SHIELDS)
	{
		superShields = HERO_SHIELDS-(shields-HERO_SHIELDS);
		shields = HERO_SHIELDS;
	}

	#-- draw score
	glColor4f(1.0, 1.0, 1.0, 0.4);
	glPushMatrix();
		sprintf(scoreBuf, "%07d", (int)hero->getScore());
		glTranslatef(-9.0, -8.2, 25.0);
		glScalef(0.025, 0.02, 1.0);
		game->text->Render(scoreBuf);
	glPopMatrix();
	#-- draw fps
	if(config->showFPS())
	{
		glPushMatrix();
			sprintf(scoreBuf, "%3.1f", game->fps);
			glTranslatef(7.75, 8.0, 25.0);
			glScalef(0.018, 0.015, 1.0);
			game->text->Render(scoreBuf);
		glPopMatrix();
	}

	#-- draw ship lives
	glPushMatrix();
	glColor4f(0.6, 0.6, 0.7, 1.0);
	glBindTexture(GL_TEXTURE_2D, game->hero->heroTex);
	glTranslatef(10.2, 7.4, 25.0);
	size[0] = game->hero->getSize(0)*0.5;
	size[1] = game->hero->getSize(1)*0.5;
	for(i = 0; i < game->hero->getLives(); i++)
	{
		drawQuad(size[0], size[1]);
		glTranslatef(0.0, -size[1]*2.0, 0.0);
	}
	glPopMatrix();

	#-- draw usable items
	if(config->gfxLevel() > 1)
	{
		glPushMatrix();
		glColor4f(1.0, 1.0, 1.0, 1.0);
		glTranslatef(8.5, -7.7, 25.0);
		size[0] = 0.4;
		size[1] = 0.5;
		for(i = 0; i < NUM_HERO_ITEMS; i++)
		{
			if(i == game->hero->currentItem())
			{
				float a = game->hero->itemArmed()*0.8;
				glColor4f(0.4+a, 0.4, 0.4, 0.4+a);
				glBindTexture(GL_TEXTURE_2D, useFocus);
				drawQuad(size[1], size[1]);
				glColor4f(1.0, 1.0, 1.0, 1.0);
			}
			glBindTexture(GL_TEXTURE_2D, useItem[i]);
			drawQuad(size[0], size[0]);
			glTranslatef(-size[1]*2.0, 0.0, 0.0);
		}
		glPopMatrix();
	}

	#-- draw 'enemy-got-past' Warning
	if(enemyWarn && game->hero->getLives() >= 0)
	{
		glPushMatrix();
		glColor4f(1.0, 0.0, 0.0, enemyWarn+0.15*sin(game->gameFrame*0.7));
		glTranslatef(0.0, -8.75, 25.0);
		glBindTexture(GL_TEXTURE_2D, heroAmmoFlash[0]);
		drawQuad(12.0, 3.0);
		glPopMatrix();
		enemyWarn = 0.0;
	}

	#-- draw AMMO
	glPushMatrix();
	glTranslatef(statPosAmmo[0], statPosAmmo[1], statPosAmmo[2]);


	#--draw ammo reserves
	glBindTexture(GL_TEXTURE_2D, statTex);
	glBegin(GL_QUADS);
	for(i = 0; i < NUM_HERO_AMMO_TYPES; i++)
	{
 		glColor4fv(statClrAmmo[i]);
		ammoStock = hero->getAmmoStock(i);
		if(ammoStock > 0.0)
		{
			x = i*0.3;
			y = ammoStock*0.02;
			y3= y*2.65;
			if( blink || ammoStock > 50.0 )
				glColor4fv(statClrAmmo[i]);
			else
			{
				statClrWarnAmmo = true;
				glColor4fv(statClrWarn);
			}

			glTexCoord2f(1.0, 0.00); glVertex3f( x+w, -y3, 0.0 );
			glTexCoord2f(1.0,    y); glVertex3f( x+w, 0.0, 0.0 );
			glTexCoord2f(0.0,    y); glVertex3f( x-w, 0.0, 0.0 );
			glTexCoord2f(0.0, 0.00); glVertex3f( x-w, -y3, 0.0 );
		}
	}
	glEnd();

	glBindTexture(GL_TEXTURE_2D, topTex);
	if(statClrWarnAmmo)
		glColor4f(statClrWarn[0], statClrWarn[1], statClrWarn[2], 0.5+ammoAlpha);
	else
		glColor4f(0.5, 0.5, 0.5+ammoAlpha, 0.2+ammoAlpha);
	glBegin(GL_QUADS);
		glTexCoord2f(1.0,  1.0); glVertex3f(  1.25, -1.85, 0.0 );
		glTexCoord2f(1.0,  0.0); glVertex3f(  1.25,  0.47, 0.0 );
		glTexCoord2f(0.0,  0.0); glVertex3f( -0.75,  0.47, 0.0 );
		glTexCoord2f(0.0,  1.0); glVertex3f( -0.75, -2.85, 0.0 );
	glEnd();
	x += w*1.5;

	glPopMatrix();

	#--draw Shields
	damageAlpha *= 0.94;
	shieldAlpha *= 0.94;
	float	dc = damageAlpha*0.5;
	float   sc = shieldAlpha * 0.5;
	float	sl, sls, dl, dls;
	float	szx = 0.5;
	float	szy = 6.0;
	static	float rot = 0;
	rot+=2.0*game->speedAdj;
	float	rot2;
	rot2 = 2*((int)rot%180);

	sl  = sls = (shields/HERO_SHIELDS)-1.0;
	dl  = dls = ( damage/HERO_DAMAGE)-1.0;
	if(superShields)
		sls = dls = ((shields+superShields)/HERO_SHIELDS)-1.0;

	#------ draw Engine
	if(hero->isVisible() && config->gfxLevel() >= 1)
	{
		float c1f = 1.0+dl;
		float c2f = -dl;
		float c1[4] = { 0.85, 0.65, 1.00, 0.7 };
		float c2[4] = { 1.00, 0.20, 0.25, 0.7 };
		glColor4f(	c1[0]*c1f+c2[0]*c2f,
					c1[1]*c1f+c2[1]*c2f,
					c1[2]*c1f+c2[2]*c2f,
					c1[3]*c1f+c2[3]*c2f);
		glBindTexture(GL_TEXTURE_2D, heroAmmoFlash[0]);
		glPushMatrix();
		glTranslatef(hero->pos[0], hero->pos[1]-0.625, hero->pos[2]);
		float esz = 1.0+c2f;
		drawQuad(1.3, 0.5*esz);
		glTranslatef(0.0, -0.18, 0.0);
		glRotatef(IRAND, 0.0, 0.0, 1.0);
		drawQuad(0.85*esz, 0.6*esz);
		glPopMatrix();
	}

	#------ draw Super Shields
	if(superShields)
	{
		glPushMatrix();
		float sz = hero->getSize(1)*1.3;
		glColor4f(1.0, 1.0, 1.0, 1.0-sls*sls);
		glBindTexture(GL_TEXTURE_2D, heroSuperTex);
		glTranslatef(hero->pos[0], hero->pos[1], hero->pos[2]);
		glRotatef(IRAND, 0.0, 0.0, 1.0);
		drawQuad(sz, sz);
		glPopMatrix();

		#------ add a bit of Glitter...
		if(config->gfxLevel() > 1 && (!game->game_pause) )
		{
			float p[3] = { 0.0, 0.0, hero->pos[2] };
			float v[3] = { 0.01*SRAND, 0.0, 0.0 };
			float c[4] = { 1.0, 1.0, 0.7, 1.0-sls*sls };
			switch(game->gameFrame%2)
			{
				case 0:
					v[1] = -0.3+FRAND*0.05;
					p[0] = hero->pos[0];
					p[1] = hero->pos[1]-0.8;
					game->explosions->addGlitter(p, v, c, 0, 0.4+0.4*FRAND);
					v[1] = -0.25+FRAND*0.05;
					p[0] = hero->pos[0]+0.95;
					p[1] = hero->pos[1]+0.1;
					game->explosions->addGlitter(p, v, c, 0, 0.4+0.4*FRAND);
					p[0] = hero->pos[0]-0.95;
					p[1] = hero->pos[1]+0.1;
					game->explosions->addGlitter(p, v, c, 0, 0.4+0.4*FRAND);
					break;
				case 1:
					v[1] = -0.25+FRAND*0.05;
					p[0] = hero->pos[0]+0.95;
					p[1] = hero->pos[1]+0.1;
					game->explosions->addGlitter(p, v, c, 0, 0.4+0.4*FRAND);
					p[0] = hero->pos[0]-0.95;
					p[1] = hero->pos[1]+0.1;
					game->explosions->addGlitter(p, v, c, 0, 0.4+0.4*FRAND);
					break;
			}
		}
	}

	#---------- Draw ammo flash
	if(config->gfxLevel() > 1)
	{
		glPushMatrix();
		glTranslatef(hero->pos[0], hero->pos[1], hero->pos[2]);
		if(hero->gunFlash0[0])
		{
			glBindTexture(GL_TEXTURE_2D, heroAmmoFlash[0]);
			szx = hero->gunFlash0[0];
			szy = 0.46f*szx;
			glColor4f(0.75f, 0.75f, 0.75f, szx);
			glTranslatef( 0.275,  0.25, 0.0);
			drawQuad(szy, szy);
			glTranslatef(-0.550,  0.00, 0.0);
			drawQuad(szy, szy);
			glTranslatef( 0.275, -0.25, 0.0);

			if(hero->gunFlash1[0])
			{
				glTranslatef( 0.45, -0.10, 0.0);
				drawQuad(szy, szy);
				glTranslatef(-0.90,  0.00, 0.0);
				drawQuad(szy, szy);
				glTranslatef( 0.45,  0.10, 0.0);
			}
		}
		if(hero->gunFlash0[1])
		{
			glBindTexture(GL_TEXTURE_2D, heroAmmoFlash[1]);
			szx = hero->gunFlash0[1];
			szy = 0.8f*szx;
			glColor4f(1.0f, 1.0f, 1.0f, szx);
			glTranslatef(0.0,  0.7, 0.0);
			drawQuad(szy, szy);
			glTranslatef(0.0, -0.7, 0.0);
		}
		glBindTexture(GL_TEXTURE_2D, heroAmmoFlash[2]);
		if(hero->gunFlash0[2])
		{
			szx = hero->gunFlash0[2];
			szy = 0.65*szx;
			glColor4f(1.0f, 1.0f, 1.0f, szx);
			glTranslatef(-0.65, -0.375, 0.0);
			drawQuad(szy, szy);
			glTranslatef( 0.65,  0.375, 0.0);
		}
		if(hero->gunFlash1[2])
		{
			szx = hero->gunFlash1[2];
			szy = 0.65f*szx;
			glColor4f(1.0f, 1.0f, 1.0f, szx);
			glTranslatef( 0.65, -0.375, 0.0);
			drawQuad(szy, szy);
			glTranslatef(-0.65,  0.375, 0.0);
		}
		glPopMatrix();
	}

	#-- shield indicator
	glBindTexture(GL_TEXTURE_2D, shldTex);
	glColor4f(0.2, 0.2, 0.2, 0.5);
	glBegin(GL_QUADS);
	szx = 0.6;
	szy = 6.0;
		glTexCoord2f( 1.0, 1.0); glVertex3f(  statPosShld[0]+szx,  statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f(-2.5, 1.0); glVertex3f(  statPosShld[0]-2.0,  statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f(-2.5, 0.0); glVertex3f(  statPosShld[0]-2.0,  statPosShld[1]+0.0, statPosShld[2] );
		glTexCoord2f( 1.0, 0.0); glVertex3f(  statPosShld[0]+szx,  statPosShld[1]+0.0, statPosShld[2] );

		glTexCoord2f( 3.5, 1.0); glVertex3f( -statPosShld[0]+2.0,  statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f( 0.0, 1.0); glVertex3f( -statPosShld[0]-szx,  statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f( 0.0, 0.0); glVertex3f( -statPosShld[0]-szx,  statPosShld[1]+0.0, statPosShld[2] );
		glTexCoord2f( 3.5, 0.0); glVertex3f( -statPosShld[0]+2.0,  statPosShld[1]+0.0, statPosShld[2] );
	glEnd();

	if(config->gfxLevel() > 0)
	{
		#-- Shields
		if( (sl < -0.7 && blink && shields > 0.0) || superShields )
			glColor4fv(statClrWarn);
		else
			glColor4f(0.7+dc, 0.6+dc, 0.8+dc, 0.5+damageAlpha);
		glPushMatrix();
		glTranslatef(statPosShld[0], statPosShld[1], statPosShld[2]);
		glRotatef(-rot, 0.0, 1.0, 0.0);
		glBegin(GL_QUADS);
		szx = 0.5;
		glTexCoord2f( 1.0,     sls); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 0.0,     sls); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 0.0, 1.0+sls); glVertex3f( -szx,  0.0,  szx );
		glTexCoord2f( 1.0, 1.0+sls); glVertex3f(  szx,  0.0,  szx );

		glTexCoord2f( 0.0,     sls); glVertex3f(  szx,  szy, -szx );
		glTexCoord2f( 0.0, 1.0+sls); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 1.0, 1.0+sls); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 1.0,     sls); glVertex3f( -szx,  szy, -szx );

		glTexCoord2f( 1.0,     sls); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 1.0, 1.0+sls); glVertex3f(  szx,  0.0,  szx );
		glTexCoord2f( 0.0, 1.0+sls); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 0.0,     sls); glVertex3f(  szx,  szy, -szx );

		glTexCoord2f( 1.0,     sls); glVertex3f( -szx,  szy, -szx );
		glTexCoord2f( 1.0, 1.0+sls); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 0.0, 1.0+sls); glVertex3f( -szx,  0.0,  szx );
		glTexCoord2f( 0.0,     sls); glVertex3f( -szx,  szy,  szx );

		if(shields)
		{
			glTexCoord2f( 1.0, 1.0);
			glColor4f(0.3+sc, 0.4+sc, 1.0+sc, 0.5);
			glVertex3f(  szx,  0.0,  szx );
			glVertex3f(  szx,  0.0, -szx );
			glVertex3f( -szx,  0.0, -szx );
			glVertex3f( -szx,  0.0,  szx );
		}
		glEnd();

		glRotatef( rot2, 0.0, 1.0, 0.0);
		glColor4f(0.1+sc, 0.15+sc, 0.9+sc, 0.6+shieldAlpha);
		glBegin(GL_QUADS);
		szx = 0.4;
		glTexCoord2f( 1.0,     sl); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 0.0,     sl); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 0.0, 1.0+sl); glVertex3f( -szx,  0.0,  szx );
		glTexCoord2f( 1.0, 1.0+sl); glVertex3f(  szx,  0.0,  szx );

		glTexCoord2f( 0.0,     sl); glVertex3f(  szx,  szy, -szx );
		glTexCoord2f( 0.0, 1.0+sl); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 1.0, 1.0+sl); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 1.0,     sl); glVertex3f( -szx,  szy, -szx );

		glTexCoord2f( 1.0,     sl); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 1.0, 1.0+sl); glVertex3f(  szx,  0.0,  szx );
		glTexCoord2f( 0.0, 1.0+sl); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 0.0,     sl); glVertex3f(  szx,  szy, -szx );

		glTexCoord2f( 0.0,     sl); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 1.0,     sl); glVertex3f( -szx,  szy, -szx );
		glTexCoord2f( 1.0, 1.0+sl); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 0.0, 1.0+sl); glVertex3f( -szx,  0.0,  szx );
		glEnd();
		glPopMatrix();



		if( (dl < -0.7 && blink) || superShields )
		{
			glColor4fv(statClrWarn);
			if(config->texBorder())
				glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, statClrWarn );
		}
		else
		{
			glColor4f(0.9+dc, 0.6+dc, 0.7+dc, 0.5+damageAlpha);
			if(config->texBorder())
				glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, statClrZero );
		}
		#-- Life
		glPushMatrix();
		glTranslatef(-statPosShld[0], statPosShld[1], statPosShld[2]);
		glRotatef( rot, 0.0, 1.0, 0.0);

		glBegin(GL_QUADS);
		szx = 0.5;
		glTexCoord2f( 1.0,     dls); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 0.0,     dls); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 0.0, 1.0+dls); glVertex3f( -szx,  0.0,  szx );
		glTexCoord2f( 1.0, 1.0+dls); glVertex3f(  szx,  0.0,  szx );

		glTexCoord2f( 0.0,     dls); glVertex3f(  szx,  szy, -szx );
		glTexCoord2f( 0.0, 1.0+dls); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 1.0, 1.0+dls); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 1.0,     dls); glVertex3f( -szx,  szy, -szx );

		glTexCoord2f( 1.0,     dls); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 1.0, 1.0+dls); glVertex3f(  szx,  0.0,  szx );
		glTexCoord2f( 0.0, 1.0+dls); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 0.0,     dls); glVertex3f(  szx,  szy, -szx );

		glTexCoord2f( 0.0,     dls); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 1.0,     dls); glVertex3f( -szx,  szy, -szx );
		glTexCoord2f( 1.0, 1.0+dls); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 0.0, 1.0+dls); glVertex3f( -szx,  0.0,  szx );

		if(damage)
		{
			glTexCoord2f( 1.0, 1.0);
			glColor4f(1.0+dc, 0.0+dc, 0.0+dc, 0.5);
			glVertex3f(  szx,  0.0,  szx );
			glVertex3f(  szx,  0.0, -szx );
			glVertex3f( -szx,  0.0, -szx );
			glVertex3f( -szx,  0.0,  szx );
		}
		glEnd();

		glRotatef(-rot2, 0.0, 1.0, 0.0);
		glColor4f(1.0+dc, 0.0+dc, 0.0+dc, 0.6+damageAlpha);
		glBegin(GL_QUADS);
		szx = 0.4;
		glTexCoord2f( 1.0,     dl); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 0.0,     dl); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 0.0, 1.0+dl); glVertex3f( -szx,  0.0,  szx );
		glTexCoord2f( 1.0, 1.0+dl); glVertex3f(  szx,  0.0,  szx );

		glTexCoord2f( 0.0,     dl); glVertex3f(  szx,  szy, -szx );
		glTexCoord2f( 0.0, 1.0+dl); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 1.0, 1.0+dl); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 1.0,     dl); glVertex3f( -szx,  szy, -szx );

		glTexCoord2f( 1.0,     dl); glVertex3f(  szx,  szy,  szx );
		glTexCoord2f( 1.0, 1.0+dl); glVertex3f(  szx,  0.0,  szx );
		glTexCoord2f( 0.0, 1.0+dl); glVertex3f(  szx,  0.0, -szx );
		glTexCoord2f( 0.0,     dl); glVertex3f(  szx,  szy, -szx );

		glTexCoord2f( 0.0,     dl); glVertex3f( -szx,  szy,  szx );
		glTexCoord2f( 1.0,     dl); glVertex3f( -szx,  szy, -szx );
		glTexCoord2f( 1.0, 1.0+dl); glVertex3f( -szx,  0.0, -szx );
		glTexCoord2f( 0.0, 1.0+dl); glVertex3f( -szx,  0.0,  szx );

		glEnd();
		glPopMatrix();
	}
	else
	{
		szx = 0.8;
		if( (sl < -0.7 && blink && shields > 0.0) || superShields )
			glColor4fv(statClrWarn);
		else
			glColor4f(0.0+sc, 0.35+sc, 1.0+sc, 0.7+shieldAlpha);
		#-- Shields
		glBegin(GL_QUADS);
		glTexCoord2f( 1.0,     sl); glVertex3f( statPosShld[0]    , statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f( 0.0,     sl); glVertex3f( statPosShld[0]-szx, statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f( 0.0, 1.0+sl); glVertex3f( statPosShld[0]-szx, statPosShld[1]    , statPosShld[2] );
		glTexCoord2f( 1.0, 1.0+sl); glVertex3f( statPosShld[0]    , statPosShld[1]    , statPosShld[2] );
		#-- Life

		if( (dl < -0.7 && blink) )
			glColor4fv(statClrWarn);
		else
			glColor4f(1.0+dc, 0.0+dc, 0.0+dc, 0.7+damageAlpha);
		glTexCoord2f( 1.0,     dl); glVertex3f( -statPosShld[0]    , statPosShld[1]+szy, statPosShld[2] );
		glTexCoord2f( 1.0, 1.0+dl); glVertex3f( -statPosShld[0]    , statPosShld[1]    , statPosShld[2] );
		glTexCoord2f( 0.0, 1.0+dl); glVertex3f( -statPosShld[0]+szx, statPosShld[1]    , statPosShld[2] );
		glTexCoord2f( 0.0,     dl); glVertex3f( -statPosShld[0]+szx, statPosShld[1]+szy, statPosShld[2] );
		glEnd();
	}

	#-- print message if we're paused...
	if(game->game_pause)
	{
		float off[2];
		off[0] = 2.0 * sin(game->frame*0.01);
		off[1] = 1.0 * cos(game->frame*0.011);
		glPushMatrix();
		glTranslatef(-14.5, -3.0, 0.0);
		glScalef(0.21, 0.21, 1.0);
		glPushMatrix();
		glColor4f(1.0, 1.0, 1.0, 0.10*fabs(sin(game->frame*0.05)) );
		game->text->Render("p a u s e d");
		glPopMatrix();
		glColor4f(1.0, 1.0, 1.0, 0.10*fabs(sin(game->frame*0.03)) );
		glTranslatef(off[0], off[1], 0.0);
		game->text->Render("p a u s e d");
		glPopMatrix();
	}
	if( game->tipShipPast == 1 && game->gameLevel == 1)
	{
		game->tipShipPast++;
		tipShipShow = 200;
	}
	if( game->tipSuperShield == 1 && game->gameLevel == 1)
	{
		game->tipSuperShield++;
		tipSuperShow = 200;
	}
	if(	tipShipShow > 0 )
	{
		tipShipShow--;
		glPushMatrix();
		glTranslatef(-16, 13.0, 0.0);
		glScalef(0.035, 0.035, 1.0);
		glColor4f(1.0, 1.0, 1.0, tipShipShow/300.0 );
		const char *str = "do not let -any- ships past you! each one costs you a life!";
		game->text->Render(str);
		glPopMatrix();
	}
	if(	tipSuperShow > 0 )
	{
		tipSuperShow--;
		glPushMatrix();
		glTranslatef(-16, 13.0, 0.0);
		glScalef(0.035, 0.035, 1.0);
		glColor4f(1.0, 1.0, 1.0, tipSuperShow/300.0 );
		const char *str = "let super shields pass by for an extra life!";
		game->text->Render(str);
		glPopMatrix();
	}
'''



if __name__ == "__main__":
	main()
