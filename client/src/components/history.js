
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import StateOnIcon from '@mui/icons-material/LocalFireDepartment';
import StateOffIcon from '@mui/icons-material/InvertColorsOff';
import WorkIcon from '@mui/icons-material/Work';
import BeachAccessIcon from '@mui/icons-material/BeachAccess';

const Log = (props) =>{
    const log = props.log
    const stateText = (log.state)?"ON":"OFF"
    const logText = "State: " + stateText + " | Temperature: " + log.temp + " *C | Required: " + log.req_temp
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
    return (
        <List sx={{ width: '100%', height:'150px', bgcolor: 'background.paper', overflowX: "hidden", overflowY: "scroll", '&::-webkit-scrollbar': {width: '0'} }}>
          {logItems}
        </List>
      );
}

export default History;