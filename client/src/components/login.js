import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import HouseIcon from '@mui/icons-material/House';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import sha256 from 'crypto-js/sha256';

 const Login = (props) => {

  const State = props.state

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const username = data.get('username')
    const password = sha256(data.get('password'));
    const loginToken = "Basic " + btoa(username+":"+password)

    const request = {
      actions : "getSessionID"
    }
    const requestOptions = {
      method: 'POST',
      headers: { 'User-Agent': State.userAgent.get, 'Authorization': loginToken },
      body: JSON.stringify(request)
    };
    fetch('https://localhost:6969', requestOptions)
        .then(
          response => {
            console.log(response.headers);
            response.json().then(
              (data) => {
                debugger;
              });});
  };

  return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <HouseIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            SmartHome
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Login
            </Button>
          </Box>
        </Box>
      </Container>
  );
}

export default Login