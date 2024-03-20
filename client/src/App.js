import React from 'react';
import Dashboard from './components/dashboard'
import { useState } from 'react';
import Typography from "@material-ui/core/Typography";
import { CssBaseline } from '@material-ui/core';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Alert from '@mui/material/Alert';
import LinearProgress from '@mui/material/LinearProgress';
import Const from './const';
import Settings from './components/settings';
import Sensors from './components/sensors';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import ThermostatIcon from '@mui/icons-material/Thermostat';
//import Login from './components/login'
//import {v4} from "uuid";
//import sha256 from 'crypto-js/sha256';
//import {getDevice,getUniqueId} from 'react-native-device-info';

import requestHandler from './requestHandler';

//const VERSION = '0.0.1'

const Copyright = (props) => {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © SmartHome '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme({
  '&::-webkit-scrollbar': { width: '0' },
  palette: {
    mode: 'dark',
    primary: {
      main: '#de7b75',
    },
    secondary: {
      main: '#de7b75',
    },
    background: {
      default: "#C38D9E",
      paper: '#C1EDF0',
      secondary: '#98E1E6'
    },
    text: {
      primary: '#1f7a80',
      secondary: '#80251F',
      disabled: '#030c0d'
    },
    divider: {
      backgroundColor: '#030c0d',
    }
  },
});


const App = () => {

  const [server, setServer] = useState("/");
  //const [localSessionID, setLocalSessionID] = useState(null);
  const [alertType, setAlertType] = useState(null);
  const [alertMessage, setAlertMessage] = useState("");
  const [loading, setLoading] = useState(false);

  //Data:
  const [currentTemperature, setCurrentTemperature] = useState(0);
  const [requiredTemperature, setRequiredTemperature] = useState(20);
  const [currentHumidity, setCurrentHumidity] = useState(0);
  const [thermostatState, setThermostatState] = useState(false);
  const [refreshRate, setRefreshRate] = useState(0);
  const [temperatureOffset, setTemperatureOffset] = useState(0.5);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [stateLogs, setStateLogs] = useState({});
  const [schedule, setSchedule] = useState({});
  const [sensors, setSensors] = useState({});

  function setAlert(message, status) {
    setAlertMessage(String(message));
    switch (status) {
      case Const.Status.error: setAlertType('error'); break;
      case Const.Status.success: setAlertType('success'); break;
      case Const.Status.warning: setAlertType('warning'); break;
      case Const.Status.information: setAlertType('info'); break;
      default: setAlertType('error'); break;
    }
  }

  function sendRequiredTemperature() {
    const reqHandler = new requestHandler(State);
    reqHandler.addCommand(Const.Commands.setRequiredTemperature, requiredTemperature);
    reqHandler.addCommand(Const.Commands.getRequiredTemperature);
    reqHandler.sendCommands();
  }

  const State = {
    setLoading: (value) => setLoading(value),
    showAlert: (message,status) => setAlert(message,status),
    //deviceID: {get:()=>localSessionID},
    server: {
      set: (value) => setServer(value),
      get: () => server
    },
    data: {
      LastUpdate: { get: () => lastUpdate, set: (value) => setLastUpdate(value) },
      TemperatureOffset: { get: () => temperatureOffset, set: (value) => setTemperatureOffset(value) },
      RefreshRate: { get: () => refreshRate, set: (value) => setRefreshRate(value) },
      ThermostatState: { get: () => thermostatState, set: (value) => setThermostatState(value) },
      CurrentHumidity: { get: () => currentHumidity, set: (value) => setCurrentHumidity(value) },
      RequiredTemperature: { get: () => requiredTemperature, set: (value) => setRequiredTemperature(value), send: sendRequiredTemperature },
      CurrentTemperature: { get: () => currentTemperature, set: (value) => setCurrentTemperature(value) },
      StateLogs: { get: () => stateLogs, set: (value) => setStateLogs(value) },
      Schedule: { get: () => schedule, set: (value) => setSchedule(value) },
      Sensors: { get: () => sensors, set: (value) => setSensors(value) }
    }
  }

  //useEffect(()=>{
  //  //setServer(localStorage.getItem(Const.Session.server))
  //  setLocalSessionID(localStorage.getItem(Const.Session.localSessionID));
  // },[])
  //useEffect(()=>{
  //  if (server == "https://localhost:6969") return;
  //  localStorage.setItem(Const.Session.server,server);
  //},[server])
  //useEffect(()=>{
  //  let id = localStorage.getItem(Const.Session.localSessionID);
  //  if (id == null){
  //    id = "SmartHomeClient/" + VERSION + " " + sha256(v4());
  //    localStorage.setItem(Const.Session.localSessionID,id);
  //    setLocalSessionID(id);
  //  }
  //},[localSessionID])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
      <AppBar sx={{ position: 'fixed', height: 'fit-content' }}>
        <Toolbar>
          <ThermostatIcon />
          <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
            SmartThermostat
          </Typography>

          <Settings sx={{ position:'absolute', right: '10px', top:'10px'}} state={State} />
        </Toolbar>
        {alertType != null && alertMessage != null && <Alert  severity={alertType} onClick={() => setAlertType(null)}>{alertMessage}</Alert>}
      </AppBar>
        <div style={{ height: '2pt' }}>
          {loading === true && <LinearProgress sx={{ height: '2pt', }} color='secondary' />}
        </div>
        <Dashboard state={State} />
      </div>
      <Copyright sx={{ mt: 8, mb: 4 }} />
    </ThemeProvider>
  );
}

export default App;