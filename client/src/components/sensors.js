
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import DeviceThermostatIcon from '@mui/icons-material/DeviceThermostat';
import Divider from '@mui/material/Divider';
import Const from '../const'

const Sensors = (props) => {
    const State = props.state
    let sensors = State.data.Sensors.get()
    let sensorItems = []
    Object.keys(sensors).map((s, _) => {
        if (!(Const.Sensor.temperature in sensors[s])) sensors[s][Const.Sensor.temperature] = 0;
        if (!(Const.Sensor.humidity in sensors[s])) sensors[s][Const.Sensor.humidity] = 0;
        let name = s;
        if (!('.' in name)) name = "GPIO_" + name
        if (Const.Sensor.name in sensors[s]) name += " - " + sensors[s][Const.Sensor.name]
        sensorItems.push(
        <ListItem>
            <ListItemAvatar>
                <DeviceThermostatIcon fontSize='large' sx={{color:"green"}} />
            </ListItemAvatar>
            <ListItemText primary={name} secondary={"Temperature: "+(Math.round(sensors[s]["temperature"]*100)/100).toFixed(2)+" °C | Humidity: "+(Math.round(sensors[s]["humidity"]*100)/100).toFixed(2)+" %"} />
            <Divider/>
        </ListItem>);
    });
    return (
        <List sx={{ width: '100%', height:'150px', bgcolor: 'background.paper', overflowX: "hidden", overflowY: "scroll", '&::-webkit-scrollbar': {width: '0'} }}>
          {sensorItems}
        </List>
      );
}

export default Sensors;