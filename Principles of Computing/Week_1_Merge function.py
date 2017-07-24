"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #input list must not be changed
    line = list(line)
    results = len(line)
    
    # Slide tiles to the front
    while 0 in line:
        line.remove(0)
    
    for tile in range(len(line) - 1):
        if line[tile] == line[tile + 1]:
            line[tile] *= 2
            del line[tile + 1]
            line.insert(tile + 1, 0)
        # find the end of "line"
        if tile + 2 > len(line):
            break
    # fill "line" up with zeros and slide to front
    while 0 in line:
        line.remove(0)
    while len(line) != results:
        line.append(0)
    
    
    return line

#print merge([2, 0, 2, 4])
#print merge([0, 0, 2, 2])
#print merge([2, 2, 0, 0])
#print merge([2, 2, 2, 2])
#print merge([4, 4, 4, 4])
#print merge([8, 16, 16, 8])
#print merge([0, 0, 0, 0])