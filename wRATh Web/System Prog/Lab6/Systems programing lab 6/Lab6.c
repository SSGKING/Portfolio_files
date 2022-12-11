//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 6



// Simple SDL2 program
#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
//Screen dimension constants
int SCREEN_WIDTH = 800;
int SCREEN_HEIGHT = 600;
int main(int argc, char *argv[])
{
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
            SDL_MapRGB( screenSurface->format, red, green, blue ) );
            //Update the surface
            SDL_UpdateWindowSurface( window );
            //Wait five seconds
            SDL_Delay( 5000 );
        }
    }
    int looping = 0;
    SDL_Event e;

    while(looping == 0)
    {
        //main loop


        while(SDL_PollEvent(&e)!=0)
        {
            srand(time(NULL));

            if(e.type == SDL_WINDOWEVENT)
            {
                if(e.window.event== SDL_WINDOWEVENT_CLOSE)
                {
                    printf("bye!");
                    //Destroy window
                    SDL_DestroyWindow( window );
                    //Quit SDL subsystems
                    SDL_Quit();
                    looping++;
                }

            }
            if(e.type == SDL_KEYDOWN)
            {
                if(e.key.keysym.sym == SDLK_ESCAPE)
                {
                    printf("bye!");
                    //Destroy window
                    SDL_DestroyWindow( window );
                    //Quit SDL subsystems
                    SDL_Quit();
                    looping++;
                }
                if(e.key.keysym.sym == SDLK_r)
                {

                    red = rand()%256;
                    blue = rand()%256;
                    green = rand()%256;
                    SDL_FillRect( screenSurface, NULL,SDL_MapRGB( screenSurface->format, red, green, blue ) );
                    SDL_UpdateWindowSurface( window );
                }
            }
        }
    }





}
