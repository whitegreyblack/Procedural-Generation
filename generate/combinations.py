class Sequences:
    '''Includes two static methods: types and sequences
    Types: 
        uses sequence.keys

    Sequences: 
        uses sequence sets if given a proper
        sequence key
    '''
    HORIZONTAL, VERTICAL, DIAGONAL, LATERAL, ALL = range(5)

    @staticmethod
    def types():
        '''Returns all sequence key types'''
        return (Sequences.HORIZONTAL,
            Sequences.VERTICAL,
            Sequences.DIAGONAL,
            Sequences.LATERAL,
            Sequences.ALL)

    @staticmethod
    def sequences(sequence, inclusive=False):
        '''Returns a sequence set given a sequence key'''
        if sequence not in Sequences.types():
            raise ValueError("Invalid sequence")

        steps = set()
        if sequence == Sequences.HORIZONTAL:
            for i in range(-1, 2, 2):
                steps.add((i, 0))

        elif sequence == Sequences.VERTICAL:
            for j in range(-1, 2, 2):
                steps.add((0, j))

        elif sequence == Sequences.DIAGONAL:
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    steps.add((i, j))

        elif sequence == Sequences.LATERAL:
            for i in range(-1, 2, 2):
                steps.add((0, i))
                steps.add((i, 0))

        elif sequence == Sequences.ALL:
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if (i, j) != (0, 0):
                        steps.add((i, j))

        if inclusive:
            steps.add((0, 0))
            
        return steps

if __name__ == "__main__":
    print(__file__)
    c = Sequences()