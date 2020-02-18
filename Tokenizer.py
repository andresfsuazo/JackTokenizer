import re
import xml.etree.ElementTree as ET
"""
TO Do later
    -Last character in each line is not being read
    -String are read as identifiers
        -Check for quotes required
"""
class Tokenizer:
    classification = ["symbol", "keyword", "identifier", "integerConstant", "stringConstant"]
    spaces = ["\n", "\t", " ", "\r"]
    symbols = ["[", "]", "(", ")", "{", "}", ",", ";", "=", ".", "+", "-", "*", "/", "&", "|", "<", ">", "~"]
    reservedWords = ["class", "constructor", "method", "function", "int", "boolean", "char",
                     "void", "var", "static", "field", "let", "do", "if", "while", "return", "true", "false", "null",
                     "this"]
    identifier = "\w+"
    intConst = "\d+"
    strConst = "\"(\S*\s*)*\""
    boolConst = ["true", "false"]
    xmlReservedMap = {'<':'&lt;', '>':'&gt;', '\"':'&quot;', '&':'&amp;'}

    def __init__(self, file):
        self.tokens = []
        self.currentToken = ""
        self.currentChar = ''
        self.file = file
        self.done = False
        self.types = []
        self.formatDict = {}

    def toXML(self):
        # create the file structure
        data = ET.Element('tokens')
        items = ET.SubElement(data, 'items')
        item1 = ET.SubElement(items, 'item')
        item2 = ET.SubElement(items, 'item')
        item1.set('name', 'item1')
        item2.set('name', 'item2')
        item1.text = 'item1abc'
        item2.text = 'item2abc'

        # create a new XML file with the results
        mydata = ET.tostring(data)
        myfile = open("MainT.xml", "w")
        myfile.write(mydata)

    def toFile(self, fileName):
        with open(fileName, "w") as file:
            file.write("<tokens>\n")
            for i in self.tokens:
                if i in self.xmlReservedMap:
                    i = self.xmlReservedMap[i]
                file.write("\t<{1}> {0} </{1}>\n".format(i, self.formatDict[i]))
            file.write("</tokens>")

    def ignoreSpaces(self):
        # Ignore whitespaces
        while self.currentChar in self.spaces:
            self.currentChar = self.file.readNext()

    def ignoreComments(self):
        # Ignore comments
        while self.currentChar == "/" and (self.file.checkNext() == "/"):
            self.file.ignoreLine()
            self.currentChar = self.file.readNext()

    def getToken(self):
        """
        Retrieves character by character from file reader and separates them into
        jack tokens
        """

        self.currentChar = self.file.readNext()
        self.currentToken = ""

        if self.currentChar == None:
            self.done = True
            return

        self.ignoreSpaces()
        self.ignoreComments()

        self.ignoreSpaces()

        # Check multiple line comments
        while self.currentChar == "/" and (self.file.checkNext() == "*"):
            self.file.readNext()
            while True:
                self.currentChar = self.file.readNext()
                if self.currentChar == "*" and self.file.checkNext() == "/":
                    self.file.readNext()
                    self.currentChar = self.file.readNext()
                    break

        self.ignoreSpaces()

        while True:
            if self.file.hasNext() == False:
                return

            self.currentToken += self.currentChar

            if self.currentToken.startswith("\""):
                if self.file.checkNext() == "\"":
                    self.currentToken = self.currentToken + self.file.readNext()
                    return

            # Check for space
            elif self.file.checkNext() in self.spaces:
                self.tokens.append(self.currentToken)
                return

            # Check for symbols
            elif (self.currentToken in self.symbols) or (self.file.checkNext() in self.symbols):
                self.tokens.append(self.currentToken)
                return

            #Check for keyword
            elif self.currentToken in self.reservedWords:
                self.tokens.append(self.currentToken)
                return

            self.currentChar = self.file.readNext()


    def printTokens(self):
        print(self.tokens)

    def fillDict(self):
        """
        Check if token
            -Symbol
            -Keyword
            -Identifier
            -integerConstant
            -stringConstant

        Add to dictionary, keys are the tokens and the values are the types fo tokens
        """
        #<, >, ", &
        #&lt;, &gt;, &quot;, and &amp

        for token in self.tokens:
            #Symbol
            if token in self.symbols:
                if token in self.xmlReservedMap:
                    token = self.xmlReservedMap[token]
                self.formatDict[token] = "symbol"

            #Keyword
            elif token in self.reservedWords:
                self.formatDict[token] = "keyword"

            #IntegerConstant
            elif re.search(self.intConst, token):
                self.formatDict[token] = "integerConstant"

            #Identifier
            elif re.search(self.identifier, token):
                self.formatDict[token] = "identifier"

            #stringConstant
            elif re.search(self.strConst, token):
                self.formatDict[token] = "stringConstant"


    def printFormatted(self):
        print("<tokens>")
        for i in self.tokens:
            if i in self.xmlReservedMap:
                i = self.xmlReservedMap[i]
            print("\t<{1}> {0} </{1}>".format(i, self.formatDict[i]))
        print("</tokens>")
