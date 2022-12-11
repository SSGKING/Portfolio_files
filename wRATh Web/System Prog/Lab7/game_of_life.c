//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 7 game_of_life.c
#define BOARD_HEIGHT 100
#define BOARD_WIDTH 200
#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
inline void init_board(int board[BOARD_HEIGHT][BOARD_WIDTH],int num_alive)
{
    int x;
    int y;
    for (x = 0; x < BOARD_HEIGHT; x++)
    {
        for (y = 0; y < BOARD_WIDTH; y++)
        {

            board[x][y] = 0;

        }
    }

    int i = 0;
    srand(time(NULL));
    while(num_alive > 0)
    {


        int randX = rand()%BOARD_HEIGHT;
        int randY = rand()%BOARD_WIDTH;

        if (board[randX][randY] == 0)
        {

            i++;
            board[randX][randY] = 1;
            num_alive--;
        }

    }



    /*
    for (i = 0; i < BOARD_HEIGHT; i++)
    {
        for (j = 0; j < BOARD_WIDTH; j++)
        {
            if (num_alive > 0)
            {
                board[i][j] = 1;
                num_alive --;
            }
            else
            {
                board[i][j] = 0;
            }
        }
    }
    */
}
inline void add_cells(int board[BOARD_HEIGHT][BOARD_WIDTH],int num_alive)
{
    srand(time(NULL));
    while(num_alive > 0)
    {


        int randX = rand()%BOARD_HEIGHT;
        int randY = rand()%BOARD_WIDTH;

        if (board[randX][randY] == 0)
        {


            board[randX][randY] = 1;
            num_alive--;
        }

    }

}
inline void display_board(int board[BOARD_HEIGHT][BOARD_WIDTH],SDL_Surface* screen)
{
    int i;
    int j;
    SDL_Rect rectangle_list[BOARD_HEIGHT][BOARD_WIDTH];

    for (i = 0; i < BOARD_HEIGHT; i++)
    {
        for (j = 0; j < BOARD_WIDTH; j++)
        {
            rectangle_list[i][j].x = ((j*5)+1);
            rectangle_list[i][j].y = ((i*5)+1);
            rectangle_list[i][j].w = 4;
            rectangle_list[i][j].h = 4;

            SDL_FillRect(screen,&rectangle_list[i][j],SDL_MapRGB( screen->format, 255*board[i][j], 0*board[i][j], 255*board[i][j] ));
        }

    }
}
inline int num_neighbors(int board[BOARD_HEIGHT][BOARD_WIDTH],int x,int y)
{
    int neighbors =0;
    int i,j;


    for(i = -1;i < 2;i++)
    {
        for (j = -1;j < 2;j++)
        {

            if (((x+i) == x) &&((y+j) == y))
                neighbors = neighbors;

            else if (board[x+i][y+j] == 1)
            {
                if ((x+i) >= 0 && (x+i) < BOARD_HEIGHT)
                {
                    if ((y+j) >= 0 && (y+j) < BOARD_WIDTH)
                    {
                        neighbors ++;
                    }
                }
            }
        }
    }
    return neighbors;

}
inline int next_state(int board[BOARD_HEIGHT][BOARD_WIDTH],int x,int y)
{
    int g;
    int returns;
    g = num_neighbors(board,x,y);
    if (g < 2)
    {
        returns = 0;

        return returns;
    }
    if (g > 3)
    {
        returns = 0;

        return returns;
    }
    if (g == 3)
    {
        returns = 1;

        return returns;
    }
    if(g == 2 && board[x][y] == 1)
    {
        returns = 1;

        return returns;
    }
    if(g == 2 && board[x][y] == 0)
    {
        returns = 0;

        return returns;
    }

}
inline void chance_kill(int board[BOARD_HEIGHT][BOARD_WIDTH])
{
    srand(time(NULL));
    int x;
    int y;
    for (x = 0; x < BOARD_HEIGHT; x++)
    {
        for (y = 0; y < BOARD_WIDTH; y++)
        {
            int percent = rand()%10;

            if(board[x][y] != 0)
            {
                if(percent == 1)
                {
                    board[x][y] = 0;
                }
            }

        }
    }

}
inline void next_generation(int board[BOARD_HEIGHT][BOARD_WIDTH])
{
    int copy[BOARD_HEIGHT][BOARD_WIDTH];
    int next = 0;

    memcpy(copy,board,(sizeof(int)*BOARD_HEIGHT*BOARD_WIDTH));

    for (int i = 0; i < BOARD_HEIGHT; i++)
    {

        for (int j = 0; j < BOARD_WIDTH; j++)
        {

            copy[i][j] = next_state(board,i,j);

        }
        printf("\n");

    }
     memcpy(board,copy,(sizeof(int)*BOARD_HEIGHT*BOARD_WIDTH));


}
