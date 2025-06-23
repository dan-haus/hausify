import * as fs from 'fs-extra';
import * as path from 'path';
import { workspace, Uri, WorkspaceFolder } from 'vscode';

export async function getProjectRoot(): Promise<WorkspaceFolder> {
    const workspaces: readonly WorkspaceFolder[] = workspace.workspaceFolders ?? [];
    if (workspaces.length === 0) {
        return {
            uri: Uri.file(process.cwd()),
            name: path.basename(process.cwd()),
            index: 0
        }
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