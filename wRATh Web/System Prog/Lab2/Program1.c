//name: Alex Neill
//class ETEC 2110.01
//assignment: Lab 2



#include<stdio.h>

int collatz_length(long long int number)
{
    long long int times = 1;
    while(number !=1)
    {
        if (number%2 == 0)
        {
            number = number / 2;
            times++;
        }
        else
        {
            number = (number*3);
            number++;
            times++;
        }
    }
    return times;
}

void collatz_print_sequence(long long int number)
{
    printf("%d:",number);

    while(number !=1)
    {
        printf("%d,",number);
        if (number%2 == 0)
        {
            number = number / 2;
        }
        else
        {
            number = (number*3);
            number++;
        }
    }
    printf("%d",number);
}

main()
{
    long long int i = 1;
    int longest = 1;
    while(i<= 1000000)
    {
        if (collatz_length(i)> collatz_length(longest))
        {

            longest = i;
        }
        i++;
    }
    printf("%d \n",collatz_length(longest));
    collatz_print_sequence(longest);
}

