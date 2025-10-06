#BIBLIOGRAPHIC COMPLETENESS
#Uses algorithm based off of Ex Libris Bibliographic Rank to determine completeness of MARC records based on resource type and content standard

from pymarc import MARCReader, Field, Subfield
from tkinter import messagebox, filedialog
import pandas as pd
import datetime
import re

#Alma Bib Rank Breadth
def breadth(record):
    bscore = 0
    #Create string for critical errors
    #critical = '\"Record ID\",\"Error\"\n'
    #High importance fields/data
    highfields = [['050','082','060','070','080','083','086'],['250'],['010','020','022','024','028'],['100','110','111','700','710','711'],['260','264'],['245']]
    highsubs = ['600','610','611','630','647','648','650','651','655']
    highfixed = [[0,5],[6],[7,10],[11,14],[15,17],[35,37],[39]]
    medfields = [['007'],['344','345','346','347','348','310','321','382','384','362'],['300','336','337','338'],['490','800','810','811','830','780','785'],['520'],['505']]
    medfixed_music = [[18,19],[20],[21],[22],[23],[24,29],[30,31],[33]]
    medfixed_vis = [[18,20],[22],[28],[29],[33],[34]]
    medfixed_map = [[18,21],[22,23],[25],[28],[29],[31],[33,34]]
    medfixed_con = [[18],[19],[21],[22],[23],[24],[25,27],[28],[29],[33],[34]]
    lowfields = [[['010','z'],['020','z'],['022','y'],['022','z'],['024','z']],['041','042','044','047'],['502'],['504'],['773','776'],['130','240','740']]
    lowfixed_books = [[18,21],[22],[23],[24,27],[28],[29],[30],[31],[33],[34]]
    lowfixed_comp = [[22],[23],[26],[28]]
    #Check LDR
    try:
        record.leader
        bscore += 7
    except:
        record_id = str(record['001']).lstrip('=001  ').strip()
        print(f'Critical error: record {record_id} missing LDR.')
        #critical = critical + '\"' + str(record_id) + '\",\"Missing LDR\"\n'
    #Check for presence of high scoring fields
    for set in highfields:
        present = False
        for field in set:
            try:
                record[field]
                present = True
            except:
                continue
        if present == True:
            bscore += 7
    #Check subjects
    subs = False
    for field in highsubs:
        try:
            data = record.get_fields(field)
            for instance in data:
                if instance.indicator2 in [0,1,2,3,5,6]:
                    subs = True
                elif instance.indicator2 == 7:
                    try:
                        source = instance.get('2')
                        if source.lower() in ['aat','lacnaf','eurovoc','fast','fmesh','homoit','rameau','lcdgt','lcgft','lcmpt','ram','cona','tgn','rvm','rvmgf','rvmmem','rvmgd','rvmfast']:
                            subs = True
                    except:
                        continue
                    else:
                        continue
        except:
            continue
    if subs == True:
        bscore += 7
    #Check 008 common data
    nulls = re.compile(r'(\||#|\s)+')
    commondata = False
    try:
        record['008']
        print(record['008'])
        fixeddata = record['008'].value()
        print(f'FIXED DATA: {fixeddata}')
        for slice in highfixed:
            if len(slice) > 1:
                data = fixeddata[int(slice[0]):int(slice[1])]
            elif len(slice) == 1:
                data = fixeddata[int(slice[0])]
            else:
                print('Error: Slice invalid')
            if nulls.fullmatch(data):
                commondata = False
                continue
            else:
                commondata = True
                break
    except KeyError:
        record_id = str(record['001']).lstrip('=001  ').strip()
        print(f'Critical error: record {record_id} missing 008.')
        #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'      
    if commondata == True:
        bscore += 7
    print(f'HIGH BREADTH SCORE TOTAL: {bscore}')
    #Check for presence of med scoring fields
    for set in medfields:
        present = False
        for field in set:
            try:
                record[field]
                present = True
            except:
                continue
        if present == True:
            bscore += 3
    #Check for 008 (format dependent)
    form = None
    if record.leader[6] in ['c','d','i','j']:
        form = "music"
    elif record.leader[6] in ['g','k','o','r']:
        form = "visual"
    elif record.leader[6] in ['e','f']:
        form = "map"
    elif record.leader[6] == 'a' and record.leader[7] in ['b','i','s']:
        form = "cont"
    formdata = False
    if form == "music":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in medfixed_music:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                ##THIS IS BROKEN HERE, BUT NOT FOR HIGH SCORE FIELDS? NOT SURE ABOUT ALL OTHER FORMATS
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    elif form == "visual":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in medfixed_vis:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    elif form == "map":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in medfixed_map:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    elif form == "cont":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in medfixed_con:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    if formdata == True:
        bscore += 3
    print(f'HIGH AND MED BREADTH SCORE TOTAL: {bscore}')
    #Check low scoring fields
    invalid_codes = False
    for field in lowfields[0]:
        for set in field:
            try:
                fields = record.get_fields(set[0])
                for field in fields:
                    if field.get(set[1]) != None:
                        invalid_codes = True
            except:
                continue
    if invalid_codes == True:
        bscore += 1
    for set in lowfields[1:]:
        present = False
        for field in set:
            try:
                record[field]
                present = True
            except:
                continue
        if present == True:
            bscore += 7
    #Check for 008 (format dependent)
    form = None
    if record.leader[6] == 'm':
        form = "comp"
    elif record.leader[6] == 'a' and record.leader[7] in ['a','c','d','m']:
        form = "book"
    formdata = False
    if form == "comp":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in lowfixed_comp:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    elif form == "book":
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in lowfixed_books:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    formdata = False
                    continue
                else:
                    formdata = True
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
    if formdata == True:
        bscore += 1
    print(f'TOTAL BREADTH SCORE: {bscore}')
    return bscore

#Alma Bib Rank Depth
def depth(record):
    dscore = 0
    dfields_cap3 = [['050','082','060','070','080','083','086'],['041','042','044','047'],['344','345','346','347','348','310','321','382','384','362'],['490','800','810','811','830','780','785']]
    dfields_cap5 = [['100','110','111','700','710','711'],['300','336','337','338']]
    dfields_cap10 = [['010','a'],['010','b'],['020','a'],['022','a'],['024','a'],['028','a']]
    dfields_cap15 = ['600','610','611','630','647','648','650','651','655']
    highfixed = [[0,5],[6],[7,10],[11,14],[15,17],[35,37],[39]]
    fixed_music = [[18,19],[20],[21],[22],[23],[24,29],[30,31],[33]]
    fixed_vis = [[18,20],[22],[28],[29],[33],[34]]
    fixed_map = [[18,21],[22,23],[25],[28],[29],[31],[33,34]]
    count = 0
    #Check depth fields sets with cap of 3
    for set in dfields_cap3:
        for field in set:
            fields = record.get_fields(field)
            for _ in enumerate(fields):
                count += 1
                if count >= 3:
                    break
                else:
                    continue
        if count <= 3:
            dscore += count
        else:
            dscore += 3
    print(f'DEPTH SCORE CAP 3 IS {dscore}')
    #Check depth fields sets with cap of 5
    count = 0
    for set in dfields_cap5:
        for field in set:
            fields = record.get_fields(field)
            for _ in enumerate(fields):
                count += 1
                if count >= 5:
                    break
                else:
                    continue
        if count <= 5:
            dscore += count
        else:
            dscore += 5
    print(f'DEPTH SCORE CAP 3 + CAP 5 IS {dscore}')
    #Check depth fields with cap of 10
    count = 0
    for set in dfields_cap10:
        try:
            fields = record.get_fields(set[0])
            for field in fields:
                if field.get(set[1]) != None:
                    count += 1
        except:
            continue
    if count <= 10:
        dscore += count
    else:
        dscore += 10
    print(f'DEPTH SCORE CAPS 3, 5, AND 10 IS {dscore}')
    #Check subjects fields (cap of 15)
    ####PICK UP HERE: NEED TO FIX COUNTING FOR VALID SUBJECT FIELDS AND ADD COUNTING FOR 008 DATA (MUSIC, VIS, MAPS) WITH MAX 5 TO GET BIB RANK, THEN CHECK AGAINST ALMA RANKS FOR A SMALL SET
    count = 0
    for field in dfields_cap15:
        try:
            data = record.get_fields(field)
            for instance in data:
                if int(instance.indicator2) in [0,1,2,3,5,6]:
                    count += 1
                elif int(instance.indicator2) == 7:
                    try:
                        source = instance.get('2')
                        if source.lower() in ['aat','lacnaf','eurovoc','fast','fmesh','homoit','rameau','lcdgt','lcgft','lcmpt','ram','cona','tgn','rvm','rvmgf','rvmmem','rvmgd','rvmfast']:
                            count += 1
                    except:
                        continue
                    else:
                        continue
        except:
            continue
    if count <= 15:
        dscore += count
    else:
        dscore += 15
    print(f'DEPTH SCORE CAPS 3, 5, 10, AND 15 IS {dscore}')
    #Check common data in fixed field
    count = 0
    nulls = re.compile(r'(\||#|\s)+')
    try:
        record['008']
        print(record['008'])
        fixeddata = record['008'].value()
        print(f'FIXED DATA: {fixeddata}')
        for slice in highfixed:
            if len(slice) > 1:
                data = fixeddata[int(slice[0]):int(slice[1])]
            elif len(slice) == 1:
                data = fixeddata[int(slice[0])]
            else:
                print('Error: Slice invalid')
            if nulls.fullmatch(data):
                continue
            else:
                count += 1
                break
    except KeyError:
        record_id = str(record['001']).lstrip('=001  ').strip()
        print(f'Critical error: record {record_id} missing 008.')
        #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'      
    if count <= 5:
        dscore += count
    else:
        dscore += 5
    print(f'DEPTH SCORE WITH 008 IS {dscore}')
    #Check format-dependent fixed length data
    form = None
    if record.leader[6] in ['c','d','i','j']:
        form = "music"
    elif record.leader[6] in ['g','k','o','r']:
        form = "visual"
    elif record.leader[6] in ['e','f']:
        form = "map"
    count = 0
    if form == "music": 
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in fixed_music:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                ##THIS IS BROKEN HERE, BUT NOT FOR HIGH SCORE FIELDS? NOT SURE ABOUT ALL OTHER FORMATS
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    continue
                else:
                    count += 1
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
        if count <= 5:
            dscore += count
        else:
            dscore += 5
    elif form == "map": 
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in fixed_map:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                ##THIS IS BROKEN HERE, BUT NOT FOR HIGH SCORE FIELDS? NOT SURE ABOUT ALL OTHER FORMATS
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    continue
                else:
                    count += 1
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
        if count <= 5:
            dscore += count
        else:
            dscore += 5
    elif form == "visual": 
        try:
            record['008']
            print(record['008'])
            fixeddata = record['008'].value()
            print(f'FIXED DATA: {fixeddata}')
            for slice in fixed_vis:
                if len(slice) > 1:
                    data = fixeddata[int(slice[0]):int(slice[1])]
                ##THIS IS BROKEN HERE, BUT NOT FOR HIGH SCORE FIELDS? NOT SURE ABOUT ALL OTHER FORMATS
                elif len(slice) == 1:
                    data = fixeddata[int(slice[0])]
                else:
                    print('Error: Slice invalid')
                if nulls.fullmatch(data):
                    continue
                else:
                    count += 1
                    break
        except KeyError:
            record_id = str(record['001']).lstrip('=001  ').strip()
            print(f'Critical error: record {record_id} missing 008.')
            #critical = critical + '\"' + str(record_id) + '\",\"Missing 008\"\n'
        if count <= 5:
            dscore += count
        else:
            dscore += 5
    print(f'DEPTH SCORE TOTAL IS {dscore}')
    return dscore

def main():
    #Prompt user for file
    messagebox.showinfo(title=None,message="Select a set of records to process")
    file = None
    #Open file with try/except in while to catch errors
    while file == None:
        file = filedialog.askopenfilename()
        try:
            file = open(file,'rb')
            reader = MARCReader(file)
        except Exception as e:
            print(e)
            file = None
            continue
    #Create string for record scores
    record_scores = '\"Record ID\",\"Rank\"\n'
    #Create timestamp to prevent overwriting
    timestamp = datetime.datetime.now().strftime('%m%d%H%M')
    #Call scoring methods and write record ID and total score to string; add total score to local note field in record
    for record in reader:
        record_id = str(record['001']).lstrip('=001  ').strip()
        score1 = breadth(record)
        score2 = depth(record)
        total_score = score1 + score2
        print(total_score)
        record_scores = record_scores + '\"' + record_id + '\",\"' + str(total_score) + '\"\n'
        rankfield = Field(tag='995',subfields=[Subfield(code='a',value=str(total_score))])
        record.add_ordered_field(rankfield)
        with open(f'rankedrecords{timestamp}.mrc', 'ab') as fj:
            fj.write(record.as_marc())
    #Write IDs and scores to csv with unique timestamp to prevent overwriting
    with open(f'bibrank{timestamp}.csv','w',encoding='utf-8') as fh:
        fh.write(record_scores)
    print(f'Process completed successfully. Results written to bibrank{timestamp}.csv and rankedrecords{timestamp}.mrc')

if __name__ == "__main__":
    main()