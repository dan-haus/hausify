"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findHausifyCli = findHausifyCli;
const vscode_1 = require("vscode");
const child_process_1 = require("child_process");
const channel_1 = require("./channel");
function findHausifyCli() {
    const config = vscode_1.workspace.getConfiguration('hausify');
    const configLspPath = config.get('lspPath');
    if (configLspPath && configLspPath.trim() !== "") {
        (0, channel_1.logMessage)(`Using hausify LSP from configuration: ${configLspPath}`);
        return configLspPath;
    }
    try {
        const cmd = process.platform === 'win32' ? 'where hausify' : 'which hausify';
        const result = (0, child_process_1.execSync)(cmd, { encoding: 'utf-8' }).trim();
        const cliPath = result.split('\n')[0];
        (0, channel_1.logMessage)(`Using hausify LSP from PATH: ${cliPath}`);
        return cliPath;
    }
    catch (error) {
        (0, channel_1.logError)(error);
        (0, channel_1.logError)("Could not find 'hausify' CLI.  Please install hausify in this environment " +
            "using 'pip install hausify' or 'pipx install hausify'");
        return undefined;
    }
}
//# sourceMappingURL=hausifyLsp.js.map