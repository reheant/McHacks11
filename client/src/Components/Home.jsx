import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
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
  Stack,
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import RemoveCircleOutlineIcon from "@mui/icons-material/RemoveCircleOutline";
import AnimatedText from "./AnimatedText";

const TeamForm = () => {
  const [teamLeader, setTeamLeader] = useState("");
  const [newUser, setNewUser] = useState("");
  const [users, setUsers] = useState([]);

  const navigate = useNavigate();

  const handleTeamLeaderChange = (event) => {
    setTeamLeader(event.target.value);
  };

  const handleNewUserChange = (event) => {
    setNewUser(event.target.value);
  };

  const addUser = () => {
    if (newUser) {
      setUsers([...users, newUser]);
      setNewUser("");
    }
  };

  const deleteUser = (index) => {
    const updatedUsers = users.filter((_, i) => i !== index);
    setUsers(updatedUsers);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const teamData = {
      teamLeader: teamLeader,
      users: [teamLeader, ...users],
    };
    console.log("Team Data:", teamData);
    navigate("/Initialization", { state: teamData });
  };

  return (
    <>
      <Stack
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
         
          
        }}
      >
        <h1>
          <AnimatedText
            text="Welcome to Minute Handler"
            animationClassName="letter-animation"
          />
        </h1>
        <Box sx={{width:"41%"}}> <h5 style={{

          justifyContent: "center",
          alignItems: "center",}}>  <AnimatedText
            text="Revolutionize your meetings with the Meeting Handler App, your all-in-one solution for creatingagendas,  capturing real-time updates, and generating concise meeting summaries, perfect for educators and businesses seeking seamless meeting management."
            animationClassName="letter-animation"
          /></h5></Box>
       
      </Stack>
      <Box sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '500px', maxHeight: "1000px"}}>
        <Container maxWidth="sm">
          <Paper sx={{ padding: "20px", marginTop: "20px", boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.3)' }}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12}>
                  <TextField
                    label="Team Leader"
                    value={teamLeader}
                    onChange={handleTeamLeaderChange}
                    margin="normal"
                    fullWidth
                  />
                </Grid>
                <Grid item xs={9}>
                  <TextField
                    label="Add User"
                    value={newUser}
                    onChange={handleNewUserChange}
                    margin="normal"
                    fullWidth
                  />
                </Grid>
                <Grid item xs={3}>
                  <IconButton onClick={addUser} color="primary">
                    <AddCircleOutlineIcon />
                  </IconButton>
                </Grid>
                <Grid item xs={12}>
                  <List>
                    {users.map((user, index) => (
                      <ListItem
                        key={index}
                        secondaryAction={
                          <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => deleteUser(index)}
                          >
                            <RemoveCircleOutlineIcon color="secondary" />
                          </IconButton>
                        }
                      >
                        <ListItemText primary={user} />
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