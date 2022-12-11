//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 8 program2.h

#ifndef PROGRAM2_H_INCLUDED
#define PROGRAM2_H_INCLUDED
#include "program2func.c"
void addBlockHeadToList(struct BLOCKHEAD_ARRAY* array_ptr);
void addBlockHeadAtPos(struct BLOCKHEAD_ARRAY* array_ptr,int x,int y);
void removeBlockHeadFromList(struct BLOCKHEAD_ARRAY* array_ptr, int index);
void removeChance(struct BLOCKHEAD_ARRAY* array_ptr);
void removePos(struct BLOCKHEAD_ARRAY* array_ptr, int posx, int posy);
void freeBlockHeadList( struct BLOCKHEAD_ARRAY* array_ptr);
void renderBlockHead(struct BLOCKHEAD_NODE * blockhead,SDL_Surface* screen);
void moveBlockHead(struct BLOCKHEAD_NODE * blockhead);
void renderBlockHeadList(struct BLOCKHEAD_ARRAY* array_ptr,SDL_Surface* screen);
void moveBlockHeadList(struct BLOCKHEAD_ARRAY* array_ptr);
#endif // PROGRAM2_H_INCLUDED
