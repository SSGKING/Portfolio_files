#name: Alex Neill
#class ETEC 2110.01
#assignment: Lab 2

import time

def collatz_length(number):
    times = 1
    while(number !=1):
        if (number%2 == 0):
            number = number / 2
            times+=1
        else:
            number = (number*3)
            number+=1
            times+=1
    return times

def collatz_print_sequence(number):

    print(str(number)+":")

    while(number !=1):
    
        print(str(number)+",")
        if (number%2 == 0):
        
            number = number / 2
        
        else:
        
            number = (number*3)
            number += 1
        
    
    print(str(number))

start_time = time.time()
i = 1
longest = 1
while(i<= 1000000):
    

    if (collatz_length(i)> collatz_length(longest)):
        longest = i
    i+= 1
end_time = time.time()
total_time = end_time-start_time


print(str(collatz_length(longest)))
collatz_print_sequence(longest)
print(str(total_time)+" Seconds")