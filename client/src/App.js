import React from 'react';
import Login from './components/login'
import Dashboard from './components/dashboard'
import { useState, useEffect } from 'react';
import Typography from "@material-ui/core/Typography";
import { CssBaseline } from '@material-ui/core';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import DeviceInfo from 'react-native-device-info';

const VERSION = '0.0.1'

const Copyright = (props) => {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © SmartHome '}
      { new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme();


const App = () => {

  const [sessionID, setSessionID] = useState(null);
  const [userAgent, setUserAgent] = useState(null);

  useEffect(()=>{
    const init = async () =>{
      const deviceID = await DeviceInfo.getUniqueId()
      setUserAgent("SmartHomeClient/" + VERSION + " " + deviceID)}
    init();
  },[])

  const State = {
    sessionID : {
      set: setSessionID,
      get: sessionID
    },
    userAgent : {
      set: setUserAgent,
      get: userAgent
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
      <div className="App">
        { sessionID == null  && <Login state={State}/> }
        { sessionID == null  && <Dashboard state={State}/> }
      </div>
      <Copyright sx={{ mt: 8, mb: 4 }} />
    </ThemeProvider>
  );
}

export default App;
