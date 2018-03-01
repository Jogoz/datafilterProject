import glob
import os
import time
import configparser

time.strftime("%Y%m%d", time.gmtime(time.time()-3600))

pathDirectory = configparser.ConfigParser()
pathDirectory.read_file(open(r'path_config.txt'))
inputPath = pathDirectory.get('PATH', 'INPUT')
outputPath = pathDirectory.get('PATH', 'OUTPUT')


if not os.path.exists(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20")):
    os.makedirs(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20"))

if not os.path.exists(time.strftime(outputPath +"\\outputdata\\%Y%m%d\\CAT21")):
    os.makedirs(time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT21"))

os.chdir(inputPath)
patternName = "data.csv.*"
lines_seen = set()

def field_cat20(field):
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
            field_real = "\t"
        return field_real

def field_cat21(field):
    x = "|" + field
    if x in cat21:
        field_raw = cat21.split(x + ":")[1]
        field_real = field_raw.split('|')[0]
    else:
        field_real = "\t"
    return field_real

def eliminate_dup():
    for line in cut_date:
        if line not in lines_seen: # not a duplicate
            lines_seen.add(line)

for fileName in glob.glob(patternName):
    inputFile = os.path.join(inputPath, fileName)
    inputData = open(inputFile, "r")
    for line in inputData:
        cut_date = line[13:]
        if cut_date not in lines_seen:
            lines_seen.add(cut_date)
            match1 = 'CAT20'
            match2 = 'CAT21'
            if match1 in line:
                cat20 = line
                data = cat20.split('|')[0]
                cat = cat20.split('|')[1]
                x = field_cat20('12')
                if x not in lines_seen:
                    lines_seen.add(x)
                    Aircraft_ID = x
                if Aircraft_ID in field_cat20('12'):
                    filename_a = time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT20\\" + str(field_cat20('12').upper()))
                    a = open(filename_a, "a")
                    a.write(date + '\t' + field_cat20('3') +'\t'+ field_cat20('4') +'\t'+ field_cat20('12') +'\t'+ field_cat20('13')+'\t'+ field_cat20('14') +'\t'+ field_cat20('15') +'\t'+ field_cat20('19') +'\t'+ field_cat20('21')+'\n')
                    a.close()

            if match2 in line:
                cat21 = line
                date = cat21.split('|')[0]
                cat = cat21.split('|')[1]
                x = field_cat21('5')
                if x not in lines_seen:
                    lines_seen.add(x)
                    Aircraft_ID = x
                if Aircraft_ID in field_cat21('5'):
                    filename_b = time.strftime(outputPath + "\\outputdata\\%Y%m%d\\CAT21\\" + str(field_cat21('5').upper()))
                    b = open(filename_b, "a")
                    b.write(date +'\t'+ cat +'\t'+ field_cat21('3') +'\t'+ field_cat21('4') +'\t'+ field_cat21('5') +'\t'+ field_cat21('18')+'\n')
                    b.close()