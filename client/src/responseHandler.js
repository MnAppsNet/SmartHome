import Const from './const'
export default class responseHandler {
    constructor(state, commands, results) {
        this.commands = commands;
        this.results = results;
        this.state = state;
    }

    processResponse() {
        if (!this._checkResults()) {
            this.state.showAlert(Const.Messages.invalidResponse, Const.Status.error);
            return;
        }
        if (this.results[Const.Response.status] !== Const.Status.success) {
            this.state.showAlert(this.results[Const.Response.message], this.results[Const.Response.status]);
        }
        if (this.results[Const.Response.status] === Const.Status.error) {
            return;
        }
        for (let command in this.commands) {
            command = this.commands[command];
            let type = '';
            //Get command type
            if (typeof command === 'string' || command instanceof String)
                type = this._getCommandType(command);
            else
                for (let c in command) {
                    type = this._getCommandType(c);
                    break;
                }

            switch (type) {
                case "get": this._processGetCommand(command); break;
                //case "set":
                case "do": this._processDoCommand(command); break;
                default: break;
            }
        }
    }

    _checkResults() {
        //Check if response contains the mandatory parameters
        for (let item in Const.Response) {
            if (item.startsWith("_")) continue;
            if (!(item in this.results)) return false;
        }
        return true;
    }

    _processDoCommand(command) {
        if (typeof command === 'object') {
            command = Object.keys(command)[0]
        }
        const result = this.results.data[command];
        this.state.showAlert(result, Const.Status.information)
    }

    _processGetCommand(command) {
        if (typeof command === 'object') {
            command = Object.keys(command)[0]
        }
        const variable = command.slice(3);
        if (variable in this.state.data)
            this.state.data[variable].set(this.results.data[command]);
    }

    _getCommandType(command) {
        if (command.startsWith("get"))
            return "get";
        else if (command.startsWith("set"))
            return "set";
        else if (command.startsWith("do"))
            return "do";
        else return null;
    }
}