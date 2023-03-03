from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Asentence = And(AKnight,AKnave)
knowledge0 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)), # Exclusive or that A can be either a knave or a knight
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence))   
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Asentence = And(AKnave,BKnave)
knowledge1 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)), # Exclusive or that A can be either a knave or a knight
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),  # Exclusive or that B can be either a knave or a knight
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence)) 
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asentence = Or(And(AKnave,BKnave),And(AKnight,BKnight))
Bsentence = Or(And(AKnave,BKnight),And(AKnight,BKnave))
knowledge2 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)),
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence)),
    Implication(BKnight,Bsentence),
    Implication(BKnave,Not(Bsentence)) 
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asentence = Or(AKnight,AKnave)
Bsentence1 = And(Implication(AKnight,AKnave),
Implication(AKnave,Not(AKnave))) # # B says "A said 'I am a knave'."
Bsentence2 = CKnave
Csentence = AKnight
knowledge3 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)), # Exclusive OR (+)
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),
    Or(And(CKnight,Not(CKnave)),And(Not(CKnight),CKnave)),
    Implication(AKnight,Asentence), # A is a knight if his sentence is True.
    Implication(AKnave,Not(Asentence)), # A is a Knave if sentence if false.
    Implication(BKnight,Bsentence1),
    Implication(BKnave,Not(Bsentence1)),
    Implication(BKnight,Bsentence2),
    Implication(BKnave,Not(Bsentence2)),
    Implication(CKnight,Csentence),
    Implication(CKnave,Not(Csentence))
)


def main():
    print(knowledge3.formula())
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
