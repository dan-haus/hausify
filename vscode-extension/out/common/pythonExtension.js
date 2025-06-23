"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPythonExtension = getPythonExtension;
exports.getPythonEnvironment = getPythonEnvironment;
const python_extension_1 = require("@vscode/python-extension");
const channel_1 = require("./channel");
let pythonApi = undefined;
let environment = undefined;
async function getPythonExtension() {
    if (pythonApi) {
        return pythonApi;
    }
    try {
        pythonApi = await python_extension_1.PythonExtension.api();
    }
    catch (error) {
        (0, channel_1.logError)("Failed to get Python extension API: " + error);
        return undefined;
    }
    if (!pythonApi) {
        (0, channel_1.logError)("Python extension is not available. Please ensure it is installed and enabled.");
    }
    return pythonApi;
}
async function getPythonEnvironment() {
    if (environment) {
        return environment;
    }
    const pythonApi = await getPythonExtension();
    if (!pythonApi) {
        return undefined;
    }
    environment = await pythonApi.environments.resolveEnvironment(pythonApi.environments.getActiveEnvironmentPath());
    return environment;
}
//# sourceMappingURL=pythonExtension.js.map