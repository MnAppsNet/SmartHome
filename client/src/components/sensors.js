
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import SensorsIcon from '@mui/icons-material/Sensors';
import SensorsOffIcon from '@mui/icons-material/SensorsOff';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import Divider from '@mui/material/Divider';
import Const from '../const'

const Sensors = (props) => {
    const State = props.state
    let sensors = State.data.Sensors.get()
    let sensorItems = []
    Object.keys(sensors).map((s, _) => {
        if (!(Const.Sensor.temperature in sensors[s])) sensors[s][Const.Sensor.temperature] = 0;
        if (!(Const.Sensor.humidity in sensors[s])) sensors[s][Const.Sensor.humidity] = 0;
        if (!(Const.Sensor.offline in sensors[s])) sensors[s][Const.Sensor.offline] = false
        if (!(Const.Sensor.primary in sensors[s])) sensors[s][Const.Sensor.primary] = false
        let name = String(s);
        if (!(name.includes('.'))) name = "GPIO_" + name
        if (Const.Sensor.name in sensors[s]) name += " - " + sensors[s][Const.Sensor.name]
        if (sensors[s][Const.Sensor.primary]) name += " ☆"
        sensorItems.push(
        <ListItem>
            <ListItemAvatar>
                {!sensors[s][Const.Sensor.offline] && <SensorsIcon fontSize='large' sx={{color:"green"}} />}
                {sensors[s][Const.Sensor.offline] && <SensorsOffIcon fontSize='large' sx={{color:"red"}} />}
            </ListItemAvatar>
            <ListItemText primary={name} secondary={"Temperature: "+(Math.round(sensors[s]["temperature"]*100)/100).toFixed(2)+" °C | Humidity: "+(Math.round(sensors[s]["humidity"]*100)/100).toFixed(2)+" %"}/>
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