# Dashiell Coyier HW D04
# Starter code from Carleton College CS 254 w26, taught by Josh Davis

import re


# This function comes from our tutorial PDF.
def matches(regexp, string):
    return re.search(r"\A(?:" + regexp + r")\Z", string) != None
    # return re.search(r"(?:" + regexp + r")", string) != None


# Let's agree that a word is said to be mis-capitalized if it consists of two or
# more letters and any letter after the first one is upper-case. We assume that
# only alphabetical characters appear in words. This Python regular expression
# is supposed to match exactly mis-capitalized words.
miscapitalized = r"[A-Za-z][a-z]*[A-Z]+[A-Za-z]*"

# An e-mail address such as 'superSnake@carleton.edu' consists of a local part,
# 'superSnake', and a hostname, 'carleton.edu'. The local part is a string made
# of one or more characters from this set: upper- and lower-case English
# letters, the digits '0' through '9', the characters '!', '#', '$', '%', '&',
# ''', '*', '+', '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~', and the
# period '.'. The hostname is a string made of one or more characters from this
# set: lower-case English letters, the digits '0' through '9', the period '.',
# and the hyphen '-'. Neither the local part nor the hostname can begin or end
# in a period. The local part and the hostname are separated by a single '@'.
# (There are a few more rules to real e-mail addresses, but this is good enough
# for our purposes.) Here are four relevant character classes.
localwo = r"[\w!#\$%&'\*\+\-/=\?\^_`\{\|\}~]"
localw = r"[\w!#\$%&'\*\+\-/=\?\^_`\{\|\}~\.]"
hostwo = r"[a-z0-9-]"
hostw = r"[a-z0-9\-\.]"

# Here is a regular expression that matches e-mail addresses as just described.
email = r"[\w!#\$%&'\*\+\-/=\?\^_`\{\|\}~][\w!#\$%&'\*\+\-/=\?\^_`\{\|\}~\.]*[\w!#\$%&'\*\+\-/=\?\^_`\{\|\}~]\@[a-z0-9-][a-z0-9\-\.]*[a-z0-9-]"


# I like to write my dates in the format yyyy/mm/dd, but sometimes I
# accidentally write mm/dd/yyyy because that's how I was raised. The following
# Python function takes a string as input, uses a regular expression to fix
# all dates in the string to my liking, and returns the fixed string. All
# years are four-digit --- I'm Y2K-compliant --- but months and days can be
# one- or two-digit. (Hint: You need to use substitutions and multiple groups.
# My solution is one line of code.)
def fixDates(string):
    fixed_string = string
    for date in re.findall(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}", fixed_string):
        fixed_string = re.sub(
            date,
            re.split(r"/", date)[2]
            + "/"
            + re.split(r"/", date)[0].zfill(2)
            + "/"
            + re.split(r"/", date)[1].zfill(2),
            fixed_string,
        )
    return fixed_string


# Runs tests. (Feel free to add more test cases.)
def main():
    print("First test: mis-capitalized words...")
    student = re.findall(miscapitalized, "This is okay tHis IS nOT.")
    jrd = ["tHis", "IS", "nOT"]
    print(student == jrd)
    teacher = re.findall(
        miscapitalized,
        "test Test tEst teSt tesT TEst teST tESt TesT TESt tEST TEsT TeST TEST",
    )
    print(teacher)
    print("Second test: valid e-mail addresses...")
    print(matches(email, "superSnake@carleton.edu"))
    print(matches(email, "-babatope-44017@cheese"))
    print(matches(email, "superSnake@carleton.edu"))
    print("Third test: invalid e-mail addresses...")
    print(matches(email, "josh@.edu"))
    print(matches(email, "nerd@stolaf@edu"))
    print(matches(email, "josh@a.edu."))
    print(matches(email, "test@@@.edu"))
    print("Fourth test: fixing dates...")
    print(fixDates("Why did I pick the dates 4/17/2009, 11/9/2007?"))
    print(
        "Why did I pick the dates 2009/04/17, 2007/11/09?"
        == fixDates("Why did I pick the dates 4/17/2009, 11/9/2007?")
    )


# If the user imported this file as a module into another program, then don't
# run main(). If the user ran this file directly, then do run main().
if __name__ == "__main__":
    main()
