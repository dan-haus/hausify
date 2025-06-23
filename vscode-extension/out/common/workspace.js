"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectRoot = getProjectRoot;
const fs = require("fs-extra");
const path = require("path");
const vscode_1 = require("vscode");
async function getProjectRoot() {
    const workspaces = vscode_1.workspace.workspaceFolders ?? [];
    if (workspaces.length === 0) {
        return {
            uri: vscode_1.Uri.file(process.cwd()),
            name: path.basename(process.cwd()),
            index: 0
        };
    }
    if (workspaces.length === 1) {
        return workspaces[0];
    }
    let rootWorkspace = workspaces[0];
    let root = undefined;
    for (const w of workspaces) {
        if (await fs.pathExists(w.uri.fsPath) === false) {
            continue;
        }
        if (root === undefined) {
            root = w.uri.fsPath;
            rootWorkspace = w;
            continue;
        }
        if (w.uri.fsPath.length < root.length) {
            root = w.uri.fsPath;
            rootWorkspace = w;
        }
    }
    return rootWorkspace;
}
//# sourceMappingURL=workspace.js.map