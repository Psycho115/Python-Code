def TrimLine(inputStr):
    inputStr = inputStr.replace("，", ",")
	inputStr = inputStr.replace("\t", " ")
	while inputStr.find(" ") != -1:
		inputStr = inputStr.replace(" ", "")
    return inputStr

def TrimComment(inputStr):
    nCommentIndex = inputStr.find(_T("//"))
    if nCommentIndex != -1:
        inputStr = ""
    return inputStr

def ProcessFile(fileName):

    matLines = []
    

    with open('/path/to/file', 'r') as file:
        lines = file.readlines()
    
    for index in xrange(len(lines)):
        line = lines[index]

        line = TrimLine(line)
        line = TrimComment(line)

        if line == "/MATERIAL/"

