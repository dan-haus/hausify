import { ExtensionContext, Disposable, workspace } from 'vscode';
import { logMessage, logError, logInfo, outputChannel } from './common/channel';
import { LanguageClient } from 'vscode-languageclient/node';
import { getProjectRoot } from './common/workspace';
import { findHausifyCli } from './common/hausifyLsp';

let hausifyClient: LanguageClient | undefined = undefined;
let configListener: Disposable | undefined = undefined;

async function stopLanguageClient(): Promise<void> {
    if (hausifyClient) {
        await hausifyClient.stop();
        hausifyClient.dispose();
        hausifyClient = undefined;
        logMessage("Hausify Python Language Server stopped")
    }
}

async function startLanguageClient(): Promise<LanguageClient> {
    const projectRoot = await getProjectRoot();
    const serverPath = findHausifyCli();
    
    if (!serverPath) {
        outputChannel.appendLine("Could not find hausify cli")
        return
    }
    
    const config = workspace.getConfiguration('hausify');
    
    const args: string[] = []

    args.push("--root")
    args.push(projectRoot.uri.fsPath)
    
    const logPath = config.get<string>('lspLogPath')
    if (logPath !== '') {
        args.push('--log-path')
        args.push(logPath)
    }
    
    logInfo(`args: ${args}`)

    const client = new LanguageClient(
        "hausify",
        "Hausify Python Language Server",
        {
            command: serverPath,
            args: args,
            options: {
                env: {
                    ...process.env,
                }
            }
        },
        {
            documentSelector: [
                {language: 'python'}
            ],
            outputChannel: outputChannel
        }
    )

    await client.start();
    return client;

}


async function handleEnabled() {
    const config = workspace.getConfiguration('hausify');
    const enabled = config.get<boolean>('enable', true);

    if (enabled && !hausifyClient) {
        hausifyClient = await startLanguageClient();
        logMessage("Hausify Python Language Server started (config enabled).");
    } else if (!enabled && hausifyClient) {
        await stopLanguageClient();
        logMessage("Hausify Python Language Server stopped (config disabled).");
    }
}

export async function activate(context: ExtensionContext) {
    logMessage("Activating Hausify Ptyhon Language Server extension...")
    context.subscriptions.push(outputChannel)

    configListener = workspace.onDidChangeConfiguration(async (e) => {
        if (e.affectsConfiguration('hausify.enable')) {
            await handleEnabled();
        }

        if (e.affectsConfiguration('hausify.lspPath')) {
            await stopLanguageClient();
            await handleEnabled();
        }

        if (e.affectsConfiguration('hausify.lspLogPath')) {
            await stopLanguageClient();
            await handleEnabled();
        }
    })

    await handleEnabled();
}

export function deactivate(): Thenable<void> | undefined {
    return stopLanguageClient();
}