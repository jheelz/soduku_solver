
def read_euluer_sodukus(filepath):

    def reader(filepath):
        f = open(filepath, 'r')
        raw_file = f.read()

        file_split = raw_file.split('\n')
        return file_split

    def string_parse(x):
        string = ''
        for char in x:
            string += char + ','
        return string[:-1]

    file = reader(filepath)

    sodukus = []
    for i in range(0, len(file) + 1, 10):
        sodukus.append(file[i : i + 10])

    #chop off last empty list
    sodukus = sodukus[:-1]

    #chop off first entry of every list; corresponds to Grid1,...,Grid50
    numbers_of_sodukus = len(sodukus)
    for i in range(0, numbers_of_sodukus, 1):
        sodukus[i] = sodukus[i][1:]

    numpy_friendly_soduku = []

    for soduku in sodukus:
        soduku_lines = []
        for line in soduku:

            line_as_string = string_parse(line)
            print line_as_string
            line_as_nums = [int(x) for x in line_as_string.split(',')]

            soduku_lines.append(line_as_nums)
        numpy_friendly_soduku.append(soduku_lines)
    return numpy_friendly_soduku

print read_euluer_sodukus('/Users/james_healy/soduku_solver/soduku_puzzles.txt')
