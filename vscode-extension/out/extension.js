"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode_1 = require("vscode");
const channel_1 = require("./common/channel");
const node_1 = require("vscode-languageclient/node");
const workspace_1 = require("./common/workspace");
const hausifyLsp_1 = require("./common/hausifyLsp");
let hausifyClient = undefined;
let configListener = undefined;
async function stopLanguageClient() {
    if (hausifyClient) {
        await hausifyClient.stop();
        hausifyClient.dispose();
        hausifyClient = undefined;
        (0, channel_1.logMessage)("Hausify Python Language Server stopped");
    }
}
async function startLanguageClient() {
    const workspace = await (0, workspace_1.getProjectRoot)();
    const serverPath = (0, hausifyLsp_1.findHausifyCli)();
    if (!serverPath) {
        channel_1.outputChannel.appendLine("Could not find hausify cli");
        return;
    }
    const client = new node_1.LanguageClient("hausify", "Hausify Python Language Server", {
        command: serverPath,
        args: [
            `--root="${workspace.uri.fsPath}"`,
        ],
        options: {
            env: {
                ...process.env,
            }
        }
    }, {
        documentSelector: [
            { language: 'python' }
        ],
        outputChannel: channel_1.outputChannel
    });
    await client.start();
    return client;
}
async function handleEnabled() {
    const config = vscode_1.workspace.getConfiguration('hausify');
    const enabled = config.get('enable', true);
    if (enabled && !hausifyClient) {
        hausifyClient = await startLanguageClient();
        (0, channel_1.logMessage)("Hausify Python Language Server started (config enabled).");
    }
    else if (!enabled && hausifyClient) {
        await stopLanguageClient();
        (0, channel_1.logMessage)("Hausify Python Language Server stopped (config disabled).");
    }
}
async function activate(context) {
    (0, channel_1.logMessage)("Activating Hausify Ptyhon Language Server extension...");
    context.subscriptions.push(channel_1.outputChannel);
    configListener = vscode_1.workspace.onDidChangeConfiguration(async (e) => {
        if (e.affectsConfiguration('hausify.enable')) {
            await handleEnabled();
        }
        if (e.affectsConfiguration('hausify.lspPath')) {
            await stopLanguageClient();
            await handleEnabled();
        }
    });
    await handleEnabled();
}
function deactivate() {
    return stopLanguageClient();
}
//# sourceMappingURL=extension.js.map