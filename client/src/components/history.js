
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import StateOnIcon from '@mui/icons-material/LocalFireDepartment';
import StateOffIcon from '@mui/icons-material/InvertColorsOff';
import Divider from '@mui/material/Divider';

const Log = (props) =>{
    const log = props.log
    const stateText = (log.state)?"ON":"OFF"
    const temp = (Math.round(parseFloat(log.temp) * 100) / 100).toFixed(2)
    const reqTemp = (Math.round(parseFloat(log.req_temp) * 100) / 100).toFixed(2)
    const logText = "State: " + stateText + " | Temperature: " + temp + " *C | Required: " + reqTemp
    return(
        <ListItem>
            <ListItemAvatar>
                {(log.state == true) &&
                    <StateOnIcon fontSize='large' sx={{color:"green"}} />
                }
                {(log.state == false) &&
                    <StateOffIcon fontSize='large' sx={{color:"red"}} />
                }
            </ListItemAvatar>
            <ListItemText primary={logText} secondary={log.time} />
          </ListItem>
    )
}

const History = (props) => {
    const State = props.state
    let logs = State.data.StateLogs.get()
    let logItems = []
    for (let i = 0; i < logs.length; i++) {
        logItems.push(<Log log={logs[i]} />);
    }
    logItems = logItems.reverse()
    return (
        <List sx={{ width: '100%', height:'150px', bgcolor: 'background.paper', overflowX: "hidden", overflowY: "scroll", '&::-webkit-scrollbar': {width: '0'} }}>
          {logItems}
          <Divider/>
        </List>
      );
}

export default History;