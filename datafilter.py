import glob
import os
import time
import configparser
import shutil

time.strftime("%Y%m%d", time.gmtime(time.time()-3600))
pathDirectory = configparser.ConfigParser()
pathDirectory.read_file(open(r'path_config.txt'))
inputPath = pathDirectory.get('PATH', 'INPUT')
outputPath = pathDirectory.get('PATH', 'OUTPUT')
archivePath = pathDirectory.get('PATH', 'ARCHIVE')

def createPathDirectory():
    if not os.path.exists(inputPath):
        os.makedirs(inputPath)
    if not os.path.exists(archivePath):
        os.makedirs(archivePath)
    if not os.path.exists(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20")):
        os.makedirs(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20"))
    if not os.path.exists(time.strftime(outputPath +"\\outputdata\\%Y%m%d\\CAT21")):
        os.makedirs(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT21"))
createPathDirectory()

os.chdir(inputPath)
patternName = "data.csv.*"
lines_seen = set()

def field_cat20(field): ## function to get the specific field fron the cat20 lines.
    if field != '13':
        x = "|" + field
        if x in cat20:
            field_raw = cat20.split(x + ":")[1]
            field_real = field_raw.split('|')[0]
        else:
            field_real = "unknown"
        return field_real
    else:
        if '|13' in cat20:
            field_raw = cat20.split('|13:')[1]
            field_raw2 = field_raw.split('|')[0]
            field_real = field_raw2[4:]
        else:
            field_real = "unknown"
        return field_real

def field_cat21(field): ## function to get the specific field fron the cat21 lines.
    x = "|" + field
    if x in cat21:
        field_raw = cat21.split(x + ":")[1]
        field_real = field_raw.split('|')[0]
    else:
        field_real = "unknown"
    return field_real

def eliminate_dup():
    for line in cut_date:
        if line not in lines_seen: # not a duplicate
            lines_seen.add(line)

while True:
    for fileName in glob.glob(patternName):
        inputFile = os.path.join(inputPath, fileName)
        inputData = open(inputFile, "r")
        for line in inputData:
            cut_date = line[13:] ## cut date in the first column and keep in variable .
            if cut_date not in lines_seen: ## remove the duplicated lines.
                lines_seen.add(cut_date)
                match1 = 'CAT20'
                match2 = 'CAT21'
                if match1 in line: ## extract the lines with matching CAT type.
                    cat20 = line
                    data = cat20.split('|')[0]
                    cat = cat20.split('|')[1]
                    x = field_cat20('12') ## keep all the field12(Aircraft_ID) to variable x.
                    if x not in lines_seen: ## remove the duplicated lines that the program had seen, it will remain one of each field12(Aircraft_ID).
                        lines_seen.add(x)
                        Aircraft_ID = x ## keep not duplicated field12(Aircraft_ID) to Aircraft_ID variable.
                    if Aircraft_ID in field_cat20('12'): ## checking and sorting the Aircraft_ID that matched in the field_cat20('12').
                        filename_a = time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20\\" + str(field_cat20('12').upper())) ## creating output files categorized by (Aircraft_ID).
                        a = open(filename_a, "a")
                        a.write(date + '\t' + field_cat20('3') +'\t'+ field_cat20('4') +'\t'+ field_cat20('12') +'\t'+ field_cat20('13')+'\t'+ field_cat20('14') +'\t'+ field_cat20('15') +'\t'+ field_cat20('19') +'\t'+ field_cat20('21')+'\n')
                        a.close()

                if match2 in line: ## extract the lines with matching CAT type.
                    cat21 = line
                    date = cat21.split('|')[0]
                    cat = cat21.split('|')[1]
                    x = field_cat21('5') ## keep all the field5(Aircraft_ID) to variable x.
                    if x not in lines_seen: ## remove the duplicated lines that the program had seen, it will remain one of each field12(Aircraft_ID).
                        lines_seen.add(x)
                        Aircraft_ID = x ## keep not duplicated field5(Aircraft_ID) to Aircraft_ID variable.
                    if Aircraft_ID in field_cat21('5'): ## checking and sorting the Aircraft_ID that matched in the field_cat20('5').
                        filename_b = time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT21\\" + str(field_cat21('5').upper())) ## creating output files categorized by (Aircraft_ID).
                        b = open(filename_b, "a")
                        b.write(date +'\t'+ cat +'\t'+ field_cat21('3') +'\t'+ field_cat21('4') +'\t'+ field_cat21('5') +'\t'+ field_cat21('18')+'\n')
                        b.close()
        inputData.close()
        shutil.move(inputFile, archivePath)


