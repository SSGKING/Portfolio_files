//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 8 program2func.c

#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>


struct BLOCKHEAD_NODE
{
    float x,y;  // position
    float dx,dy; // movement  component
    long color;
    int size;
};
struct BLOCKHEAD_ARRAY
{
    unsigned int num_items;
    struct BLOCKHEAD_NODE * Blockhead;
};


inline void addBlockHeadToList(struct BLOCKHEAD_ARRAY* array_ptr)
{
    if(array_ptr->num_items==0)
    {
        array_ptr->num_items++;
        array_ptr->Blockhead = (struct BLOCKHEAD_NODE *)malloc(sizeof(struct BLOCKHEAD_NODE));
    }
    else
    {
        array_ptr->num_items++;
        array_ptr->Blockhead = (struct BLOCKHEAD_NODE *)realloc(array_ptr->Blockhead,sizeof(struct BLOCKHEAD_NODE)*array_ptr->num_items);
    }
    array_ptr->Blockhead[array_ptr->num_items-1].x=rand()%501;
    array_ptr->Blockhead[array_ptr->num_items-1].y = rand()%201;
    array_ptr->Blockhead[array_ptr->num_items-1].dx = (rand()/(float)RAND_MAX) * 2 - 1;
    array_ptr->Blockhead[array_ptr->num_items-1].dy = (rand()/(float)RAND_MAX) * 2 - 1;
    int r = rand() % 256;
    int g = rand() % 256;
    int b = rand() % 256;
    array_ptr->Blockhead[array_ptr->num_items-1].color= ((r<<16)|(g<<8)|(b));
    array_ptr->Blockhead[array_ptr->num_items-1].size = rand()%11+10;
}
inline void addBlockHeadAtPos(struct BLOCKHEAD_ARRAY* array_ptr,int x,int y)
{
    if(array_ptr->num_items==0)
    {
        array_ptr->num_items++;
        array_ptr->Blockhead = (struct BLOCKHEAD_NODE *)malloc(sizeof(struct BLOCKHEAD_NODE));
    }
    else
    {
        array_ptr->num_items++;
        array_ptr->Blockhead = (struct BLOCKHEAD_NODE *)realloc(array_ptr->Blockhead,sizeof(struct BLOCKHEAD_NODE)*array_ptr->num_items);
    }
    array_ptr->Blockhead[array_ptr->num_items-1].x=x;
    array_ptr->Blockhead[array_ptr->num_items-1].y =y;
    array_ptr->Blockhead[array_ptr->num_items-1].dx = (rand()/(float)RAND_MAX) * 2 - 1;
    array_ptr->Blockhead[array_ptr->num_items-1].dy = (rand()/(float)RAND_MAX) * 2 - 1;
    int r = rand() % 256;
    int g = rand() % 256;
    int b = rand() % 256;
    array_ptr->Blockhead[array_ptr->num_items-1].color= ((r<<16)|(g<<8)|(b));
    array_ptr->Blockhead[array_ptr->num_items-1].size = rand()%11+10;
}
inline void removeBlockHeadFromList(struct BLOCKHEAD_ARRAY* array_ptr, int index)
{
    int i;

    for(i=index;i<=array_ptr->num_items-2;i++)
    {
        array_ptr->Blockhead[i].x=array_ptr->Blockhead[i+1].x;
        array_ptr->Blockhead[i].y=array_ptr->Blockhead[i+1].y;
        array_ptr->Blockhead[i].dx=array_ptr->Blockhead[i+1].dx;
        array_ptr->Blockhead[i].dy=array_ptr->Blockhead[i+1].dy;
        array_ptr->Blockhead[i].color=array_ptr->Blockhead[i+1].color;
        array_ptr->Blockhead[i].size=array_ptr->Blockhead[i+1].size;
    }
    array_ptr->num_items--;
    array_ptr->Blockhead = (struct BLOCKHEAD_NODE *)realloc(array_ptr->Blockhead,sizeof(struct BLOCKHEAD_NODE)*array_ptr->num_items);

}
inline void removeChance(struct BLOCKHEAD_ARRAY* array_ptr)
{
    int i;
    for(i=0;i<array_ptr->num_items;i++)
    {
        int chance = rand()%11;
        if (chance == 1)
        {
           removeBlockHeadFromList(array_ptr,i);
        }
    }
}
inline void removePos(struct BLOCKHEAD_ARRAY* array_ptr, int posx, int posy)
{
    int i;
    for(i=0;i<array_ptr->num_items;i++)
    {

        if(posx <= ((array_ptr -> Blockhead[i].x) + (array_ptr->Blockhead[i].size)) && (posx >= (array_ptr->Blockhead[i].x)))
        {


            if((posy <= ((array_ptr->Blockhead[i].y + array_ptr->Blockhead[i].size)) && (posy >= array_ptr->Blockhead[i].y)))
            {
                removeBlockHeadFromList(array_ptr,i);
            }
        }
    }
}

inline void freeBlockHeadList( struct BLOCKHEAD_ARRAY* array_ptr)
{
    array_ptr->num_items = 0;
    free(array_ptr->Blockhead);

}


inline void renderBlockHead(struct BLOCKHEAD_NODE * blockhead,SDL_Surface* screen)
{
//this function should draw the blockhead according that is appropriate for the structure elements.
    SDL_Rect rectangle_list[4];
    //FULL SQUARE

    SDL_Rect head;


    rectangle_list[0].x = blockhead->x;
    rectangle_list[0].y = blockhead->y;
    rectangle_list[0].w = blockhead->size;
    rectangle_list[0].h = blockhead->size;


    //Left eye
    rectangle_list[1].x = (blockhead->x + (blockhead->size*(0.2)));
    rectangle_list[1].y = (blockhead->y + (blockhead->size*(0.2)));
    rectangle_list[1].w = (blockhead->size * 0.2);
    rectangle_list[1].h = (blockhead->size * 0.2);

    //Right eye
    rectangle_list[2].x = (blockhead->x + (blockhead->size*(0.6)));
    rectangle_list[2].y = (blockhead->y + (blockhead->size*(0.2)));
    rectangle_list[2].w = (blockhead->size * 0.2);
    rectangle_list[2].h = (blockhead->size * 0.2);

    //mouth
    rectangle_list[3].x = (blockhead->x + (blockhead->size*(0.2)));
    rectangle_list[3].y = (blockhead->y + (blockhead->size*(0.6)));
    rectangle_list[3].w = (blockhead->size * 0.6);
    rectangle_list[3].h = (blockhead->size * 0.2);


    //SDL_FillRect(screen,&rectangle_list[0],SDL_MapRGB( screen->format, blockhead->color, blockhead->color, blockhead->color ));
    /*printf("blockhead x = %d\n",blockhead->x);
    printf("blockhead y = %d\n",blockhead->y);
    printf("blockhead w = %d\n",blockhead->size);
    printf("blockhead h = %d\n",blockhead->size);

    printf("Rectangle x = %d\n",rectangle_list[0].x);
    printf("Rectangle y = %d\n",rectangle_list[0].y);
    printf("Rectangle w = %d\n",rectangle_list[0].w);
    printf("Rectangle h = %d\n",rectangle_list[0].h);*/

    SDL_FillRect(screen,&rectangle_list[0],SDL_MapRGB( screen->format, (blockhead->color>>16 & 255), ((blockhead->color>>8)&255), (blockhead->color&255)));

    SDL_FillRect(screen,&rectangle_list[1],SDL_MapRGB( screen->format, 0, 0, 0 ));

    SDL_FillRect(screen,&rectangle_list[2],SDL_MapRGB( screen->format, 0, 0, 0 ));

    SDL_FillRect(screen,&rectangle_list[3],SDL_MapRGB( screen->format, 0, 0, 0 ));


}
inline void moveBlockHead(struct BLOCKHEAD_NODE * blockhead)
{
//this function should use the displacement vector to move the blockhead to a new position..
//Be sure to handle bouncing off of the window borders.

    blockhead->x = blockhead->x + (blockhead->dx/20);
    blockhead->y = blockhead->y + (blockhead->dy/20);

    if ((blockhead->x + blockhead->size) > 600)
        blockhead->dx = blockhead->dx * (-1);
    if ((blockhead->y + blockhead->size) > 300)
        blockhead->dy = blockhead->dy * (-1);
    if (blockhead->x < 0)
        blockhead->dx = blockhead->dx * (-1);
    if (blockhead->y < 0)
        blockhead->dy = blockhead->dy * (-1);

}
inline void renderBlockHeadList(struct BLOCKHEAD_ARRAY* array_ptr,SDL_Surface* screen)
{
    int i;
    for(i=0;i<array_ptr->num_items;i++)
    {
        renderBlockHead(&(array_ptr->Blockhead[i]),screen);
    }
}

inline void moveBlockHeadList(struct BLOCKHEAD_ARRAY* array_ptr)
{
    int i;
    for(i=0;i<array_ptr->num_items;i++)
    {
        moveBlockHead(&(array_ptr->Blockhead[i]));
    }
}











