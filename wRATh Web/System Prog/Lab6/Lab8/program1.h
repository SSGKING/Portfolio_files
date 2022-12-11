//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 8 program1.h

#ifndef PROGRAM1_H_INCLUDED
#define PROGRAM1_H_INCLUDED
#include "program1func.c"


void addBlockHeadToList( struct BLOCKHEAD_NODE ** blockhead_list);
void addBlockHeadAtPos( struct BLOCKHEAD_NODE ** blockhead_list,int x,int y);
void removeBlockHeadFromList( struct BLOCKHEAD_NODE ** blockhead_list, int index);
void removeChance(struct BLOCKHEAD_NODE ** blockhead_list);
void removePos(struct BLOCKHEAD_NODE ** blockhead_list,int x, int y);
void freeBlockHeadList( struct BLOCKHEAD_NODE ** blockhead_list);
void renderBlockHead(struct BLOCKHEAD_NODE * blockhead,SDL_Surface* screen);
void moveBlockHead(struct BLOCKHEAD_NODE * blockhead);
void renderBlockHeadList( struct BLOCKHEAD_NODE * blockhead_list,SDL_Surface* screen);
void moveBlockHeadList( struct BLOCKHEAD_NODE * blockhead_list);


#endif // PROGRAM1_H_INCLUDED
