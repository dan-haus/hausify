
import {window, LogOutputChannel, OutputChannel } from "vscode";

export const logChannel: LogOutputChannel = window.createOutputChannel("Hausify Python Language Server Logs", { log: true });
export const outputChannel: OutputChannel = window.createOutputChannel("Hausify Python Language Server Output");

outputChannel.appendLine("Hausify Python Language Server Output Channel Initialized");
outputChannel.show();

export function logInfo(message: string): void {
    logChannel.info(message);
}

export function logWarning(message: string): void {
    logChannel.warn(message);
}

export function logError(message: string): void {
    logChannel.error(message);
}

export function logMessage(message: string): void {
    logChannel.appendLine(message);
}