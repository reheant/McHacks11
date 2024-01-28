import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Checkbox from '@mui/material/Checkbox';
import Button from '@mui/material/Button';
import '../css/Meeting.css';

const Meeting = () => {
  const location = useLocation();
  const { extractedText } = location.state || {};
  const [subjects, setSubjects] = useState([]);
  const [meetingInProgress, setMeetingInProgress] = useState(false);

  useEffect(() => {
    if (extractedText) {
      // Parse subjects from both methods and combine them
      const regexParsedSubjects = parseSubjectsFromRegex(extractedText);
      const jsonParsedSubjects = parseSubjectsFromJson(extractedText);
      const combinedSubjects = [...regexParsedSubjects, ...jsonParsedSubjects];
      setSubjects(combinedSubjects);
    }
  }, [extractedText]);

  const parseSubjectsFromRegex = (text) => {
    const subjectRegex = /(\d+)\.\s*\*\*(.*?)\*\*\s*\n\s*-\s*Description:\s*([^]+?)(?=\n\d+\.|\n\n|$)/g;
    const subjects = [];
    let match;
    while ((match = subjectRegex.exec(text)) !== null) {
      const [_, number, title, description] = match;
      subjects.push({ number, title, description, checked: false });
    }
    return subjects;
  };

  const parseSubjectsFromJson = (jsonText) => {
    try {
      const jsonData = JSON.parse(jsonText);
      return Object.keys(jsonData).map((key, index) => ({
        number: index + 1, // Assuming you want to number the subjects
        title: key,
        description: '', // Add descriptions if available
        checked: jsonData[key]
      }));
    } catch (e) {
      console.error('Error parsing JSON:', e);
      return [];
    }
  };

  const handleCheckboxChange = (index) => {
    setSubjects(subjects.map((subject, i) => 
      i === index ? { ...subject, checked: !subject.checked } : subject
    ));
  };

  const handleMeetingButton = async () => {
    if (!meetingInProgress) {
      try {
        const response = await fetch('http://localhost:5000/Start', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ meetingMinutes: extractedText }),
        });
        if (response.ok) {
          setMeetingInProgress(true);
          console.log('Meeting started successfully');
        } else {
          console.error('Error starting meeting');
        }
      } catch (error) {
        console.error('Error sending request:', error);
      }
    } else {
      try {
        const response = await fetch('http://localhost:5000/Stop', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          setMeetingInProgress(false);
          console.log('Meeting stopped successfully');
        } else {
          console.error('Error stopping meeting');
        }
      } catch (error) {
        console.error('Error sending request:', error);
      }
    }
  };

  return (
    <div>
      <h1 style={{marginLeft:"10px"}}>Meeting Minutes</h1>
      {subjects.map((subject, index) => (
        <Accordion key={index}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls={`panel${index}-content`} id={`panel${index}-header`}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
]              <span>
                {subject.number}. {subject.title}
              </span>
            </div>
          </AccordionSummary>
          <AccordionDetails>
            <p>{subject.description}</p>
          </AccordionDetails>
        </Accordion>
      ))}
      <Button sx={{marginTop:"15px",marginLeft:"10px"}} variant="contained" onClick={handleStartMeeting}>
        Start Meeting
      </Button>
    </div>
  );
};

export default Meeting;
