// NewPage.js
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Box, List, ListItem, ListItemText, IconButton, Button, Paper, Typography, Container } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';

const NewPage = () => {
  const location = useLocation();
  const { teamLeader, users } = location.state || {};
  const [recordings, setRecordings] = useState({});

  const handleRecord = async (userName) => {
    try {
      const response = await fetch('http://localhost:5000/record_voice', { // Replace with your Flask server URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userName }), // Send the username as part of the request
      });
      const data = await response.json();
      if (data.status === 'success') {
        // Update state to indicate recording is done for this user
        setRecordings(prev => ({ ...prev, [userName]: true }));
      }
    } catch (error) {
      console.error('Error recording voice:', error);
    }
  };

  const allRecorded = users && users.every(user => recordings[user]);

  const handleStart = () => {
    // Logic to send data to backend
    console.log('Sending data to backend...');
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Team Voice Samples
        </Typography>
        <List sx={{ width: '100%' }}>
          {users && users.map((user, index) => (
            <Paper key={index} elevation={3} sx={{ mb: 2, p: 1 }}>
              <ListItem>
                <ListItemText primary={user} secondary={index === 0 ? 'Team Leader' : 'User'} />
                <IconButton onClick={() => handleRecord(user)} disabled={recordings[user]}>
                  <MicIcon />
                </IconButton>
              </ListItem>
            </Paper>
          ))}
        </List>
        <Button
          variant="contained"
          color="primary"
          onClick={handleStart}
          disabled={!allRecorded}
        >
          Start
        </Button>
      </Box>
    </Container>
  );
};

export default NewPage;
