//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 8 program1.c
#include "program1.h"
#include <stdio.h>
#include <stdlib.h>
#include <SDL2/SDL.h>

int main(int argc, char *argv[])
{
    int SCREEN_WIDTH = 600;
    int SCREEN_HEIGHT = 300;
    SDL_Window* window = NULL;
    SDL_Surface* screenSurface = NULL;

    if( SDL_Init(SDL_INIT_VIDEO) < 0 )
    {
        printf( "SDL not initialized. SDL_Error: %s\n", SDL_GetError() );
    }
    else
    {
        //Create window
        window = SDL_CreateWindow( "Blockhead", SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN );
        if( window == NULL )
        {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
        }
        else
        {
            //Get window surface
            screenSurface = SDL_GetWindowSurface( window );
            //Fill the surface white
            SDL_FillRect( screenSurface, NULL,
            SDL_MapRGB( screenSurface->format, 0, 0, 0 ) );
            //Update the surface
            SDL_UpdateWindowSurface( window );
            //Wait five seconds
            SDL_Delay( 5000 );
        }
    }
    int pause = 0;
    int done = 0;
    SDL_Event e;
    int times = 0;
    struct BLOCKHEAD_NODE * list = NULL;
    srand(time(NULL));
    for(int times = 0;times < 30; times++)
    {
        addBlockHeadToList(&list);
    }
    int mox;
    int moy;



    while (done == 0)
    {
        SDL_GetMouseState(&mox,&moy);
        if(pause!=1)
        {

            moveBlockHeadList(list);

        }
        screenSurface = SDL_GetWindowSurface( window );
        SDL_FillRect( screenSurface, NULL,SDL_MapRGB( screenSurface->format, 0, 0, 0 ) );
        renderBlockHeadList(list,screenSurface);
        SDL_UpdateWindowSurface( window );
        while(SDL_PollEvent(&e)!=0)
        {
            if(e.window.event== SDL_WINDOWEVENT_CLOSE)
            {
                printf("bye!");
                //FREE LIST
                freeBlockHeadList(&list);
                //Destroy window
                SDL_DestroyWindow( window );
                //Quit SDL subsystems
                SDL_Quit();
                done++;
            }

            if(e.type == SDL_KEYDOWN)
            {
                if(e.key.keysym.sym == SDLK_a)
                {
                    int times = 0;
                    for(int times = 0;times < 10; times++)
                    {
                        addBlockHeadToList(&list);
                    }
                }
                if(e.key.keysym.sym == SDLK_p)
                {
                    if(pause==0)
                    {
                        pause = 1;
                    }
                    else
                    {
                        pause = 0;
                    }
                }
                if(e.key.keysym.sym == SDLK_r)
                {
                    removeChance(&list);
                }
            }
            if(e.type == SDL_MOUSEBUTTONDOWN)
            {
                if(e.button.button == SDL_BUTTON_LEFT)
                {
                    addBlockHeadAtPos(&list,mox,moy);
                }
                if(e.button.button == SDL_BUTTON_RIGHT)
                {
                    removePos(&list,mox,moy);
                }
            }
        }

    }

}
