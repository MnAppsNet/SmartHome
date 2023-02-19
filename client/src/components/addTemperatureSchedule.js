import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import Dialog from '@mui/material/Dialog';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { Box } from '@mui/material';

export default function AddTemperatureSchedule(props) {
  const [timeValue, setTimeValue] = React.useState(null);
  const [tempValue, setTempValue] = React.useState(20);
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleSave = () => {
    if (timeValue != null) {
      props.onSave(String(timeValue.$H).padStart(2, '0') + ":" + String(timeValue.$m).padStart(2, '0'),tempValue);
    }
    setOpen(false);
  };
  return (
    <Box sx={props.sx}>
      <Button fullWidth variant="outlined" onClick={handleClickOpen} sx={{color:'text.secondary'}}>
        Add New Temperature Schedule
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
              Add New Temperature Schedule
            </Typography>
          </Toolbar>
        </AppBar>
        <br />
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Box sx={{display: 'flex'}}>
          <TextField label="Temperature"
                     variant="outlined"
                     type="number"
                     inputProps={{step:"0.1", min: 0, max: 30}}
                     onChange={(newTempValue) => setTempValue(newTempValue.target.value)}
                     value={tempValue}/>
          <TimePicker
            ampm={false}
            label="Pick Time"
            value={timeValue}
            onChange={(newTimeValue) => {
              setTimeValue(newTimeValue);
            }}
            renderInput={(params) => <TextField {...params} />}
          />
          </Box>
        </LocalizationProvider>
        <Button autoFocus color="inherit" onClick={handleSave}>Add</Button>
      </Dialog>
    </Box>
  );
}