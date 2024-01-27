import * as React from 'react';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export default function ButtonAppBar() {
  const theme = createTheme({
    palette: {
      mode: 'dark', 
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center', fontFamily: 'Nunito' }}>
              Minute Handler
            </Typography>
          </Toolbar>
        </AppBar>
      </Box>
    </ThemeProvider>
  );
}