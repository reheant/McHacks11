import * as React from 'react';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import logo from "../logo.png";

export default function ButtonAppBar() {
  const theme = createTheme({
    palette: {
      mode: 'light',  
          },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1,  boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.7)", }}>
        <AppBar position="static" color="primary">  
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center', fontFamily: 'Nunito' }}>
              <a href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                <img src={logo} alt="Logo" style={{ height: '100px' }} /> 
              </a>
            </Typography>
          </Toolbar>
        </AppBar>
      </Box>
    </ThemeProvider>
  );
}