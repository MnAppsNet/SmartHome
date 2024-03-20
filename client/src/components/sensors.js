
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import DeviceThermostatIcon from '@mui/icons-material/DeviceThermostat';

const Sensors = (props) => {
    const State = props.state
    let sensors = State.data.Sensors.get()
    let sensorItems = []
    Object.keys(sensors).map((s, _) => {
        if (!("temperature" in sensors[s])) sensors[s]["temperature"] = 0;
        if (!("humidity" in sensors[s])) sensors[s]["humidity"] = 0;
        sensorItems.push(
        <ListItem>
            <ListItemAvatar>
                <DeviceThermostatIcon fontSize='large' sx={{color:"green"}} />
            </ListItemAvatar>
            <ListItemText primary={s} secondary={"Temperature: "+sensors[s]["temperature"]+" °C | Humidity: "+sensors[s]["humidity"]+" %"} />
        </ListItem>);
    });
    return (
        <List sx={{ width: '100%', height:'150px', bgcolor: 'background.paper', overflowX: "hidden", overflowY: "scroll", '&::-webkit-scrollbar': {width: '0'} }}>
          {sensorItems}
        </List>
      );
}

export default Sensors;