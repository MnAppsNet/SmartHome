import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import ListItemText from '@mui/material/ListItemText';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import SettingsIcon from '@mui/icons-material/Settings';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import AddTemperatureSchedule from './addTemperatureSchedule';
import AddSensor from './addSensor';
import InputAdornment from '@mui/material/InputAdornment';
import TextField from '@mui/material/TextField';
import requestHandler from '../requestHandler'
import Const from '../const'

const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

export default function Settings(props) {

    const State = props.state
    let reqHandler = new requestHandler(State);

    const [, updateState] = React.useState();
    const forceUpdate = React.useCallback(() => updateState({}), []);

    const [open, setOpen] = useState(false);
    const [schedule, setSchedule] = useState({});
    const [sensors, setSensors] = useState([]);
    const [refreshRate,setRefreshRate] = useState(60);
    const [tempOffset,setTempOffset] = useState(0.5);

    useEffect(() => {
        if (reqHandler != null) return;
        reqHandler = new requestHandler(State);
    }, [])

    const addNewSchedule = (time, temp) => {
        const newSchedule = schedule;
        newSchedule[time] = temp;
        setSchedule(newSchedule);
        forceUpdate();
    }

    const handleClickOpen = () => {
        const scheduleCopy = JSON.parse(JSON.stringify(State.data.Schedule.get()));
        if (scheduleCopy != null) { setSchedule(scheduleCopy); }
        else setSchedule({});
        const s = State.data.Sensors.get();
        if (s != null) { setSensors(s); }
        else setSensors({});
        setRefreshRate(State.data.RefreshRate.get())
        setTempOffset(State.data.TemperatureOffset.get())
        setOpen(true);
        forceUpdate();
    };
    const handleClose = () => {
        setOpen(false);
    };
    const handleSave = () => {
        saveTemperatureSchedule();
        saveSensorData();
        reqHandler.sendCommands();
        setOpen(false);
    };
    const saveTemperatureSchedule = () => {
        State.data.Schedule.set(schedule);
        State.data.RefreshRate.set(refreshRate);
        State.data.TemperatureOffset.set(tempOffset);
        reqHandler.addCommand(Const.Commands.setSchedule, schedule);
        reqHandler.addCommand(Const.Commands.setRefreshRate, refreshRate);
        reqHandler.addCommand(Const.Commands.setTemperatureOffset, tempOffset);
        reqHandler.addCommand(Const.Commands.doSave);
    }
    const saveSensorData = () => {
        reqHandler.addCommand(Const.Commands.setSensorData, sensors);
        reqHandler.addCommand(Const.Commands.getSensorData);
    }
    const deleteFromTemperatureSchedule = (time) => {
        const newSchedule = schedule;
        try {
            delete newSchedule[time]
            setSchedule(newSchedule);
        } catch { }
        forceUpdate();
    }
    const makeSensorPrimary = (sensor,id) => {
        if (!(Const.Sensor.name in sensor)) sensor[Const.Sensor.name] = "";
        if (!(Const.Sensor.temperatureOffset in sensor)) sensor[Const.Sensor.temperatureOffset] = 0;
        if (!(Const.Sensor.humidityOffset in sensor)) sensor[Const.Sensor.humidityOffset] = 0;
        if (!(Const.Sensor.delete in sensor)) sensor[Const.Sensor.delete] = false;
        if (!(Const.Sensor.primary in sensor)) sensor[Const.Sensor.primary] = false;
        sensor[Const.Sensor.primary] = true;
        addSensor(id,sensor[Const.Sensor.name],sensor[Const.Sensor.temperatureOffset],sensor[Const.Sensor.humidityOffset],sensor[Const.Sensor.delete],sensor[Const.Sensor.primary]);
        forceUpdate();
    }
    const deleteSensor = (sensor,id) => {
        if (!(Const.Sensor.name in sensor)) sensor[Const.Sensor.name] = "";
        if (!(Const.Sensor.temperatureOffset in sensor)) sensor[Const.Sensor.temperatureOffset] = 0;
        if (!(Const.Sensor.humidityOffset in sensor)) sensor[Const.Sensor.humidityOffset] = 0;
        if (!(Const.Sensor.delete in sensor)) sensor[Const.Sensor.delete] = false;
        if (!(Const.Sensor.primary in sensor)) sensor[Const.Sensor.primary] = false;
        sensor[Const.Sensor.delete] = true;
        addSensor(id,sensor[Const.Sensor.name],sensor[Const.Sensor.temperatureOffset],sensor[Const.Sensor.humidityOffset],sensor[Const.Sensor.delete],sensor[Const.Sensor.primary]);
        forceUpdate();
    }
    const addSensor = (id,name,tempOffset,humidOffset,deleted=null,primary=null) => {
        const tmpSensors = sensors;
        if (!(id in tmpSensors)) tmpSensors[id] = {};
        tmpSensors[id][Const.Sensor.name] = name;
        tmpSensors[id][Const.Sensor.temperatureOffset] = tempOffset;
        tmpSensors[id][Const.Sensor.humidityOffset] = humidOffset;
        if (deleted === null)
            if (Const.Sensor.delete in sensors[id])
                tmpSensors[id][Const.Sensor.delete] = sensors[id][Const.Sensor.delete]
        else tmpSensors[id][Const.Sensor.delete] = deleted;
        if (primary === null){
            if (Const.Sensor.primary in sensors[id])
                tmpSensors[id][Const.Sensor.primary] = sensors[id][Const.Sensor.primary];
        }
        else {
            tmpSensors[id][Const.Sensor.primary] = primary;
            if (primary)
            Object.keys(tmpSensors).map((s, _) => {
                if (s !== id) 
                    tmpSensors[s][Const.Sensor.primary] = false;
            });
        };
        setSensors(tmpSensors);
        forceUpdate();
    }

    return (
        <Box>
            <Button sx={props.sx} variant="outlined" onClick={handleClickOpen}>
                <SettingsIcon />
            </Button>
            <Dialog
                fullScreen
                open={open}
                onClose={handleClose}
                TransitionComponent={Transition}>
                <AppBar sx={{ position: 'relative' }}>
                    <Toolbar>
                        <IconButton
                            edge="start"
                            color="inherit"
                            onClick={handleClose}
                            aria-label="close"
                        >
                            <CloseIcon />
                        </IconButton>
                        <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
                            Settings
                        </Typography>
                        <Button autoFocus color="inherit" onClick={handleSave}>
                            save
                        </Button>
                    </Toolbar>
                </AppBar>
                <Box sx={{ paddingTop: '20px', paddingBottom: '5px' }}>
                    <Typography sx={{ backgroundColor: 'background.secondary', textAlign: 'center' }} variant="h5" component="div">
                        Temperature Schedule
                    </Typography>
                    <List sx={{ outlineStyle: 'solid', height: '20vh', overflowY: 'scroll' }}>
                        {
                            Object.keys(schedule).map((time, index) => {
                                return (
                                    <ListItem key={"sh."+index} >
                                        <ListItemText primary={"Scheduled time : " + time} secondary={"Required Temperature : " + schedule[time]} />
                                        <IconButton onClick={() => deleteFromTemperatureSchedule(time)}><DeleteIcon sx={{ color: 'red' }} /></IconButton>
                                    </ListItem>
                                );
                            })
                        }
                    </List>
                    <AddTemperatureSchedule onSave={addNewSchedule} />
                </Box>
                <Divider />
                <Box sx={{ paddingTop: '20px', paddingBottom: '5px' }}>
                    <Typography sx={{ backgroundColor: 'background.secondary', textAlign: 'center' }} variant="h5" component="div">
                        Sensors List
                    </Typography>
                    <List sx={{ outlineStyle: 'solid', height: '20vh', overflowY: 'scroll' }}>
                        {
                            Object.keys(sensors).map((s, index) => {
                                let deleted = false;
                                let primary = false;
                                let sensor = {};
                                sensor[s] = sensors[s];
                                let name = String(s);
                                if (!(name.includes('.'))) name = "GPIO_" + name
                                if (Const.Sensor.name in sensors[s]) name += " - " + sensors[s][Const.Sensor.name]
                                if ("delete" in sensor[s]) deleted = sensor[s]["delete"];
                                if ("primary" in sensor[s]) primary = sensor[s]["primary"];
                                if (!deleted)
                                    return (
                                        <ListItem key={"se."+index} >
                                            <ListItemText primary={name}
                                                        secondary={"Temperature Offset : " + sensor[s]["temperatureOffset"] + " | " + "Humidity Offset : " + sensor[s]["humidityOffset"]} />
                                            {!primary && <IconButton onClick={() => makeSensorPrimary(sensor[s],s)}><CheckCircleOutlineIcon sx={{ color: 'blue' }} /></IconButton> }
                                            <AddSensor onSave={addSensor} sensor={sensor} state={State} />
                                            {!primary && <IconButton onClick={() => deleteSensor(sensor[s],s)}><DeleteIcon sx={{ color: 'red' }} /></IconButton> }
                                        </ListItem> );
                            })
                        }
                    </List>
                    <AddSensor onSave={addSensor} state={State} />
                </Box>
                <Divider />
                <Box sx={{ paddingTop: '5px', paddingBottom: '5px'}}>
                    <Typography sx={{ backgroundColor: 'background.secondary', textAlign: 'center' }} variant="h5" component="div">
                        Other Settings
                    </Typography><br/>
                    <Box sx={{width:'100%', display:'flex' ,justifyContent: 'center'}}>
                    <TextField
                        variant="outlined"
                        label="Refresh Rate"
                        type="number"
                        value={refreshRate}
                        onChange={(newValue)=>setRefreshRate(newValue.target.value)}
                        sx={{width:"250px", paddingRight:"2px", paddingLeft:"2px"}}
                        inputProps={{step:1, min: 5, max: 3600}}
                        InputProps={{
                            endAdornment: <InputAdornment position="end">Sec</InputAdornment>
                        }} />
                    <TextField
                        variant="outlined"
                        label="Temperature Offset"
                        type="number"
                        value={tempOffset}
                        onChange={(newValue)=>setTempOffset(newValue.target.value)}
                        sx={{width:"250px", paddingRight:"2px", paddingLeft:"2px"}}
                        inputProps={{step:0.1, min: 0.1, max: 10}}
                        InputProps={{
                            endAdornment: <InputAdornment position="end">°C</InputAdornment>
                        }} />
                    </Box>
                </Box>
                <Divider />
            </Dialog>
        </Box>
    );
}