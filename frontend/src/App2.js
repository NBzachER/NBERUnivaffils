
import { useState, useEffect } from 'react';
import DropdownMenu from './DropDown';

function App2() {
    const [changesList, setChangesList] = useState([]);
    const [isLoading, setIsLoading] = useState(false);


    useEffect( () => {
        setIsLoading(true);
        const fetchData = async () => {
        try {
        const response = await fetch('http://127.0.0.1:5000/getChangesList');
        const result = await response.json();
        setChangesList(result['list']);
        setIsLoading(false);
        console.log(changesList)
        } catch (e) {
        console.error(e);
        }};
 
        fetchData();

        
        }, []);


        const alternateAffil = (idName, user, badAffil) => {
            console.log(idName);
            const textarea = document.getElementById(idName);
            
            try {
                console.log('it worked');
                replaceTheAffil(badAffil, textarea.value, user);
            } catch(exception) {
                console.log('it did not work');
            }
        
            };



    const replaceTheAffil = (badAffil, goodAffil, user) => {
        fetch('http://127.0.0.1:5000/replaceAffil', {method:'POST',
    headers: {'Content-Type': 'application/json'},
body: JSON.stringify({'replace':badAffil, 'replaceWith':goodAffil, 'user':user})})
.then(response => {if(!response.ok){throw new Error('NOOO ERRRORR!')}})
    }; 


    const changeUpperLim = () => {
        const textarea = document.getElementById('upperLim');
        fetch('http://127.0.0.1:5000/setUpperLimit', {method: 'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({'upperLim':textarea.value})})
        .then(response => {if(!response.ok){throw new Error('NOOO ERRRORR!')}})
    };

    return (<div style={{display:'flex'}}>
        <div style={{width:'5%', height:'auto'}}/>

        <div>
        {isLoading ? (<p>Loading...</p>) : 
            (<ul>
                {changesList.map(change => {

                   return (<li>{change[0]} to {change[1]} dist:{change[2]} <button onClick={ () => {fetch('http://127.0.0.1:5000/addValid', {
                    method: 'POST', // Specify the HTTP method
                    headers: {
                      'Content-Type': 'application/json', // Specify the content type
                    },
                    body: JSON.stringify({'valid': change[0]}), // Convert the data to JSON format
                  }).then(response => {
                    if (!response.ok) {
                      throw new Error('Network response was not ok');
                    }
                    return response.json(); // Parse the response body as JSON
                  })
                  .then(data => {
                    console.log('Response:', data); // Handle the response data
                  })
                  .catch(error => {
                    console.error('Error:', error); // Handle errors
                  });}}> Add {change[0]} to verified affils </button> <button onClick={() =>{ replaceTheAffil(change[0], change[1],change[3])}}> replace {change[0]} with {change[1]}</button>  
                  <div style={{display:'flex'}}><textarea id = {change[3] + ' ' + change[2] } > replace with something else...</textarea> <button onClick={() =>{ alternateAffil(change[3] + ' ' + change[2], change[3], change[0])}} style={{height:'35px', width:'55px'}}>Submit</button> </div> </li>)

                })}
            </ul>)
        }

        </div>

        <div style={{width:'20%', height:'auto'}}>
<div style={{marginBottom:'8%',display:'flex'}}>
        <button style={{height:'5%'}} onClick={ () => {
setIsLoading(true);            
fetch('http://127.0.0.1:5000/back')
.then(response => {
    if (!response.ok) {
        throw new Error('Response is not ok');
    }
    return response.json();
})
.then(data => {
    setIsLoading(false);
    setChangesList(data['list']);
})}}> Prev Page </button>

<button style={{height:'5%'}} onClick={() => { 
    setIsLoading(true);
    fetch('http://127.0.0.1:5000/continue')
.then(response => {
    if (!response.ok){
        console.log('NOOOOOO ERROR!!!! DETETECTED!!!00');
        throw new Error('EORRER DECTECTED!!! ');
    }
    return response.json();
})
.then(data => {
    setChangesList(data['list']);
    setIsLoading(false);
});
}}> Next Page</button>
<div style={{display:'flex'}}>
    <textarea id='upperLim'> What is the max allowed distance between words?(default = 3) the upper limit is exlcuded ie: 4 becomes 3  </textarea>
    <button onClick={() => {changeUpperLim()}}> Submit</button>
</div>
        </div>
        <DropdownMenu />
        </div>

    </div>);
}














export default App2;
