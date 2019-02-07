

def num2alphabet(number):
    '''This function converts a number into its corresponding alphabetic letter. Meaning 1 gives a A while 2 gives a B.
    Since i use it to acces the excel collumns I convert the numbers to uppercase chars. When a number is higher than 26
    the remainder gets appended to the A such that 27 gives AA.'''

    ### Translate number to letter ###
    if number <= 26: # If number is lower or equal to 26 translate to alphabetic letter
        letter_code = chr(number + 64)
        return letter_code
    else:   # If number is higher than 26 append the remainder as a alphabetic letter. Example: AB
        n, r = divmod(number, 26)
        letter_code = "".join(n*[chr(1+64)]+[chr(r+64)])

    ### Return alphabet char ###
    return letter_code

alpha_bet = num2alphabet(270)
print(alpha_bet)