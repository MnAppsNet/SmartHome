import Const from './const'
import responseHandler from './responseHandler'
import { Agent } from 'https';

export default class requestHandler{
    constructor(state,server=null) {
        this.headers = {};
        if (this.server == null) this.server = state.server.get();
        else this.server = server
        if (!this.server.endsWith("/")) this.server += "/";
        this.commands = [];
        this.state = state; //Global state object (defined in App.js)
      }
    addCommand(command,value = null) {
        //Add command to the list of command for the server to execute
        if (value != null){
            const action = {};
            action[command] = value;
            this.commands.push(action);
        } else
            this.commands.push(command);
    }
    addHeader(header,value){
        //Add a header to the request that will be sent to the server
        this.headers[header] = value;
    }
    sendCommands() {
        //Send the gathered commands to the server and handle the response
        if (this.commands.length === 0)
            return true;
        const request = {};
        request[Const.Request.actions] = this.commands;
        this.addHeader('Content-Type','application/json');
        const requestOptions = {
            method: Const.Request.postMethod,
            headers: this.headers,
            body: JSON.stringify(request),
            agent: new Agent({
                rejectUnauthorized: false
             })};
        const commandsCopy = JSON.parse(JSON.stringify(this.commands))
        this.state.setLoading(true);
        const url = this.server + Const.Commands.path;
        fetch(url, requestOptions)
            .then((response) => {
                if (response.ok)
                    response.json().then( (responseData) => this._handleResponse(commandsCopy,responseData));
                else{
                    this._handleError(response.statusText);
                }
            })
            .catch((error) => {this._handleError(error)});
        this.commands = [];
        this.headers = {};
        return true;
    }
    _handleError(error){
        this.state.showAlert(error,Const.Status.error);
        this.state.setLoading(false);
    }
    _handleResponse(commands,responseData) {
        this.state.setLoading(false);
        const respHandler = new responseHandler(this.state,commands,responseData);
        respHandler.processResponse();
    }
}