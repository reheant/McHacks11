import React, { useState } from "react";
import {
  Container,
  TextField,
  Button,
  IconButton,
  List,
  ListItem,
  Box,
  ListItemText,
  Grid,
  Paper,
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import RemoveCircleOutlineIcon from "@mui/icons-material/RemoveCircleOutline";
import AnimatedText from './AnimatedText';


const TeamForm = () => {
  const [scrumMaster, setScrumMaster] = useState("");
  const [newDeveloper, setNewDeveloper] = useState("");
  const [developers, setDevelopers] = useState([]);

  const handleScrumMasterChange = (event) => {
    setScrumMaster(event.target.value);
  };

  const handleNewDeveloperChange = (event) => {
    setNewDeveloper(event.target.value);
  };

  const addDeveloper = () => {
    if (newDeveloper) {
      setDevelopers([...developers, newDeveloper]);
      setNewDeveloper(""); // Reset the input field
    }
  };

  const deleteDeveloper = (index) => {
    const updatedDevelopers = developers.filter((_, i) => i !== index);
    setDevelopers(updatedDevelopers);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, probably send to your server
    console.log("Scrum Master:", scrumMaster);
    console.log("Developers:", developers);
  };

  return (
    <>
    <Box sx={{display: 'flex', justifyContent: 'center', alignItems: 'center',height:'100px'}}> <h1><AnimatedText text="Welcome to My App" animationClassName="letter-animation" /></h1></Box>
    <Box sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '600px', maxHeight:"1000px"}}>
    <Container maxWidth="sm">
      
      <Paper sx={{ padding: "20px", marginTop: "20px",boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.3)'}}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12}>
              <TextField
                label="Scrum Master"
                value={scrumMaster}
                onChange={handleScrumMasterChange}
                margin="normal"
                fullWidth
              />
            </Grid>
            <Grid item xs={9}>
              <TextField
                label="Add Developer"
                value={newDeveloper}
                onChange={handleNewDeveloperChange}
                margin="normal"
                fullWidth
              />
            </Grid>
            <Grid item xs={3}>
              <IconButton onClick={addDeveloper} color="primary">
                <AddCircleOutlineIcon />
              </IconButton>
            </Grid>
            <Grid item xs={12}>
              <List>
                {developers.map((developer, index) => (
                  <ListItem
                    key={index}
                    secondaryAction={
                      <IconButton
                        edge="end"
                        aria-label="delete"
                        onClick={() => deleteDeveloper(index)}
                      >
                        <RemoveCircleOutlineIcon color="secondary" />
                      </IconButton>
                    }
                  >
                    <ListItemText primary={developer} />
                  </ListItem>
                ))}
              </List>
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Submit
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
    </Box>
    </>
  );
};

export default TeamForm;
