
import { PythonExtension, ResolvedEnvironment} from "@vscode/python-extension";

import { logError } from "./channel";


let pythonApi: PythonExtension | undefined = undefined;
let environment: ResolvedEnvironment | undefined = undefined;

export async function getPythonExtension(): Promise<PythonExtension | undefined> {
    if (pythonApi) {
        return pythonApi;
    }

    try {
        pythonApi = await PythonExtension.api();
    } catch (error) {
        logError("Failed to get Python extension API: " + error);
        return undefined;
    }

    if (!pythonApi) {
        logError("Python extension is not available. Please ensure it is installed and enabled.");
    }

    return pythonApi;
}

export async function getPythonEnvironment(): Promise<ResolvedEnvironment | undefined> {
    if (environment) {
        return environment;
    }

    const pythonApi = await getPythonExtension();
    if (!pythonApi) {
        return undefined;
    }

    environment = await pythonApi.environments.resolveEnvironment(
        pythonApi.environments.getActiveEnvironmentPath()
    );

    return environment;
}

