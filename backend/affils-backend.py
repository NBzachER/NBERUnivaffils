from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
import requests
from urllib.parse import quote
import mariadb

app = Flask(__name__)
CORS(app)


global_i = 0

linesAffils = []
linesSorted = None
linesAffilsNames = []


def excuteSQL(qry):
        password = 'zoalekri'
        # I am not sure where the password file is but if you could replace the /path/to... in the open function this code below should read 
        #from the file and set the first line equal to password, if the password is not on the first line put in the correct line using the lines array! 
        #keep in mind the readlines function splits based off of \n characters but keeps them in I am 99% sure so this could be a cause for errors
        #with open('/etc/mysql_nobody_password.txt', 'r'):
         #       lines = file.readlines()
        #password = lines[0]
        try:
            conn = mariadb.connect(user="nobody", password=password, host="mysql.nber.org", database="nber_mysql")
            print("Connected successfully to MariaDB!")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            return "SOMETHING WENT WRONG" 
        cur = conn.cursor()

        try:
                cur.execute(qry)
                conn.commit()
                print("success!!")
        except mariadb.Error as e:
            print(f"Error updating data: {e}")
             
        cur.close()
        conn.close()
        return cur.fetchall()



         

def levReplacement(str1, str2):
        # Declaring array 'D' with rows = len(a) + 1 and columns = len(b) + 1:
    D = [[0 for i in range(len(str2) + 1)] for j in range(len(str1) + 1)]

# Initialising first row:
    for i in range(len(str1) + 1):
     D[i][0] = i

# Initialising first column:
    for j in range(len(str2) + 1):
        D[0][j] = j

    for i in range(1, len(str1) + 1):
     for j in range(1, len(str2) + 1):
         if str1[i - 1] == str2[j - 1]:
             D[i][j] = D[i - 1][j - 1]
         else:
            # Adding 1 to account for the cost of operation
            insertion = 1 + D[i][j - 1]
            deletion = 1 + D[i - 1][j]
            replacement = 1 + D[i - 1][j - 1]

            # Choosing the best option:
            D[i][j] = min(insertion, deletion, replacement)
    return D[len(str1)][len(str2)]


def stringSimilarity(str1, str2):
    #longest = lcs(str(str1), str(str2)) 
   # if str1 in str2 and str(str1).replace(' ', '') != str(str2).replace(' ', ''):
    #    return 100
    #else:
    #    return 0
   # seventyPercent = (float(longest) / float(max(len(str1), len(str2))))
    #return seventyPercent
    #return longest
    return levReplacement(str1, str2)


def findMostSim(str2):
    smallest = 10000000
    mostSimilarString = ''
    for i in range(2, len(linesSorted)):

        str1 = linesSorted[i].split('=')[0]

        if str1 == '':
            continue
        if str1 != str2:
            simScore = stringSimilarity(str1.rstrip(), str(str2))

            if simScore < smallest:
                smallest = simScore
                mostSimilarString = str1
        else:
            smallest = 0
            mostSimilarString = str2
            break

        
    return smallest, mostSimilarString


def init():
    global linesAffils
    global linesSorted
    global linesAffilsNames
    lines = None
    #with open('correctDocument.txt', 'r', encoding='utf-8') as file:
    #    lines = file.readlines()
    
    #for line in lines:
    #   temp = line.split('\t')
       
    #   linesAffils.append(temp[1])
     #  linesAffilsNames.append(temp[0])


    response = excuteSQL("SELECT user, univaffil FROM people WHERE user IS NOT NULL AND univaffil IS NOT NULL ORDER BY univaffil ASC")    
    #url = 'https://backdev.nber.org/cgi-bin//backend_mysql.pl?sql=select%20user%2c%20univaffil%20from%20people%20where%20user%20is%20not%20null%20and%20univaffil%20is%20not%20null%20order%20by%20univaffil%20asc'
    #cookie = {'STYXKEY_username_ticket_cookie': '702214287-zach_hixson'} #when my account is deactivated this code will stop working!
    #response = requests.get(url,cookies=cookie)
    if response != "SOMETHING WENT WRONG":
        # Print the JSON data returned by the API
        #print(response.json())
       print('Ok')

    else:
        # Print an error message if the request failed
        print('Error:' + response)

    #db_return =response.json()
    db_return = response
    print(len(db_return))

    for i in range(len(db_return)):
      linesAffils.append(db_return[i]['univaffil'])
      linesAffilsNames.append(db_return[i]['user'])

    encodings_to_try = [ 'cp1252', 'iso-8859-1'] 
    for encoding in encodings_to_try:
     try:
        with open('verifiedAfils.txt', 'r', encoding=encoding) as file:
            linesSorted = file.readlines()
        print("File read successfully with encoding:", encoding)
        break  
     except UnicodeDecodeError:
        print("Failed to read file with encoding:", encoding)

@app.route('/next')
def next():
    global global_i
    global_i += 1
    if linesAffils == [] or linesSorted == None:
       init()
    
    currentWord = linesAffils[global_i].split('=')[0]

    while currentWord == '' or currentWord == '\n' or currentWord == 'NULL\n':
       global_i += 1


    while currentWord in linesSorted:
       global_i += 1
       currentWord = linesAffils[global_i].split('=')[0]

    val, mostSim = findMostSim(currentWord)

    while val == 1:
       global_i += 1
       currentWord = linesAffils[global_i].split('=')[0]
       val, mostSim = findMostSim(currentWord)

    return jsonify({'string1': currentWord, 'string2': mostSim, 'val': val})



@app.route('/addValid', methods=['POST'])
def addValid(): 
   data = request.json
   word = data['valid']
   
   with open('verifiedAfils.txt', 'a', newline='') as file:
      file.write(f"\n{str(word).strip()}=-13")
   linesSorted.append(str(word).strip())
    
global_iter = 3820
global_upper_limit = 4

@app.route('/getChangesList')
def getChangesList():
    global global_upper_limit
    if linesAffils == [] or linesSorted == None:
       init()
    result = []
    global global_iter
    print(len(linesAffils))
    print(len(linesAffilsNames))
    while len(result) < 20 and global_iter < len(linesAffils):
        currentWord = linesAffils[global_iter]
        val, mostSim = findMostSim(currentWord)

        if val > 1 and val < global_upper_limit: #starts at 4
           result.append([currentWord, mostSim,val, linesAffilsNames[global_iter]])
        global_iter = global_iter + 1
    
    print(global_iter)
    return jsonify({'list':result})
       
      
    
@app.route('/setUpperLimit', methods=['POST'])
def changeUpperBounds():
   data = request.json
   num = data['upperLim']
   global global_upper_limit
   if int(num) < 2:
      return 'Number is too small' 
   global_upper_limit = int(num)
   return 'Ok'



@app.route('/continue')
def contin():
   global global_iter
   if linesAffils == [] or linesSorted == None:
       init()
   if global_iter < len(linesAffils):
    result = getChangesList()
    return result




@app.route('/back')
def back():
    global global_iter
    if linesAffils == [] or linesSorted == None:
       init()
    result = []
    global global_iter
    global_iter -= 2
    while len(result) < 20 and global_iter > 3821:
        currentWord = linesAffils[global_iter]
        val, mostSim = findMostSim(currentWord)

        if val > 1 and val < 4:
           result.append([currentWord, mostSim,val,linesAffilsNames[global_iter]])
        global_iter = global_iter - 1
    

    return jsonify({'list':result})
    


@app.route('/uniReplace', methods=['POST'])
def UniversalReplace():
    data = request.json
    oldValue = data['old']
    newValue = data['new']
    torf = data['torf']
    if torf:
       
       #url = 'https://backdev.nber.org/cgi-bin//backend_mysql.pl?sql=select%20user%20%2c%20univaffil%20from%20people%20where%20univaffil%20like%20%22University%20of%20California%2c%25%22'
       #cookie = {'STYXKEY_username_ticket_cookie': '702214287-zach_hixson'} #when my account is deactivated this code will stop working!
       #response = requests.get(url,cookies=cookie)
       response = excuteSQL(repr("select user, univaffil from people where univaffil like '%University of California,%'"))    
       if response == "SOMETHING WENT WRONG":
        # Print the JSON data returned by the API
        #print(response.json())
        print('Error:', response.status_code)




       #db_return =response.json()
       db_return =response
        
       changes = []
       for i in range(len(db_return)):
          if len(db_return[i]) == 2:
            newparts = str(db_return[i]['univaffil']).split(',')
            if len(newparts) == 2:
                newAffil = newparts[0] + ' at' + newparts[1] 
                temp = f"update people set univaffil = '{newAffil}' where user = '{db_return[i]['user']}'"
                changes.append(temp)
       #run the changes list and update each occurence 

      
       for i in range(len(changes)):
          print(changes[i])
          executeSQL(repr(changes[i]))
       
    else:
        #url = 'https://backdev.nber.org/cgi-bin//backend_mysql.pl?sql='
        #cookie = {'STYXKEY_username_ticket_cookie': '702214287-zach_hixson'}
        

        sql = f"update people set univaffil = '{str(newValue).strip()}' where univaffil = '{oldValue}'"
        response = excuteSQL(repr(sql))
        #url += quote(sql)
        #print(url)
        
        #response = requests.get(url,cookies=cookie)
        
    return 'OK'

       
        
@app.route('/replaceAffil',methods=['POST'])
def replaceAffil():
    data = request.json
    affil = data['replace']
    newAffil = data['replaceWith']
    user = data['user']
    
    
    if affil != '' and newAffil != '' and user != '':
        
        
        #url = 'https://backdev.nber.org/cgi-bin//backend_mysql.pl?sql='
        #cookie = {'STYXKEY_username_ticket_cookie': '702214287-zach_hixson'}

        sql = f"update people set univaffil = '{str(newAffil).strip()}' where user = '{user}' and univaffil = '{affil}'"
        executeSQL(repr(sql))
        #url += quote(sql)
            
        #print(url)
        #response = requests.get(url,cookies=cookie)

    return 'OK'
    



if __name__ == '__main__':
    app.run(debug=True)
