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

  const handleStartMeeting = async () => {
    // Replace with your backend endpoint and data format
    try {
      const response = await fetch('/start-meeting', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subjects }),
      });
      if (response.ok) {
        console.log('Meeting started successfully');
      } else {
        console.error('Error starting meeting');
      }
    } catch (error) {
      console.error('Error sending request:', error);
    }
  };

  const handleDuring = async () => {
    try {
      const response = await fetch('/checkbox', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subjects }),
      });
      if (response.ok) {
        console.log(JSON.stringify({ subjects }))
        console.log('checkbox content received successfuly');
      } else {
        console.error('Error with checkbox');
      }
    } catch (error) {
      console.error('Error sending request:', error);
    }
  };

  const MeetingAgenda = ({ initialSubjects }) => {
    const [subjects, setSubjects] = useState(initialSubjects);
  
    const handleCheckboxChange = async (index) => {
      // Update the local state
      const newSubjects = subjects.map((subject, idx) => {
        if (idx === index) {
          return { ...subject, checked: !subject.checked };
        }
        return subject;
      });
  
      setSubjects(newSubjects);
  
      // Send the updated subjects to the backend
      try {
        const response = await fetch('/checkbox', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ subjects: newSubjects }),
        });
  
        if (response.ok) {
          console.log('Checkbox content updated successfully');
        } else {
          console.error('Error with checkbox');
        }
      } catch (error) {
        console.error('Error sending request:', error);
      }
    };
  
    return (
      <div>
        {subjects.map((subject, index) => (
          <div key={subject.number}>
            <input
              type="checkbox"
              checked={subject.checked}
              onChange={() => handleCheckboxChange(index)}
            />
            <label>{subject.title}</label>
          </div>
        ))}
      </div>
    );
  };
  const initialSubjects = [
    {
      "number": "1",
      "title": "Welcome & Introductions",
      "description": "Start the meeting by welcoming all participants and facilitating brief introductions. This is an opportunity for team members to connect and for new attendees to be familiarized with the group, creating a friendly and engaging meeting atmosphere.",
      "checked": false
    },
    {
      "number": "2",
      "title": "Business Overview",
      "description": "Present a high-level overview of the business, including recent developments, market trends, and strategic direction. This segment provides context for the meeting, aligning everyone with the company's current position and future objectives.",
      "checked": false
    },
    {
      "number": "3",
      "title": "Current Performance Snapshot (Financials, Key Metrics)",
      "description": "Review the latest financial results and key performance indicators. This analysis helps assess the health of the business, understand trends, and identify areas needing attention or improvement.",
      "checked": false
    },
    {
      "number": "4",
      "title": "Update on Project X (3 minutes)",
      "description": "Provide a concise update on the status of Project X, covering progress made, milestones achieved, and any immediate next steps or decisions required. This keeps the team informed and allows for quick feedback or input on the project's direction.",
      "checked": false
    },
    {
      "number": "5",
      "title": "Discussion on Challenges and Solutions (5 minutes)",
      "description": "Open the floor for a focused discussion on current challenges facing the team or project. Encourage sharing of ideas and collaboratively explore potential solutions, fostering a problem-solving mindset and team collaboration.",
      "checked": false
    },
    {
      "number": "6",
      "title": "Closing",
      "description": "Conclude the meeting by summarizing key takeaways, action items, and assigning responsibilities. Confirm the time and date for the next meeting, ensuring everyone leaves with a clear understanding of their tasks and commitments.",
      "checked": false
    }
  ];
  
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
      <Button sx={{marginTop:"15px",marginLeft:"10px"}} variant="contained" onClick={handleDuring}>
        
      </Button>
    </div>
  );
};

export default Meeting;
