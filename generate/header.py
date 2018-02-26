# header.py

def lpath(b1, b2):
    # x1, y1 = center(b1)
    # x2, y2 = center(b2)
    x1, y1 = b1
    x2, y2 = b2

    # check if xs are on the same axis -- returns a vertical line
    if x1 == x2 or y1 == y2:
        return line((x1, y1), (x2, y2))

    # # check if points are within x bounds of each other == returns the midpoint vertical line
    # elif b2.x1 <= x1 < b2.x2 and b1.x1 <= x2 < b1.x2:
    #     x = (x1+x2)//2
    #     return line((x, y1), (x, y2))

    # # check if points are within y bounds of each other -- returns the midpoint horizontal line
    # elif b2.y1 <= y1 < b2.x2 and b1.y1 <= y2 < b2.y2:
    #     y = (y1+y2)//2
    #     return line((x1, y), (x2, y))

    else:
        # we check the slope value between two boxes to plan the path
        slope = abs((max(y1, y2) - min(y1, y2))/((max(x1, x2) - min(x1, x2)))) <= 1.0
    
        # low slope -- go horizontal
        if slope:
            # width is short enough - make else zpath
            return line((x1, y1), (x1, y2)) \
                + line((x1, y2), (x2, y2))

        # high slope -- go vertical
        else:
            return line((x1, y1), (x2, y1)) + line((x2, y1), (x2, y2))

def line(start, end):
    """Bresenham's Line Algo -- returns list of tuples from start and end"""

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)

        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()

    return points

def constructor(width, height=None, depth=None, value=None, args=None):
    '''Returns either a 1D, 2D or 3D array depending on height parameter
    and assigns each value in the array a value passed in as a parameter.
    The value can also take in arguments passed in as a parameter which 
    it uses to create the final value in the array
    '''
    def determine():
        '''Helper function for constructor that allows constructor to 
        calculate the final value that will be returned and placed in 
        the array
        '''
        ret = 0
        if callable(value):
            if callable(args):
                ret = value(args())
            elif args:
                ret = value(*args)
            else:
                ret = value()
        elif value:
            ret = value
        return ret

    if not width:
        raise ValueError('Width must be specified')

    if not height and depth:
        # cannot have height but have depth -- just switch it in that case
        height, depth = depth, height

    array = None
    dimensions = sum(map(lambda x: 1 if x else 0, (width, height, depth)))
    
    for _ in range(dimensions):
        # first dimension check -- create the array
        # all other checks should append to the array
        if not array:
            array = [determine() for _ in range(width)]
        elif isinstance(array[0], int) or isinstance(array[0], float):
            array = [array for _ in range(height)]
        else:
            array = [array for _ in range(depth)]

    return array

def setup(x, y, cx=8, cy=8):
    '''BLT terminal initialization and setup'''
    terminal.open()
    terminal.set(f'window: size={x}x{y}, cellsize={cx}x{cy}')
    terminal.refresh()

def key_handle_exit(key):
    '''Key check to detect and handle exitting of blt terminal'''
    if key in (terminal.TK_Q, terminal.TK_ESCAPE, terminal.TK_CLOSE):
        return True

def term_loop(m):
    output_flag = False
    while True:
        terminal.clear()
        for x, y, ch, col in list(m.output_terminal(output_flag)):
            terminal.puts(x, y, '[c={}]{}[/c]'.format(col, ch))
        terminal.refresh()

        key = terminal.read()
        if key_handle_exit(key):
            break

        elif key == terminal.TK_S:
            m.smooth()
            m.normalize()
            m.evaluate()

        elif key == terminal.TK_F:
            output_flag = not output_flag