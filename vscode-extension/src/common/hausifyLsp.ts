import { workspace } from 'vscode'
import { execSync} from 'child_process'
import { outputChannel, logError, logMessage } from './channel';

export function findHausifyCli(): string | undefined {
    
    const config = workspace.getConfiguration('hausify');
    const configLspPath = config.get<string>('lspPath')
    if (configLspPath && configLspPath.trim() !== "") {
        logMessage(`Using hausify LSP from configuration: ${configLspPath}`)
        return configLspPath;
    }

    try {
        const cmd = process.platform === 'win32' ? 'where hausify' : 'which hausify';
        const result = execSync(cmd, {encoding: 'utf-8'}).trim();
        const cliPath = result.split('\n')[0];
        logMessage(`Using hausify LSP from PATH: ${cliPath}`)
        return cliPath
    } catch (error) {
        logError(error)
        logError(
            "Could not find 'hausify' CLI.  Please install hausify in this environment " +
            "using 'pip install hausify' or 'pipx install hausify'"
        )
        return undefined;
    }
}