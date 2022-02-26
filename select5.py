with open('words_alpha_long.txt') as word_file:
    for line in word_file.readlines():
        if len(line.strip()) == 5:
            print(line, end='')
