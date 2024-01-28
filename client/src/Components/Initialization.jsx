import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Modal, Box, List, ListItem, ListItemText, IconButton, Button, Paper, Typography, Container, Input } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

const NewPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { users } = location.state || {};
  const [recordings, setRecordings] = useState({});
  const [pdfFile, setPdfFile] = useState(null);

  const handleRecord = async (userName) => {
    try {
      const response = await fetch('http://localhost:5000/Initialization', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userName }),
      });
      const data = await response.json();
      if (data.status === 'success') {
        setRecordings(prev => ({ ...prev, [userName]: true }));
      }
    } catch (error) {
      console.error('Error recording voice:', error);
    }
  };

  const allRecorded = users && users.every(user => recordings[user]);

  const handleClose = () => setOpen(false);
  const handleStart = () => {
    setOpen(true);
    console.log('Sending data to backend...');
  };
  const handleFileChange = (event) => {
    setPdfFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) {
      console.error('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', pdfFile);

    try {
      const response = await fetch('http://localhost:5000/upload_pdf', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (response.ok) {
        console.log("Extracted text:", data.extracted_text);
        navigate('/Meeting', { state: { extractedText: data.extracted_text } });
      } else {
        console.error("Error in response:", data.error);
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
    }
  };

  const [open, setOpen] = useState(false);

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
          Next
        </Button>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Upload PDF File
            </Typography>
            <Input
              type="file"
              onChange={handleFileChange}
              accept="application/pdf"
              sx={{ mt: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              disabled={!pdfFile}
              sx={{ mt: 2 }}
            >
              Upload and Continue to Meeting
            </Button>
          </Box>
        </Modal>
      </Box>
    </Container>
  );
};

export default NewPage;
