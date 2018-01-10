class Combinations:
    HORIZONTAL, VERTICAL, DIAGONAL, LATERAL, ALL = range(5)

    @staticmethod
    def types():
        return (Combinations.HORIZONTAL,
            Combinations.VERTICAL,
            Combinations.DIAGONAL,
            Combinations.LATERAL,
            Combinations.ALL)

    @staticmethod
    def combinations(combination, inclusive=False):
        if combination not in Combinations.types():
            raise ValueError("Invalid Combination")

        steps = set()
        if combination == Combinations.HORIZONTAL:
            for i in range(-1, 2, 2):
                steps.add((i, 0))

        elif combination == Combinations.VERTICAL:
            for j in range(-1, 2, 2):
                steps.add((0, j))

        elif combination == Combinations.DIAGONAL:
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    steps.add((i, j))

        elif combination == Combinations.LATERAL:
            for i in range(-1, 2, 2):
                steps.add((0, i))
                steps.add((i, 0))

        elif combination == Combinations.ALL:
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if (i, j) != (0, 0):
                        steps.add((i, j))

        if inclusive:
            steps.add((0, 0))
            
        return steps

if __name__ == "__main__":
    print(__file__)
    c = Combinations()