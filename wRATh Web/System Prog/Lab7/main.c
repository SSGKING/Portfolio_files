//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 7 main.c
#include <SDL2/SDL.h>
#include "game_of_life.h"
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
    int SCREEN_WIDTH = 1001;
    int SCREEN_HEIGHT = 501;
    SDL_Window* window = NULL;   //The window we'll be rendering to
    SDL_Surface* screenSurface = NULL; //The surface contained by the window
    //Initialize SDL
    int red = 255;
    int blue = 255;
    int green = 255;
    if( SDL_Init(SDL_INIT_VIDEO) < 0 )
    {
        printf( "SDL not initialized. SDL_Error: %s\n", SDL_GetError() );
    }
    else
    {
        //Create window
        window = SDL_CreateWindow( "SDL Tutorial", SDL_WINDOWPOS_UNDEFINED,
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
    int board[BOARD_HEIGHT][BOARD_WIDTH];
    int i;
    int j;

    init_board(board,10000);
    screenSurface = SDL_GetWindowSurface( window );
    display_board(board,screenSurface);

    char inputdata [100] = "\0";
    int done = 0;
    int loop = 0;
    int pause = 0;
    SDL_Event e;
    while (done==0)
    {
        if(pause!=1)
        {
            next_generation(board);
            screenSurface = SDL_GetWindowSurface( window );
            display_board(board,screenSurface);
            SDL_UpdateWindowSurface( window );
            if(pause > 1)
            {
                pause--;
            }
        }



        while(SDL_PollEvent(&e)!=0)
        {
            if(e.window.event== SDL_WINDOWEVENT_CLOSE)
            {
                printf("bye!");
                //Destroy window
                SDL_DestroyWindow( window );
                //Quit SDL subsystems
                SDL_Quit();
                done++;
            }
            if(e.type == SDL_KEYDOWN)
            {
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
                    init_board(board,10000);
                }
                if(e.key.keysym.sym == SDLK_a)
                {
                    add_cells(board,100);
                }
                if(e.key.keysym.sym == SDLK_ESCAPE)
                {
                    printf("bye!");
                    //Destroy window
                    SDL_DestroyWindow( window );
                    //Quit SDL subsystems
                    SDL_Quit();
                    done++;
                }
                if(e.key.keysym.sym == SDLK_q)
                {
                    printf("bye!");
                    //Destroy window
                    SDL_DestroyWindow( window );
                    //Quit SDL subsystems
                    SDL_Quit();
                    done++;
                }
                if(e.key.keysym.sym == SDLK_k)
                {
                    chance_kill(board);
                }
                if(e.key.keysym.sym == SDLK_SPACE)
                {
                    if(pause == 1)
                    {
                        pause++;
                    }
                }
            }

        }
    }





}
