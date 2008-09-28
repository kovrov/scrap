/* Q:

Come up with a suitable object oriented design for designing a set of
"playing card" games. Assume standard deck of cards; multiple people
participating in games; and a neutral dealer.  

Note: This is a design question and is meant to be little vague. Use
your imagination and write about 1/2 to 1 page (avoid too much detail)
of ideas on class design, hierarchy and some class variables. There
is no right or wrong answer and you will be evaluated for your
imagination and object oriented concepts.  
*/


/* A:

I would go with set of game entities like Card, Player, Dealer(?) classes.
There is no use of heirarchy(-ies) at this point, except perhaps to
refactor some common properties or interfaces (eg, Players and dealer could
have somthing common). But basically they are POD types (structs)

The most important class is Game - here incapsulated game logic and state
(of specific game, BlackJack, etc..), providing convinient interface.

Underlying mechanism would be a state machine (generic) and it's config
(set of states, tansitions etc. for a specific game). Reason for using
FSM is that all board games esetualy are state machines. But this is
rather implementation details.

*/

struct Card
{
	suit /* HEARTS, DIAMONDS, CLUBS, SPADES */
	rank  /* ACE, KING, QUEEN, JACK, 10 - 2? */
};

/* this is esentially a wrapper for a handle to the player of particular hame
handle is generic to all games, so the Player class/struct.
Other than handle it may hold methadata not strictly relevant for
specific game, such as credits/money, etc.. which may or may not affect
game logic of a specific game */
struct Player
{
	handle // is unique for game instance, and set by game instance
	/* why use handle to identify player? because Player instance memory address may change. */
	credits //money
};

/* Honestly I don't know if there is a point to have a Dealer class. 
If there is NO game type where dealer have to decide anything (not just draw
cards if player asks) - there is no need for the dealer class. Because all
the game "logic" (rules) and state are elswere (in *Game classes). I this
case the real dealer and (with the desk with cards) is real world card game
application analog.

I for game type where dealer may make any decitions, there would be
a game-specific AI (or human) dealer implementation. This could be useful
to decouple AI (human/network interface) implementation from game logic.
Again, if there is any. */

// Specific game class. For sake of example let it be a BlackJack game.
// BlackJackGame probably would be derived from a CardGame interface (if we
// have more than one game in one application)
class BlackJackGame : public CardGame
{
	// game specific methos if called in wrong state will throw

	/* depending on how players join and leaving game there will be 
	corresponding methonds to bind player handles to Player instances. */
	addPlayer(Player* player); // uses handle
	// we need some way to acually play game
	placeBet(Player* player); // uses handle and credits/money
	takeCard(Player* player); // uses handle and affect game state
	// etc...
	/* why not move (some of) this methods to Player class? 
	   because than we'd have lot of game specific Player classes
	   hard coupled to *Game classes implementations. */

	// we may need to introspect game in progress.
	/* these methods may or may not be needed - if for exaplme we have some
	   sort of callbacks for game state changes, application could track
	   this information on its own */
	getState(); // PLACING_BETS, WAITING_FOR_PLAYER_TO...
	getPlayers(); // return array of player instances (handles)
	playerCards(Player* player); // what cards specific player holds
	dealerCards() // see rationale for (not)having dealer instances.
	wichPlayersTurn() // to see who has to do something right now.
	// etc...
};

/* interface for application to handle any of games in generic way,
   eg. abort game on application exit. */
  
class CardGame
{
	abort() // why not just delete istance and have a cleanup in destructor? I downt know =) need more use cases
	save() // (?)
	// etc..
};
