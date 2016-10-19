'''

This module is designed to extract information from specifically-designed two kinds of xml files and create one re-designed new xml file.
Therefore, the two differently-formed xml files which have similar information can be unified into one new xml file.

'''


#############################################################################
#
# Authors:
# 
# Tessa(Hyeri) Song (songt@unimelb.student.edu.au)
#
# Date created:
# 
# 25 March 2014
#
# Date modified and reason:
#
# None
#
##############################################################################


from lxml import etree


#Element list for functions readFirstURL() and readSecondURL()
eleList = ("title", "rating", "studio", "genre" ,"writer", "director", "year", "origin", "metascore", "earnings")


# Extract information from the data source of the first URL and return a list of dictionaries.
def readFirstURL(url):
    xmlTree = etree.parse(url)
    root = xmlTree.getroot()
    movieDicList = []
    movieIdx = 0
    
    for ele1 in root:
        movieDicList.append({})
        actors = []
        scores = []
        i = 0
        for ele2 in ele1:
            if ele2.tag == "reviews":
                for ele3 in ele2:
                    reviewer = ele3.get("reviewer")
                    score = ele3.get("value")
                    scores.append((reviewer,score))
                movieDicList[movieIdx]["scores"] = scores
            elif ele2.tag == "actors":
                valueList = ele2.attrib.values()
                for value in valueList:
                    actors.append(value)
                movieDicList[movieIdx]["actors"] = actors
            else:
                movieDicList[movieIdx][eleList[i]] = ele2.text
                i+=1
        movieIdx+=1

    return movieDicList


#Extract information from the data source of the first URL and return a list of dictionaries.
def readSecondURL(url):
    xmlTree = etree.parse(url)
    root = xmlTree.getroot()
    movieDicList = []
    movieIdx = 0

    for ele1 in root:
        movieDicList.append({})
        actors = []
        scores = []
        actorsIdx = 1
        i = 0
        for ele2 in ele1:
            if ele2.tag == "Actor"+str(actorsIdx):
                actors.append(ele2.text)
                actorsIdx+=1
            elif ele2.tag == "score":
                reviewer = ele2.get("src")
                score = ele2.text
                if score == None:
                    score = ""
                scores.append((reviewer,score))    
            else:
                movieDicList[movieIdx][eleList[i]] = ele2.text  
                i+=1  
        movieDicList[movieIdx]["actors"] = actors
        if scores != []:
            movieDicList[movieIdx]["scores"] = scores
        movieIdx+=1
        
    return movieDicList


#Write a new xml file based on the extracted information by the two functions above.
def writeXML(movieDicList):
    
    #standard for the arrangement of elements.
    NewXMLeleList = ("title", "rating", "studio", "genre", "actors", "writer", "director", "year", "origin", "scores", "metascore", "earnings")
    
    fopen = open("movies.xml", "w")
    fopen.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fopen.write("<movieList>\n")
    
    for movie in movieDicList:
        fopen.write("<movie>\n")
        for ele in NewXMLeleList:
            if ele == "actors":
                fopen.write("<actors>\n") 
                for actor in movie.get("actors"):
                    fopen.write("<actor>"+actor+"</actor>\n")
                fopen.write("</actors>\n")
            elif ele == "scores": 
                if "scores" in movie:
                    fopen.write("<scores>\n")
                    for score in movie.get("scores"):
                        if(score[1] == ""):
                            fopen.write("<score src="+'"'+score[0]+'"'+" />\n")
                        else:
                            fopen.write("<score src="+'"'+score[0]+'">'+str(score[1])+"</score>\n")
                    fopen.write("</scores>\n")   
            else:
                fopen.write("<"+ele+">"+movie.get(ele)+"</"+ele+">\n")
        fopen.write("</movie>\n")
        
    fopen.write("</movieList>")
    fopen.close()


def main():
    movieDicList01 = readFirstURL("http://students.informatics.unimelb.edu.au/~ivow/foi/mywork/public/lord_of_the_rings.xml")
    movieDicList02 = readSecondURL("http://students.informatics.unimelb.edu.au/~ivow/foi/mywork/public/harry_potter.xml")
    movieDicList = movieDicList01+movieDicList02
    writeXML(movieDicList)

#Execute this script     
main()
