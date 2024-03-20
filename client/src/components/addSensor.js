import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import Dialog from '@mui/material/Dialog';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { Box } from '@mui/material';
import Const from '../const'

export default function AddSensor(props) {
  const [editMode, setEditMode] = React.useState(false);
  const [id, setId] = React.useState(null);
  const [tempOffset, setTempOffset] = React.useState(0);
  const [humidOffset, setHumidOffset] = React.useState(0);
  const [name, setName] = React.useState("");
  const [open, setOpen] = React.useState(false);
  const [title,setTitle] = React.useState("Add New Sensor")

  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleSave = () => {
    if (id != null) {
      props.onSave(id,name,tempOffset,humidOffset);
    }
    setOpen(false);
  };

  if ("sensor" in props){
    Object.keys(props["sensor"]).map((s, _) => {
      if (Const.Sensor.temperatureOffset in props["sensor"][s]) setTempOffset(props["sensor"][s][Const.Sensor.temperatureOffset])
      if (Const.Sensor.humidityOffset in props["sensor"][s]) setHumidOffset(props["sensor"][s][Const.Sensor.humidityOffset])
      if (Const.Sensor.name in props["sensor"][s]) setName(props["sensor"][s][Const.Sensor.name])
      setId(s)
    });
    setEditMode(true);
    setTitle("Edit Sensor")
    delete props["sensor"];
  }
  return (
    <Box sx={props.sx}>
      <Button fullWidth variant="outlined" onClick={handleClickOpen} sx={{color:'text.secondary'}}>
        {title}
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}>
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close">
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} component="div">
              {title}
            </Typography>
          </Toolbar>
        </AppBar>
        <br />
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Box sx={{display: 'flex'}}>
          <TextField label="Sensor PIN or IP"
                     variant="outlined"
                     type="text"
                     onChange={(newId) => { 
                        if (!editMode) setId(newId.target.value)
                      }}
                     InputProps={{readOnly: editMode}}
                     value={id}/>
          <TextField label="Sensor Name"
                     variant="outlined"
                     type="text"
                     onChange={(newName) => setName(newName.target.value)}
                     value={name}/>
          <br />
          <TextField label="Temperature Offset"
                     variant="outlined"
                     type="number"
                     inputProps={{step:"0.1", min: -30, max: 30}}
                     onChange={(offset) => setTempOffset(offset.target.value)}
                     value={tempOffset}/>
          <TextField label="Humidity Offset"
                     variant="outlined"
                     type="number"
                     inputProps={{step:"0.1", min: -30, max: 30}}
                     onChange={(offset) => setHumidOffset(offset.target.value)}
                     value={humidOffset}/>
          </Box>
        </LocalizationProvider>
        <Button autoFocus color="inherit" onClick={handleSave}>Add</Button>
      </Dialog>
    </Box>
  );
}