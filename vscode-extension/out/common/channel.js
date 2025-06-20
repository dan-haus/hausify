"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.outputChannel = exports.logChannel = void 0;
exports.logInfo = logInfo;
exports.logWarning = logWarning;
exports.logError = logError;
exports.logMessage = logMessage;
const vscode_1 = require("vscode");
exports.logChannel = vscode_1.window.createOutputChannel("Hausify Python Language Server Logs", { log: true });
exports.outputChannel = vscode_1.window.createOutputChannel("Hausify Python Language Server Output");
exports.outputChannel.appendLine("Hausify Python Language Server Output Channel Initialized");
exports.outputChannel.show();
function logInfo(message) {
    exports.logChannel.info(message);
}
function logWarning(message) {
    exports.logChannel.warn(message);
}
function logError(message) {
    exports.logChannel.error(message);
}
function logMessage(message) {
    exports.logChannel.appendLine(message);
}
//# sourceMappingURL=channel.js.map