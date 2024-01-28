// NewPage.js
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';
import '../css/Meeting.css'

export const MeetingMinutes = () => {
  const [minutes, setMinutes] = useState('');

  useEffect(() => {
    fetchMeetingMinutes();
  }, []); 

  const fetchMeetingMinutes = async () => {
    try {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // If you need to send a request body, include it here
        // body: JSON.stringify({ key: 'value' }),
      };

      // Make the POST request to your backend
      const response = await fetch('/Meeting', requestOptions);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Extract the data from the response
      const data = await response.text(); // or response.json() if your server sends JSON
      setMinutes(data); // Update state with the fetched data
    } catch (error) {
      console.error('There was an error fetching the meeting minutes:', error);
    }
  };

  return (
    <div>
      <h1>{minutes}</h1>
      {/* Display the fetched data */}
      <p>{minutes}</p>
    </div>
  );
};




export function AccordionUsage() {
    return (
      <div>
        <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            Accordion 1
          </AccordionSummary>
          <AccordionDetails>
            <MeetingMinutes/>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2-content"
            id="panel2-header"
          >
            Accordion 2
          </AccordionSummary>
          <AccordionDetails>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </AccordionDetails>
        </Accordion>
        <Accordion defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel3-content"
            id="panel3-header"
          >
            Accordion Actions
          </AccordionSummary>
          <AccordionDetails>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </AccordionDetails>
          <AccordionActions>
          </AccordionActions>
        </Accordion>
      </div>
    );
  }

const NewPage = () => {
  const location = useLocation();

  return (
    <>
        <div className='accordion'>
            <AccordionUsage/>
        </div>
    </>
  );
};

export default NewPage;
