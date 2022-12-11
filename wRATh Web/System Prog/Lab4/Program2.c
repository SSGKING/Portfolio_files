//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 4 Program 2
#include <string.h>

void crypt( char * message, int length, char * key);

int main( )
{
    //code to allow input of message string.
    char mes[100];
    char *ptr;
    printf("Please enter the message \n");
    scanf("%99[^\n]s",mes);
    ptr = mes;
    //code to allow input of key string.
    char key[100];
    char *ptr2;
    printf("Please enter the key to encrypt \n");
    scanf(" %99[^\n]s",key);
    ptr2 = key;
    //code to encrypt message.
    crypt(ptr,strlen(mes),ptr2);
    //code to display encrypted message.
    printf("Message is: %s\n",mes);
    //code to decrypt message.
    crypt(ptr,strlen(mes),ptr2);
    //code to display decrypted message.
    printf("Message is: %s\n",mes);
}
void crypt( char * message, int length, char * key)
{
    // code to encrypt the message using XOR with the key string.
    int i;
    int j = 0;
    int max = strlen(key);
    printf("%i\n",length);
    for(i=0;i<length;i++)
    {
        message[i] = message[i] ^ (key[j]^255);
        j++;
        if (j>=max)
        {
            j = j - max;
        }
    }
}
