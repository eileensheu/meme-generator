

from ingestor import Ingestor

print("\nIngesting _data/DogQuotes/DogQuotesDOCX.docx")
qm = Ingestor.parse(path="_data/DogQuotes/DogQuotesTXT.txt")
for q in qm:
    print(q)

print("\nIngesting _data/SimpleLines/SimpleLines.docx")
qm = Ingestor.parse(path="_data/SimpleLines/SimpleLines.txt")
for q in qm:
    print(q)