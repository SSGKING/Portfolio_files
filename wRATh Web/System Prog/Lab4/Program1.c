//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 4 Program 1

#include <string.h>
void convertToLeetSpeak( char * text );

int main()
{

    //code to allow the input of a message string.
    //call the convertToLeetSpeak function to modify the string.
    //print out the converted message string.

    char text[100];
    char *ptr;
    printf("Please enter the string to be converted \n");
    scanf("%99[^\n]s",text);
    printf("Entered %s\n",text);
    ptr = text;
    convertToLeetSpeak(ptr);
    printf("Leetspeek version %s\n",text);



}
void convertToLeetSpeak( char * text )
{
    // code to convert the string as described above.


    while(*text != '\0')
    {
        if (*text == 'a')
        {
            *text = '@';
        }
        if (*text == 'A')
        {
            *text = '4';
        }
        if (*text == 's')
        {
            *text = '5';
        }
        if (*text == 'S')
        {
            *text = '$';
        }
        if (*text == 'e' || *text=='E')
        {
            *text = '3';
        }
        if (*text == 'l'|| *text=='L')
        {
            *text = '1';
        }
        if (*text == 'o'|| *text=='O')
        {
            *text = '0';
        }
        if (*text == 'b')
        {
            *text = '6';
        }
        if (*text == 'B')
        {
            *text = '8';
        }
        if (*text == 'z'|| *text=='Z')
        {
            *text = '2';
        }
        if (*text == 't'|| *text=='T')
        {
            *text = '7';
        }
        text++;
    }

}
