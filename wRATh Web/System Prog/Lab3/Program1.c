//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 3



void printTable(unsigned char startChar, unsigned char endChar)
{
    // code to print a table of the specified characters as follows:
    // decimal representation, the character representation, and the 8-bit binary
    // representation. Call the printBinary function to print the
    // binary representation. Call the printHex function to print the hexadecimal
    // representation.
    printf("Table A to Z:\n");
    printf("num  ch  bin      hex\n");
    while (startChar<=endChar)
    {
        printf("%d   ",startChar);
        printf("%c   ", startChar);
        printBinary(startChar);
        printf(" ");
        printHex(startChar);

        startChar++;
        printf("\n");

    }

}
void printBinary(unsigned char ch)
{
    // code to print out the specified character in binary.
    unsigned char mask = 128;

    while (mask>0)
    {
        if((ch&mask)==0)
        {
            printf("0");
        }
        else
        {
            printf("1");
        }
        mask = mask >> 1 ;
    }



}
void printHex(unsigned char ch)
{
    // code to print out the specified character in hexadecimal.
    printf("%X",ch);



}
int main( )
{
    //code to call the print table function to print out a table of the
    //characters form 'A' to 'Z'

    unsigned char letter = 'A';
    unsigned char endLetter = 'Z';

    printTable(letter,endLetter);



}
