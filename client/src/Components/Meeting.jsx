import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import '../css/Meeting.css';

const Meeting = () => {
  const location = useLocation();
  const { extractedText } = location.state || {};
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    if (extractedText) {
      const parsedSubjects = parseSubjects(extractedText);
      setSubjects(parsedSubjects);
    }
  }, [extractedText]);

  const parseSubjects = (extractedText) => {
    const subjectRegex = /(\d+)\.\s*\*\*(.*?)\*\*\s*\n\s*-\s*Description:\s*([^]+?)(?=\n\d+\.|\n\n|$)/g;
    const subjects = [];
    let match;
    while ((match = subjectRegex.exec(extractedText)) !== null) {
      const [_, number, title, description] = match;
      subjects.push({ number, title, description });
    }
    return subjects;
  };

  return (
    <div>
      <h1>Meeting Minutes</h1>
      {subjects.map((subject, index) => (
        <Accordion key={index}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls={`panel${index}-content`} id={`panel${index}-header`}>
            {subject.number}. {subject.title}
          </AccordionSummary>
          <AccordionDetails>
            <p>{subject.description}</p>
          </AccordionDetails>
        </Accordion>
      ))}
    </div>
  );
};

export default Meeting;
