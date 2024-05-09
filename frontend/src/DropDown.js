import React, { useState } from 'react';

function DropdownMenu() {
  // State to track whether the dropdown is open or closed
  const [isOpen, setIsOpen] = useState(false);

const alteranteUniReplace = () => {
    const textarea = document.getElementById('anyglobalreplace');
    console.log(textarea.value);
    const splitTextContent = textarea.value.split('->');
            if (splitTextContent.length === 2) {

                uniReplace(splitTextContent[0].replace(/^\s+|\s+$/g, ''), splitTextContent[1], false);

            }

};

  const uniReplace = (oldValue, newValue, CA) => {
    fetch('http://127.0.0.1:5000/uniReplace', {method:'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'old': oldValue, 'new': newValue, 'torf':CA})})
    .then(response => {if(!response.ok){console.error(response)}});
  };

  
  // State to track the selected option
  const [selectedOption, setSelectedOption] = useState('');



  return (
    <div className="dropdown">
      {/* Button to toggle the dropdown */}
      <button onClick={() => setIsOpen(!isOpen)}>Universal Replace</button>

      {/* Dropdown menu */}
      {isOpen && (
        <div style={{display:'flex', flexDirection:'column'}}>
          {/* Menu items */}
          <button onClick={() => uniReplace('University of California,', 'University of California at', true)}>University of California, &lt;location&gt; -&gt; University of California at &lt;location&gt;</button> {/* DO NOT FORGET TO ADD THE and LOGIC!!!! THIS IS BEYOND IMPORTANT*/}
          <button onClick={() => uniReplace('NYU', 'New York University', false)}>NYU -&gt; New York University</button> {/* DO NOT FORGET TO ADD THE and LOGIC!!!! THIS IS BEYOND IMPORTANT*/} 
          <button onClick={() => uniReplace('MIT', 'Massachusetts Institute of Technology', false)}>MIT -&gt; Massachusetts Institute of Technology</button> {/* DO NOT FORGET TO ADD THE and LOGIC!!!! THIS IS BEYOND IMPORTANT*/}
          <button onClick={() => uniReplace('ASU', 'Arizona State University', false)}>ASU -&gt; Arizona State University</button> {/* DO NOT FORGET TO ADD THE and LOGIC!!!! THIS IS BEYOND IMPORTANT*/}
          <button onClick={() => uniReplace('USC', 'University of Southern California', false)}>USC -&gt; University of Southern California</button> {/* DO NOT FORGET TO ADD THE and LOGIC!!!! THIS IS BEYOND IMPORTANT*/}
          <div style={{display:'flex'}}> 
            <textarea id='anyglobalreplace' style={{width:'100%'}}> og -&gt; new (please include the arrows!)</textarea> <button onClick={() => {alteranteUniReplace();}}> Submit</button>
          </div>
        </div>
      )}

      {/* Display the selected option */}
      {selectedOption && <p>Selected Option: {selectedOption}</p>}
    </div>
  );
}

export default DropdownMenu;
