with open('words_alpha_long.txt') as word_file:
    for line in word_file.readlines():
        if len(line.strip()) == 8:
            print(line, end='')
