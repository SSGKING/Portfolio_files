//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 7 game_of_life.h
#ifndef GAME_OF_LIFE_H_INCLUDED
#define GAME_OF_LIFE_H_INCLUDED
#include "game_of_life.c"
#define BOARD_HEIGHT 100
#define BOARD_WIDTH 200
void init_board(int board[BOARD_HEIGHT][BOARD_WIDTH],int num_alive);
void add_cells(int board[BOARD_HEIGHT][BOARD_WIDTH],int num_alive);
void display_board(int board[BOARD_HEIGHT][BOARD_WIDTH],SDL_Surface* screen);
int num_neighbors(int board[BOARD_HEIGHT][BOARD_WIDTH],int x,int y);
int next_state(int board[BOARD_HEIGHT][BOARD_WIDTH],int x,int y);
void chance_kill(int board[BOARD_HEIGHT][BOARD_WIDTH]);
void next_generation(int board[BOARD_HEIGHT][BOARD_WIDTH]);
#endif // GAME_OF_LIFE_H_INCLUDED
