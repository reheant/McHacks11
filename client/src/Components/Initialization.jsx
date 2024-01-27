// NewPage.js
import React from 'react';
import { useLocation } from 'react-router-dom';

const NewPage = () => {
  const location = useLocation();
  const { scrumMaster, developers } = location.state || {};

  return (
    <div>
      <h2>New Page</h2>
      <p>Scrum Master: {scrumMaster}</p>
      <p>Developers:</p>
      <ul>
        {developers && developers.map((developer, index) => (
          <li key={index}>{developer}</li>
        ))}
      </ul>
    </div>
  );
};

export default NewPage;
