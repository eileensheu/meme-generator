

from ingestor import Ingestor

print("\nIngesting _data/DogQuotes/DogQuotesTXT.txt")
qm = Ingestor.parse(path="_data/DogQuotes/DogQuotesTXT.txt")
for q in qm:
    print(q)

print("\nIngesting _data/SimpleLines/SimpleLines.txt")
qm = Ingestor.parse(path="_data/SimpleLines/SimpleLines.txt")
for q in qm:
    print(q)