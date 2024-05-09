README

Hello, This is an overview of the Univaffil standardization project, by Zach. 


Front-end: 

The Front end of this project consists of 20 affiliation suggestions, the only way an affiliation can be displayed here is if it's not on the verifiedAffils list containing all valid affailitions, or if the distance between the og affil and the suggested affil falls out of the upper limit. The user has 3 options when dealing with a suggestion, 1. add og affil to the verifiedAffils list, meaning it is a valid affiliation 2. repalce og affil with suggested affil, this will replace this affil in the database 3. repalce with anything, if a user knows an affiliation is incorrect and the suggested affiliation is also not correct there is a textbox which the user can insert anything they would like, this will change the affil in the database if the "submit" button is clicked. 

Outside of the changes list there also exists the Universal Changes dropdown menu. This menu allows the user to run changes, like NYU -> New York University, which affects the entire database. They also have the option to create their own universal changes, there is a textbox at the bottom of the dropdown menu which allows the users to insert "old -> new" which will act as a universal change across the DB. 


    APP2.js:
        [{}] changesList: 20 change suggestions, each item in the list has a map holding the og affiliation, the suggested affiliation and the user name of the og affil

        Boolean isLoading: determines if an async call has been made to the back end to update hte changesList

        func replaceTheAffil = takes in badAFfil(old affil) goodAffil(new affil) and user(string username) makes a call to the back to run an update call to change the affiliation of user 

        func changeUpperLim = grabs the value out of the upperLim text area and sends a call to the back end to change the upper limit of the distnace between 2 words
    
    DropDown.js:

    func uniReplace: (oldValue, newValue, CA) all arguments are self explanatory besides CA, CA is a hard coded boolean which determines if the unireplace is the hard coded University of CA, -> University of CA at. This has different logic than all other uniReplaces due to the regex on the back end. This function replace all oldValues with the given newValue 

    func alteranteUniReplace: user inputted uniReplace, cleans the text before sending it to uniReplace



Back-end 

    Dependancies:
         flask, flask_cors, requests, and urllib.parse 

    Basic Idea:
        Simple rest API carrying out DB opperations and string similarity scores
    
    Global Variables:
        List<String> linesAffils: a list holding every affiliation that is not "" or null, the list is in alphabetical order a->z

        List<String> linesSorted: This is a poor variable name, but it holds the verified affiliations, primary purpose is to act as a "string 2" for comparasions against linesAffils

        List<String> linesAffilsNames: this holds the usernames of the Affiliations in linesAffils, it is one to one as in LinesAffilsNames[i] goes with linesAffils[i]

        int global_iter: this is the iterator which traverses through linesAffils, it holds it's value until the back-end is restarted. it starts at 3820 as this is the first occurence of a non "" string

        int global_i: PLEASE IGNORE THIS VALUE IT WAS USED FOR APP.JS not APP2.js 

        int global_upper_limit: this variable represents the upperbounds for the similarity algo, the value is not included as in 4 allows for 3,2,1 

    Endpoint:
        /next: ignore not used in APP2.js only in APP.js which is not used anymore

        /addValid: adds a validAffil to the text file verifiedAfils.txt, it is also added to linesSorted to keep an up to date enviornment 

        /getChangesList: returns the first 20 string pairs which fall between 1 and global_upper_limit, the iterator begins at the last point global_iter left off at

        /setUpperLimit: set the global_upper_limit var to user inputted value 

        /continue: advance the changesList to the next 20 matches 

        /back: return the previous 20 matches 

        /uniReplace: Universal replace function University of California, -> University of California at is hard coded under the torf variable(true or false)

        /replaceAffil: make a DB call to replace oldAffil with the newAffil

    Optimizations: 
        convert verifiedAffils.txt to a table in the DB, or make it its own DB 

        run getChngesList on the entire dataset every night to reduce wait times for the first run through of the day  
    
    Changes: 
        any update query is not currently working due to an API issue, this is unfixable on my end at the moment 

        If my account is deleeted this program WILL NOT WORK due to my personal cookie being put into the get requests to access the database

        all the update queries are commented out these exist at lines 263 and 286

        this program is running on port 5000, so if it were to be put into production a change would need to be made to the endpoints on the front end 





