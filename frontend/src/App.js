import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [string1, setS1] = useState('String1');
  const [string2, setS2] = useState('String2');
  const [distance, setDistance] = useState(0);
  const [isLoading, setIsLoading] = useState(false);



useEffect( () => {
setIsLoading(true);

const fetchData = async () => {
try {
const response = await fetch('http://127.0.0.1:5000/next');

const result = await response.json();

setS1(result['string1']);
setS2(result['string2']);
setDistance(result['val']);

} catch (e) {
console.error(e);
}
  

};


fetchData();
setIsLoading(false);
}, []);



  return (
   <div style={{alignContent:'center'}}>
    
    {isLoading ? (<p>Loading...</p>) : 
    (<><div id='isS1EqualToS2' >
     <div id='string1Vert' style={{display:'flex'}}> {string1.split("").map(word => {
      return <h3 style={{padding:'10px'}}>{word}</h3>
     })}</div>  <h3> {distance}</h3> <div id='string2Vert' style={{display:'flex'}}> {string2.split("").map(word => {
      return <h3 style={{padding:'10px'}}>{word}</h3>
     })}</div>
    </div>

    <div style={{display:'flex'}}> <button onClick={ () => {fetch('http://127.0.0.1:5000/addValid', {
  method: 'POST', // Specify the HTTP method
  headers: {
    'Content-Type': 'application/json', // Specify the content type
  },
  body: JSON.stringify({'valid': string1}), // Convert the data to JSON format
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
});}}>Add {string1} to verified Affils</button>  
    <button> replace {string1} with {string2}</button></div>
    <button onClick={ () => {
setIsLoading(true);

const fetchData = async () => {
try {
const response = await fetch('http://127.0.0.1:5000/next');

const result = await response.json();

setS1(result['string1']);
setS2(result['string2']);
setDistance(result['val']);

} catch (e) {
console.error(e);
}
  

};


fetchData();
setIsLoading(false);
}}> skip</button></>)}
   



   </div>
  );
}

export default App;
