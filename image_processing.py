# Author: Jake Fogel - ID: 261085935

ERROR_MESSAGE = "Input not in valid regular PGM format!"
C_ERROR_MESSAGE = "Input not in valid compressed PGM format!"
B_ERROR_MESSAGE = "Input not in valid compressed or regular PGM format!"


def valid_number(int):
    """(int) -> bool
    Takes an integer (int) as input and tests if it is a valid pgm
    darkness value

    >>> valid_number(2)
    True
    >>> valid_number(-18)
    False
    >>> valid_number(2000)
    False
    """
    return int >= 0 and int <= 255

def is_valid_image(lists):
    """(list<list<int>>) -> bool 
    Takes a pgm matrix (lists) and confirms it
    is a valid pgm matrix

    >>> is_valid_image([[2],[2],[2]])
    True
    >>> is_valid_image([[22,22,33],[244,33,22],[22,22,22],[1,2,3]])
    True
    >>> is_valid_image([[2],[2,2],['hi',3]])
    False
    """

    #Check immediately for 0 length
    if len(lists) == 0:
        return False

    for list in lists:
        if len(list) == 0:
            return False

    if len(lists) != 1:
        list_len = len(lists[0])
        for list in lists:
            if len(list) != list_len:
                return False

    for list in lists:
        for data in list:
            if type(data) != int:
                return False
            if not valid_number(data):
                return False
    return True


def get_compressed_length(list):
    """(list<str>) -> int
    Takes a list of compressed pgm values (list) and returns the
    total length of the list when decompressed

    >>> get_compressed_length(['22x4','22x8'])
    12
    >>> get_compressed_length(['83x2','39x3', '22x1'])
    6
    >>> get_compressed_length(['2x4','45x8', '29x9'])
    21
    """

    list_len = 0
    for data in list:
        x_local = str(data).find('x')
        after_x = str(data)[x_local + 1:]
        list_len += int(after_x)
    return list_len



def is_valid_compressed_image(lists):
    """(list<list<str>>) -> bool
    Takes a compressed pgm matrix (lists) and
    confirms it is a valid compressed pgm matrix

    >>> is_valid_compressed_image([['22x4','22x8'],['23x6','28x6'],['22x11','240x1'],['1x2','1x10']])
    True
    >>> is_valid_compressed_image([['2x4','45x8', '29x9'], ['23x21'], ['1x21']])
    True
    >>> is_valid_compressed_image([['mi'],['fa'],['so']])
    False
    """

    # Check immediately for 0 length
    if len(lists) == 0:
        return False

    for list in lists:
        if len(list) == 0:
            return False

    for list_i in range(len(lists)): #Check Each Row

        for data in lists[list_i]: #Check Each Compressed Data
            if str(data) != data:
                return False

            x_local = data.find('x')
            before_x = data[:x_local]
            after_x = data[x_local + 1:]

            # Confirm darkness value is an integer
            if not (before_x.isdecimal()):
                return False
            
            if not (after_x.isdecimal()):
                return False

            pgm_value = int(before_x)

            if 'x' not in data or not valid_number(pgm_value):
                return False

        if (list_i == 0):
            list_len = get_compressed_length(lists[0])

        if get_compressed_length(lists[list_i]) != list_len:
                return False

    return True

def load_regular_image(file_name):
    """(str) -> list<list> 
    Takes a string representing a pgm file name and loads the
    pgm file data into a 2D list

    >>> load_regular_image('comp.pgm')
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> save_image([[22, 22, 33], [244, 33, 22], [22, 22, 22], [1, 2, 3]], 'test0.pgm')
    >>> load_regular_image('test0.pgm')
    [[22, 22, 33], [244, 33, 22], [22, 22, 22], [1, 2, 3]]
    >>> save_image([['2x4'],['12x3', '1x1'],['23x4']], 'test1.pgm')
    >>> load_regular_image('test1.pgm')
    AssertionError: Input not in valid regular PGM format!
    """

    matrix = []
    file = open(file_name, "r")

    for line in file:
        matrix.append(line.split())

    file.close()

    # Check information of line 1 and 3 of the file
    if matrix[0] != ['P2'] or matrix[2] != ['255']:
         raise AssertionError(ERROR_MESSAGE)

    # Get the row column information on line 2 of the file
    row_col = []
    row_col.append(matrix[1][0])
    row_col.append(matrix[1][1])

    matrix = matrix[3:]

    for row in range(len(matrix)):
        for data in range(len(matrix[row])):
            value = matrix[row][data]
            if not value.isdecimal():
                raise AssertionError(ERROR_MESSAGE)
            matrix[row][data] = int(value)

    if not is_valid_image(matrix):
        raise AssertionError(ERROR_MESSAGE)

    if row_col[0] != str(len(matrix[0])) or row_col[1] != str(len(matrix)):
        raise AssertionError(ERROR_MESSAGE)

    return matrix


def load_compressed_image(file_name):
    """(str) -> <list<list<str>>>
    Takes a string representing a compressed pgm file name
    and loads the compressed pgm file data into a 2D list
    
    >>> save_image([['22x4','22x8'],['23x6','28x6'],['22x11','240x1'],['1x2','1x10']], 'test2.pgm.compressed')
    >>> load_compressed_image('test2.pgm.compressed')
    [['22x4', '22x8'], ['23x6', '28x6'], ['22x11', '240x1'], ['1x2', '1x10']]
    >>> save_image([['2x4','45x8', '29x9'], ['23x21'], ['1x21']], 'test3.pgm.compressed')
    >>> load_compressed_image('test3.pgm.compressed')
    [['2x4', '45x8', '29x9'], ['23x21'], ['1x21']]
    >>> save_image([[0, 0],[2, 202],[2, 3]], 'test4.pgm.compressed')
    >>> load_compressed_image('test4.pgm.compressed')
    AssertionError: Input not in valid compressed PGM format!
    """

    matrix = []
    file = open(file_name, "r")

    for line in file:
        matrix.append(line.split()) 

    file.close()

    # Check information of line 1 and 3 of the file
    if matrix[0] != ['P2C'] or matrix[2] != ['255']:
         raise AssertionError(C_ERROR_MESSAGE)
    
    # Get the row column information on line 2 of the file
    row_col = []
    row_col.append(matrix[1][0])
    row_col.append(matrix[1][1])

    matrix = matrix[3:]
    
    if not is_valid_compressed_image(matrix):
        raise AssertionError(C_ERROR_MESSAGE)

    if row_col[0] != str(get_compressed_length(matrix[0])) or row_col[1] != str(len(matrix)):
        raise AssertionError(C_ERROR_MESSAGE)

    return matrix


def load_image(file_name):
    """(str) -> <list<list<str>>> | <list<list<int>>>
    Takes a string representing a pgm or compressed pgm 
    file name (file_name) and loads the file data into a 
    2D list

    >>> save_image([['88x5','20x8', '29x9'], ['23x22'], ['1x22']], 'test5.pgm.compressed')
    >>> load_image('test5.pgm.compressed')
    [['88x5', '20x8', '29x9'], ['23x22'], ['1x22']]
    >>> save_image([[22,22,33],[244,33,22],[22,22,22],[1,2,3]], 'test6.pgm')
    >>> load_image('test6.pgm')
    [[22, 22, 33], [244, 33, 22], [22, 22, 22], [1, 2, 3]]
    >>> file = open('test7.pgm', 'w')
    >>> file.write('P4C')
    3
    >>> load_image('test7.pgm')
    AssertionError: Input not in valid compressed or regular PGM format!
    """

    file = open(file_name, "r")
    file_read = file.read()
    if file_read[0:3] == 'P2C':
        return load_compressed_image(file_name)
    elif file_read[0:2] == 'P2':
        return load_regular_image(file_name)
    else:
        raise AssertionError(B_ERROR_MESSAGE)

def save_regular_image(lists, file_name):
    """(list<list<int>>, str) -> NoneType
    Writes a file with name file_name in which the pgm
    matrix (lists) is stored

    >>> save_regular_image([[22,22,33],[244,33,22],[22,22,22],[1,2,3]], 'test8.pgm')
    >>> file = open('test8.pgm', 'r')
    >>> file.read()
    'P2\\n3 4\\n255\\n22 22 33\\n244 33 22\\n22 22 22\\n1 2 3\\n'
    >>> save_regular_image([[44,22,22,33],[44,244,33,22],[44,22,22,22],[44,1,2,3]], 'test9.pgm')
    >>> file = open('test9.pgm', 'r')
    >>> file.read()
    'P2\\n4 4\\n255\\n44 22 22 33\\n44 244 33 22\\n44 22 22 22\\n44 1 2 3\\n'
    >>> save_regular_image([[1],['a'],['2']], 'invalid.pgm')
    AssertionError: Input not in valid regular PGM format!
    """

    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)
    
    output = ''


    output += 'P2\n'
    output += str(len(lists[0])) + ' ' + str(len(lists)) + '\n'
    output += '255\n'
    for list in lists:
        for data_i in range(len(list)):
            output += str(list[data_i])

            if data_i + 1 < len(list):
                output += ' '

        output += '\n'

    file = open(file_name, 'w')
    file.write(output)
    file.close()


def save_compressed_image(lists, file_name):
    """(list<list<str>>, str) -> NoneType
    Writes a file with name file_name in which the 
    compressed pgm matrix (lists) is stored

    >>> save_compressed_image([['22x2','33x1'],['244x1','33x1','22x1'],['22x3'],['1x1','2x1','3x1']], 'test11.pgm.compressed')
    >>> file = open('test11.pgm.compressed', 'r')
    >>> file.read()
    'P2C\\n3 4\\n255\\n22x2 33x1\\n244x1 33x1 22x1\\n22x3\\n1x1 2x1 3x1\\n'
    >>> save_compressed_image([['44x1','22x2','33x1'],['44x1','244x1','33x1','22x1']], 'test12.pgm.compressed')
    >>> file = open('test12.pgm.compressed', 'r')
    >>> file.read()
    'P2C\\n4 2\\n255\\n44x1 22x2 33x1\\n44x1 244x1 33x1 22x1\\n'
    >>> save_compressed_image([[1],['a'],['2']], 'invalid.pgm')
    AssertionError: Input not in valid compressed PGM format!
    """

    if not is_valid_compressed_image(lists):
        raise AssertionError(C_ERROR_MESSAGE)
    
    output = ''


    output += 'P2C\n'
    output += str(get_compressed_length(lists[0]))+' '+str(len(lists))+'\n'
    output += '255\n'
    for list in lists:
        for data_i in range(len(list)):
            output += list[data_i]

            if data_i + 1 < len(list):
                output += ' '

        output += '\n'

    file = open(file_name, 'w')
    file.write(output)
    file.close()


def save_image(lists, file_name):
    """(list<list<int>> | list<list<str>>) -> NoneType
    Writes a file with name file_name in which the 
    compressed pgm matrix (lists) is stored

    >>> save_image([['43x1','23x2','33x1'],['43x1','243x1','33x1','23x1']], 'test13.pgm.compressed')
    >>> file = open('test13.pgm.compressed', 'r')
    >>> file.read()
    'P2C\\n4 2\\n255\\n43x1 23x2 33x1\\n43x1 243x1 33x1 23x1\\n'
    >>> save_image([[43,23,23,33],[43,243,33,23],[43,23,23,23],[43,1,2,3]], 'test14.pgm')
    >>> file = open('test14.pgm', 'r')
    >>> file.read()
    'P2\\n4 4\\n255\\n43 23 23 33\\n43 243 33 23\\n43 23 23 23\\n43 1 2 3\\n'
    >>> save_image([[12],[12],['a']], 'test15.pgm')
    AssertionError: Input not in valid compressed or regular PGM format!
    """

    if type(lists[0][0]) == str:
        save_compressed_image(lists, file_name)
    elif type(lists[0][0]) == int:
        save_regular_image(lists, file_name)
    else:
        raise AssertionError(B_ERROR_MESSAGE)

def invert(lists):
    """(list<list<int>>) -> list<list<int>>
    Takes a pgm matrix (lists) and inverts the colour
    value of each pixel

    >>> image = [[0, 100, 150], [200, 200, 200], [255, 255, 255]] 
    >>> invert(image)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    >>> image = [[0]]
    >>> invert(image)
    [[255]]
    >>> image = [['hi'], ['hi']]
    >>> invert(image)
    AssertionError: Input not in valid regular PGM format!
    """


    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)

    inverted = []
    for list in lists:
        new_list = []

        for data in list:
            new_list.append(255 - data)
        inverted.append(new_list)

    return inverted

def flip_horizontal(lists):
    """(list<list<int>>) -> list<list<int>>
    Takes a pgm matrix (lists) and flips it horizontally

    >>> image = [[0, 100, 150], [200, 200, 200], [256, 255, 255]] 
    >>> flip_horizontal(image)
    [[150, 100, 0], [200, 200, 200], [255, 255, 256]]
    >>> image = [[0, 1], [2, 3]]
    >>> flip_horizontal(image)
    [[1, 0], [3, 2]]
    >>> image = [['hi'], ['hi']]
    >>> flip_horizontal(image)
    AssertionError: Input not in valid regular PGM format!
    """

    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)

    fliph = []
    for list in lists:
        fliph.append(list[::-1])

    return fliph


def flip_vertical(lists):
    """(list<list<int>>) -> list<list<int>>
    Takes a pgm matrix (lists) and flips it vertically

    >>> image = [[0, 100, 150], [200, 200, 200], [256, 255, 255]] 
    >>> flip_vertical(image)
    [[255, 255, 255], [200, 200, 200], [0, 100, 150]]
    >>> image = [[0, 1], [2, 3]]
    >>> flip_vertical(image)
    [[2, 3], [0, 1]]
    >>> image = [['h3y'], ['h3y']]
    >>> flip_vertical(image)
    AssertionError: Input not in valid regular PGM format!
    """

    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)

    flipv = lists[::-1]

    return flipv


def crop(lists, row, col, height, width):
    """(list<list<int>>, int, int, int, int) -> list<list<int>>
    Takes a pgm matrix (lists) and flips it vertically

    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2) 
    [[6, 6], [6, 7]]
    >>> crop([[1, 1, 1, 4], [1, 1, 1, 4], [1, 1, 1, 4], [1, 1, 1, 4]], 0, 0, 3, 3)
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    >>> crop([['hi'], [22]], 0, 0, 1, 1)
    AssertionError: Input not in valid regular PGM format!
    
    """

    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)
    
    #Ensure given row and column do not exceed lists
    if row + height > (len(lists)):
        raise AssertionError('Not a valid crop!')
    
    if col + width > (len(lists[0])):
        raise AssertionError('Not a valid crop!')


    crop_lists = []
    for list_i in range(row, row + height):
        crop_list = [] 
        for data_i in range(col, col + width):
            crop_list.append(lists[list_i][data_i])
        crop_lists.append(crop_list)
    
    return crop_lists


def find_end_of_repetition(list, index, target):
    """(list<int>, int, int) -> int
    Takes a row of a pgm matrix (list) and starting from an
    index (index) finds the index at which the target value
    (target) stops repeating
    
    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 2, 5)
    4
    >>> find_end_of_repetition([3, 3, 3, 3, 3, 5], 0, 3)
    4
    >>> find_end_of_repetition([2, 2, 2, 54], 1, 2)
    2
    """

    end_index = index

    for data_i in range(index + 1, len(list)):
        if list[data_i] != target:
            return end_index
        end_index += 1
    return len(list) - 1


def compress(lists):
    """(list<list<int>>) -> list<list<str>> 
    Takes a pgm matrix (lists) and returns the matrix in
    compressed form

    >>> compress([[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]])
    [['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']]
    >>> compress([[3, 3, 3], [3, 3, 3], [4, 4, 4]])
    [['3x3'], ['3x3'], ['4x3']]
    >>> compress([['hey'], ['hi']])
    AssetionError: Input not in valid regular PGM format!
    """

    if not is_valid_image(lists):
        raise AssertionError(ERROR_MESSAGE)

    compressed = []
    for list in lists:
        c_list = []
        cur_index = 0
        while cur_index < len(list):
            end_index = find_end_of_repetition(list, cur_index, list[cur_index])
            reps = end_index - cur_index + 1

            c_list.append(str(list[cur_index]) + 'x' + str(reps))

            cur_index = end_index + 1
        compressed.append(c_list)

    if not is_valid_compressed_image(compressed):
        raise AssertionError(ERROR_MESSAGE)

    return compressed



def decompress(lists):
    """(list<list<str>>) -> list<list<int>>
    Takes a compressed pgm matrix (lists) and returns the
    matrix in decompressed form

    >>> decompress([['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']])
    [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> decompress([['3x3'], ['3x3'], ['4x3']])
    [[3, 3, 3], [3, 3, 3], [4, 4, 4]]
    >>> decompress([['hey'], ['hi']])
    AssetionError: Input not in valid regular PGM format!
    """


    if not is_valid_compressed_image(lists):
        raise AssertionError(ERROR_MESSAGE)

    decompressed = []
    for list in lists:
        d_list = []
        for data in list:
            x_local = data.find('x')
            after_x = int(data[x_local + 1:])
            before_x = int(data[:x_local])

            for num in range(after_x):
                d_list.append(before_x)
        decompressed.append(d_list)

    if not is_valid_image(decompressed):
        raise AssertionError(ERROR_MESSAGE)

    return decompressed

def process_command(commands):
    """(list) -> NoneType 
    Takes a string of commands (commands) and calls the
    appropriate functions to edit the file specified
    accordingly before saving the edited file

    >>> process_command('LOAD<comp.pgm> CP SAVE<comp.pgm.compressed>')
    >>> load_compressed_image('comp.pgm.compressed')
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]
    >>> save_image([[3, 3, 3], [3, 3, 3], [4, 4, 4]], 'testfinal.pgm')
    >>> process_command('LOAD<testfinal.pgm> FV SAVE<testfinal.pgm>')
    >>> load_regular_image('testfinal.pgm')
    [[4, 4, 4], [3, 3, 3], [3, 3, 3]]
    >>> process_command('LOAD<comp.pgm> GH FJD SKDJ ALSKD SAVE<comp2.pgm>')
    AssertionError: One or more commands not in list of valid commands!
    """

    commands = commands.split()

    #Load in
    load = commands[0]
    file_name = load[load.find('<') + 1:load.find('>')]
    matrix = load_image(file_name)

    #Process Commands --> Could be done with a dictionary if we learned accessing functions from dictionaries
    for command in commands[1:-1]:
        if command == 'INV':
            matrix = invert(matrix)
        elif command == 'FH':
            matrix = flip_horizontal(matrix)
        elif command == 'FV':
            matrix = flip_vertical(matrix)
        elif 'CR' in command:
            crop_info_raw = command[command.find('<') + 1: command.find('>')]
            crop_info = crop_info_raw.split(',')
            matrix = crop(matrix, int(crop_info[0]), int(crop_info[1]), int(crop_info[2]), int(crop_info[3]))
        elif command == 'CP':
            matrix = compress(matrix)
        elif command == 'DC':
            matrix = decompress(matrix)
        else:
            raise AssertionError('One or more commands not in list of valid commands!')

    #Save it
    save = commands[-1]
    new_file_name = save[save.find('<') + 1:save.find('>')]

    save_image(matrix, new_file_name)