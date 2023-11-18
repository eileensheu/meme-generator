

from ingestor import Ingestor

extension = "pdf"

p = "_data/DogQuotes/DogQuotes" + extension.upper() + f".{extension}"
print(f"\nIngesting {p}")
qm = Ingestor.parse(path=p)
for q in qm:
    print(q)

P = "_data/SimpleLines/SimpleLines" + f".{extension}"
print(f"\nIngesting {p}")
qm = Ingestor.parse(path=p)
for q in qm:
    print(q)