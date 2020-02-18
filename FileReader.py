class FileReader:

    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, "rb")
        self.nextChar = ""
        self.checkChar = ''

    def hasNext(self):
        """
        Check if there is another character iun the file and store it
        """
        self.checkChar = self.file.read(1).decode('utf-8');

        if self.checkChar != "":
            self.file.seek(-1, 1)
            return True

        return False

    def checkNext(self):
        """
        Return the next character without moving where we are pointing in the file
        """

        self.checkChar = self.file.read(1).decode('utf-8');

        if self.checkChar != "":
            self.file.seek(-1, 1)

        return self.checkChar if self.hasNext() else None

    def readNext(self):
        """
        Returns the next character in the file
        """
        self.nextChar = self.file.read(1).decode('utf-8');

        return self.nextChar if self.hasNext() else None


    def ignoreLine(self):

        self.file.readline()


