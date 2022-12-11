//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 8 program1func.c

#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
struct BLOCKHEAD_NODE
{
    float x,y;  // position
    float dx,dy; // movement  component
    long color;
    int size;
    struct BLOCKHEAD_NODE * next;
};
inline void addBlockHeadToList( struct BLOCKHEAD_NODE ** blockhead_list)
{
//this function will add a blockhead node to the list and set up it’s attributes as described.
     while((*blockhead_list)!=NULL)
     {
        blockhead_list=&(*blockhead_list)->next;
     }
     (*blockhead_list) = (struct BLOCKHEAD_NODE* ) malloc(sizeof(struct BLOCKHEAD_NODE));



     (*blockhead_list)->x = rand()%501;
     (*blockhead_list)->y = rand()%201;
     (*blockhead_list)->dx = (rand()/(float)RAND_MAX) * 2 - 1;
     (*blockhead_list)->dy = (rand()/(float)RAND_MAX) * 2 - 1;
      int r = rand() % 256;
      int g = rand() % 256;
      int b = rand() % 256;

     (*blockhead_list)->color = ((r<<16)|(g<<8)|(b));
     (*blockhead_list)->size = rand()%11+10;
     (*blockhead_list)->next=NULL;
     //printf("Creating a blockhead!! \n");


}
inline void addBlockHeadAtPos( struct BLOCKHEAD_NODE ** blockhead_list,int x,int y)
{
     while((*blockhead_list)!=NULL)
     {
        blockhead_list=&(*blockhead_list)->next;
     }
     (*blockhead_list) = (struct BLOCKHEAD_NODE* ) malloc(sizeof(struct BLOCKHEAD_NODE));



     (*blockhead_list)->x = x;
     (*blockhead_list)->y = y;
     (*blockhead_list)->dx = (rand()/(float)RAND_MAX) * 2 - 1;;
     (*blockhead_list)->dy = (rand()/(float)RAND_MAX) * 2 - 1;;

      int r = rand() % 256;
      int g = rand() % 256;
      int b = rand() % 256;

     (*blockhead_list)->color = ((r<<16)|(g<<8)|(b));
     (*blockhead_list)->size = rand()%11+10;
     (*blockhead_list)->next=NULL;

}
inline void removeBlockHeadFromList( struct BLOCKHEAD_NODE ** blockhead_list, int index)
{
    //this function will remove a blockhead node from the list at the position indicated by index.
    int i=0;
     struct BLOCKHEAD_NODE * temp;
     while((*blockhead_list)!=NULL)
     {
       if(i==index)
       {
         temp=(*blockhead_list);
         (*blockhead_list)=(*blockhead_list)->next;
         free(temp);
         return;
       }
       blockhead_list=&(*blockhead_list)->next;
       i++;
     }
}
inline void removeChance(struct BLOCKHEAD_NODE ** blockhead_list)
{
    struct BLOCKHEAD_NODE * temp;
    int counter = 0;
    temp=(*blockhead_list);
    while((*blockhead_list)!=NULL)
    {

        int chance = rand()%11;
        if (chance == 1)
        {
            removeBlockHeadFromList(&temp,counter);
            counter --;
        }
        blockhead_list=&(*blockhead_list)->next;
        counter++;
    }
}

inline void removePos(struct BLOCKHEAD_NODE ** blockhead_list,int posx, int posy)
{
    struct BLOCKHEAD_NODE * temp;
    int counter = 0;
    temp=(*blockhead_list);
    while((*blockhead_list)!=NULL)
    {

        if(posx <= (((*blockhead_list)->x) + ((*blockhead_list)->size)) && posx >= (*blockhead_list)->x)
        {
            int i = (*blockhead_list)->x;
            printf("%d vs %d at %d\n",i,posx,counter);

            if((posy <= ((*blockhead_list) ->y + (*blockhead_list) ->size)) && (posy >= (*blockhead_list)->y))
            {
                removeBlockHeadFromList(&temp,counter);

                counter --;

            }
        }
        blockhead_list=&(*blockhead_list)->next;
        counter++;
    }

}
inline void freeBlockHeadList( struct BLOCKHEAD_NODE ** blockhead_list)
{
//this function will free all of the blockhead nodes in the list.
    struct BLOCKHEAD_NODE * temp;
    while((*blockhead_list)!=NULL)
    {
        temp=(*blockhead_list)->next;
        free(*blockhead_list);
        *blockhead_list=NULL;
        blockhead_list=&temp;
    }
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
inline void renderBlockHeadList( struct BLOCKHEAD_NODE * blockhead_list,SDL_Surface* screen)
{
//this function should render all of the items in the block head list.
    while(blockhead_list!=NULL)
    {

        renderBlockHead(blockhead_list,screen);

        blockhead_list=blockhead_list->next;

    }


}
inline void moveBlockHeadList( struct BLOCKHEAD_NODE * blockhead_list)
{
//this function should update all of the items in the block head list.
    while(blockhead_list!=NULL)
    {
        moveBlockHead(blockhead_list);
        blockhead_list=blockhead_list->next;
    }
}
