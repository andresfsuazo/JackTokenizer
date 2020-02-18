import Tokenizer
import FileReader


def main():
    #fileReader = FileReader.FileReader("testFile.txt")
    fileReader = FileReader.FileReader("Main.jack")
    tokenizer = Tokenizer.Tokenizer(fileReader)

    while not tokenizer.done:
        tokenizer.getToken()

    tokenizer.fillDict()
    #tokenizer.printFormatted()
    tokenizer.printTokens()
    tokenizer.toFile("MainT.xml")


if __name__ == "__main__":
    main()