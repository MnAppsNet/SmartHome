import React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import DeviceThermostatIcon from '@mui/icons-material/DeviceThermostat';
import WaterIcon from '@mui/icons-material/Water';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import Slider from '@mui/material/Slider';
import requestHandler from '../requestHandler'
import Const from '../const'
import History from './history'
import LeftIcon from '@mui/icons-material/ArrowLeft';
import RightIcon from '@mui/icons-material/ArrowRight';
import IconButton from '@mui/material/IconButton';
import { useEffect, useState } from 'react';

const marks = [
    {
        value: 0,
        label: '0°C',
    },
    {
        value: 10,
        label: '10°C',
    },
    {
        value: 20,
        label: '20°C',
    },
    {
        value: 30,
        label: '30°C',
    },
];

function valuetext(value) {
    return `${value}°C`;
}

const Dashboard = (props) => {

    const [dateText, setDateText] = useState("");
    const [date, setDate] = useState(new Date());

    const update_every = 30000
    const State = props.state
    let reqHandler = new requestHandler(State);
    let updateViewInterval = null;

    function changeDate(increase = null){
        if (date === null) setDate(new Date());
        if (increase === null){
            setDate(new Date());
        }
        else if (increase === true){
            const tmpDate = new Date()
            tmpDate.setDate(date.getDate() + 1)
            setDate(tmpDate);
        }
        else if (increase === false){
            const tmpDate = new Date()
            tmpDate.setDate(date.getDate() - 1)
            setDate(tmpDate);
        }
    }

    function updateView(){
        //if (State.sessionID.get() == null || State.sessionID.get() == "" || State.sessionID.get() == "null") {
        //    clearInterval(updateViewInterval);
        //    return;
        //}
        reqHandler.addCommand(Const.Commands.getCurrentTemperature);
        reqHandler.addCommand(Const.Commands.getCurrentHumidity);
        reqHandler.addCommand(Const.Commands.getLastUpdate);
        reqHandler.addCommand(Const.Commands.getRequiredTemperature);
        reqHandler.addCommand(Const.Commands.getThermostatState);
        reqHandler.addCommand(Const.Commands.getStateLogs,
            { "year": date.getFullYear() , "month": date.getMonth()+1, "day":date.getDate()}
            );
        reqHandler.sendCommands();
    }

    useEffect(()=>{
        if (reqHandler != null) return;
        reqHandler = new requestHandler(State);
        changeDate();
        if (updateViewInterval == null)
            updateViewInterval = setInterval(updateView, update_every)
      },[])

    useEffect(()=>{
        setDateText(date.getDate()+'.'+(date.getMonth()+1)+'.'+date.getFullYear());
        updateView();
    },[date])

    return (
        <Container component="main" maxWidth="xm" sx={{ paddingTop: '5vh' }}>
            <CssBaseline />
            <Grid container style={{ padding: '10px', margin: 'auto' }}>
                <Grid key='lastUpdate' xs={8} style={{ padding: '2px' }}>
                    <Item title='Last Update'>
                        <Typography variant='h5'><AccessTimeIcon /> {State.data.LastUpdate.get()}</Typography>
                    </Item>
                </Grid>
                <Grid key='state' xs={4} style={{ padding: '2px' }}>
                    <Item title="Thermostat">
                        {State.data.ThermostatState.get() && <Typography variant='h5' style={{color:'green'}}>ON</Typography>}
                        {!State.data.ThermostatState.get() && <Typography variant='h5' style={{color:'red'}}>OFF</Typography>}
                    </Item>
                </Grid>
                <Grid key='temperature' xs={6} style={{ padding: '2px' }}>
                    <Item title='Temperature'>
                        <Typography variant='h5'><DeviceThermostatIcon /> {(Math.round(State.data.CurrentTemperature.get() * 100) / 100).toFixed(2)} °C</Typography>
                    </Item>
                </Grid>
                <Grid key='humidity' xs={6} style={{ padding: '2px' }}>
                    <Item title='Humidity'>
                        <Typography variant='h5'><WaterIcon /> {(Math.round(State.data.CurrentHumidity.get() * 100) / 100).toFixed(2)} %</Typography>
                    </Item>
                </Grid>
                <Grid key='requiredTemperature' xs={12} style={{ padding: '2px' }}>
                    <Item title={'Required Temperature : ' + State.data.RequiredTemperature.get() + ' °C'}>
                        <Slider
                            color="secondary"
                            getAriaLabel={() => 'Temperature'}
                            getAriaValueText={valuetext}
                            value={State.data.RequiredTemperature.get()}
                            valueLabelDisplay="always"
                            onChange={(event,value) => {State.data.RequiredTemperature.set(value)}}
                            onChangeCommitted={(event,value) => {State.data.RequiredTemperature.send(value);}}
                            max={30}
                            min={-10}
                            step={0.1}
                            marks={marks} />
                    </Item>
                </Grid>
                <Grid key='stateLogs' xs={12} style={{ padding: '2px' }}>
                    <Item title={
                        <div style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap'}}>
                            {'History'}
                            <IconButton color="secondary" onClick={()=>changeDate(false)}><LeftIcon fontSize='large'/></IconButton>
                            <Typography sx={{cursor: "pointer"}} onClick={()=>changeDate(null)}>{dateText}</Typography>
                            <IconButton color="secondary" onClick={()=>changeDate(true)}><RightIcon fontSize='large'/></IconButton>
                        </div>
                        }>
                        <History state={State} />
                    </Item>
                </Grid>
            </Grid>
        </Container>
    );
}

const Item = (props) => {
    return (
        <Card>
            <Typography variant='subtitle1' style={{ padding: '5px' }}>{props.title} {props.extra}</Typography>
            <Divider />
            <CardContent>
                {props.children}
            </CardContent>
        </Card>
    );
}


export default Dashboard