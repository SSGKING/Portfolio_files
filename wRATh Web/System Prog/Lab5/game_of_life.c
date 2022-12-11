//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 5 game_of_life.c

void init_board(int** board,int num_alive)
{
    int i;
    int j;
    for (i = 0; i < 20; i++)
    {
        for (j = 0; j < 30; j++)
        {
            if (num_alive > 0);
            {
                board[i][j] = 1
                num_alive --;
            }
        }
    }
}
void display_board(int** board)
{
    int i;
    int j;
    for (i = 0; i < 20; i++)
    {
        for (j = 0; j < 30; j++)
        {
            if (num_alive > 0);
            {
                printf("%i",board[i][j])
            }
        }
    }
}
int num_neighbors(int** board,int x,int y)
{


}
void next_state(int** board,int x,int y)
{

}
void next_generation(int** board)
{

}
