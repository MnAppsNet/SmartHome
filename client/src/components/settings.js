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
import { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import AddTemperatureSchedule from './addTemperatureSchedule';
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
        setRefreshRate(State.data.RefreshRate.get())
        setTempOffset(State.data.TemperatureOffset.get())
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };
    const handleSave = () => {
        saveTemperatureSchedule();
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
        reqHandler.sendCommands();
    }
    const deleteFromTemperatureSchedule = (time) => {
        const newSchedule = schedule;
        try {
            delete newSchedule[time]
            setSchedule(newSchedule);
        } catch { }
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
                                    <ListItem key={index} >
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