/**
 * Enhanced Error Handler for Holographic Memory Operations
 * Provides comprehensive error handling, logging, and user feedback
 */

import * as vscode from 'vscode';

export interface ErrorContext {
    operation: string;
    component: 'extension' | 'python-bridge' | 'indexer' | 'memory-system';
    severity: 'error' | 'warning' | 'info';
    recoverable: boolean;
    userMessage?: string;
    technicalDetails?: string;
    suggestedActions?: string[];
}

export class ErrorHandler {
    private outputChannel: vscode.OutputChannel;
    private errorLog: Array<{timestamp: Date; context: ErrorContext; error: Error}> = [];

    constructor(outputChannel: vscode.OutputChannel) {
        this.outputChannel = outputChannel;
    }

    /**
     * Handle errors with context and user-friendly messaging
     */
    async handleError(error: Error, context: ErrorContext): Promise<void> {
        // Log the error
        this.logError(error, context);
        
        // Store in error log
        this.errorLog.push({
            timestamp: new Date(),
            context,
            error
        });

        // Show user-appropriate message
        await this.showUserMessage(error, context);
    }

    /**
     * Handle Python bridge connection errors
     */
    async handlePythonBridgeError(error: Error): Promise<void> {
        const context: ErrorContext = {
            operation: 'python-bridge-connection',
            component: 'python-bridge',
            severity: 'error',
            recoverable: true,
            userMessage: 'Failed to connect to Python backend',
            technicalDetails: error.message,
            suggestedActions: [
                'Check Python installation',
                'Verify Python path in settings',
                'Check if required packages are installed',
                'Restart VS Code'
            ]
        };

        await this.handleError(error, context);
    }

    /**
     * Handle indexing operation errors
     */
    async handleIndexingError(error: Error, details?: any): Promise<void> {
        const context: ErrorContext = {
            operation: 'workspace-indexing',
            component: 'indexer',
            severity: 'error',
            recoverable: true,
            userMessage: 'Failed to index workspace for annotations',
            technicalDetails: `${error.message}${details ? `\nDetails: ${JSON.stringify(details, null, 2)}` : ''}`,
            suggestedActions: [
                'Check workspace permissions',
                'Verify Python files are accessible',
                'Try indexing a smaller directory first',
                'Check Output panel for detailed logs'
            ]
        };

        await this.handleError(error, context);
    }

    /**
     * Handle memory system errors
     */
    async handleMemorySystemError(error: Error, operation: string): Promise<void> {
        const context: ErrorContext = {
            operation,
            component: 'memory-system',
            severity: 'error',
            recoverable: false,
            userMessage: 'Memory system operation failed',
            technicalDetails: error.message,
            suggestedActions: [
                'Check memory system configuration',
                'Verify required dependencies are installed',
                'Restart the Python backend',
                'Check system resources'
            ]
        };

        await this.handleError(error, context);
    }

    /**
     * Handle file system errors
     */
    async handleFileSystemError(error: Error, filePath?: string): Promise<void> {
        const context: ErrorContext = {
            operation: 'file-system-access',
            component: 'extension',
            severity: 'error',
            recoverable: true,
            userMessage: `Failed to access ${filePath ? `file: ${filePath}` : 'file system'}`,
            technicalDetails: error.message,
            suggestedActions: [
                'Check file/directory permissions',
                'Verify the file exists',
                'Check disk space',
                'Try with a different file'
            ]
        };

        await this.handleError(error, context);
    }

    /**
     * Handle JSON parsing errors
     */
    async handleJsonError(error: Error, data?: string): Promise<void> {
        const context: ErrorContext = {
            operation: 'json-parsing',
            component: 'extension',
            severity: 'error',
            recoverable: true,
            userMessage: 'Failed to parse response data',
            technicalDetails: `${error.message}${data ? `\nData: ${data.substring(0, 200)}...` : ''}`,
            suggestedActions: [
                'Check Python backend output',
                'Verify communication protocol',
                'Restart the Python bridge',
                'Check for corrupted data'
            ]
        };

        await this.handleError(error, context);
    }

    /**
     * Show warning messages to user
     */
    async showWarning(message: string, details?: string, actions?: string[]): Promise<void> {
        const context: ErrorContext = {
            operation: 'user-warning',
            component: 'extension',
            severity: 'warning',
            recoverable: true,
            userMessage: message,
            technicalDetails: details,
            suggestedActions: actions
        };

        await this.handleError(new Error(message), context);
    }

    /**
     * Show info messages to user
     */
    async showInfo(message: string, details?: string): Promise<void> {
        const context: ErrorContext = {
            operation: 'user-info',
            component: 'extension',
            severity: 'info',
            recoverable: true,
            userMessage: message,
            technicalDetails: details
        };

        await this.handleError(new Error(message), context);
    }

    /**
     * Get error statistics
     */
    getErrorStats(): {
        total: number;
        byComponent: Record<string, number>;
        bySeverity: Record<string, number>;
        recent: Array<{timestamp: Date; operation: string; message: string}>;
    } {
        const byComponent: Record<string, number> = {};
        const bySeverity: Record<string, number> = {};
        
        this.errorLog.forEach(entry => {
            byComponent[entry.context.component] = (byComponent[entry.context.component] || 0) + 1;
            bySeverity[entry.context.severity] = (bySeverity[entry.context.severity] || 0) + 1;
        });

        const recent = this.errorLog
            .slice(-10)
            .map(entry => ({
                timestamp: entry.timestamp,
                operation: entry.context.operation,
                message: entry.error.message
            }));

        return {
            total: this.errorLog.length,
            byComponent,
            bySeverity,
            recent
        };
    }

    /**
     * Clear error log
     */
    clearErrorLog(): void {
        this.errorLog = [];
        this.outputChannel.appendLine('Error log cleared');
    }

    /**
     * Export error log for debugging
     */
    async exportErrorLog(): Promise<void> {
        const content = JSON.stringify({
            timestamp: new Date().toISOString(),
            errors: this.errorLog.map(entry => ({
                timestamp: entry.timestamp.toISOString(),
                context: entry.context,
                error: {
                    name: entry.error.name,
                    message: entry.error.message,
                    stack: entry.error.stack
                }
            }))
        }, null, 2);

        const doc = await vscode.workspace.openTextDocument({
            content,
            language: 'json'
        });

        await vscode.window.showTextDocument(doc);
    }

    /**
     * Log error to output channel
     */
    private logError(error: Error, context: ErrorContext): void {
        const timestamp = new Date().toISOString();
        const severity = context.severity.toUpperCase();
        
        this.outputChannel.appendLine(`[${timestamp}] ${severity}: ${context.operation}`);
        this.outputChannel.appendLine(`Component: ${context.component}`);
        this.outputChannel.appendLine(`Message: ${error.message}`);
        
        if (context.technicalDetails) {
            this.outputChannel.appendLine(`Details: ${context.technicalDetails}`);
        }
        
        if (error.stack) {
            this.outputChannel.appendLine(`Stack: ${error.stack}`);
        }
        
        this.outputChannel.appendLine('---');
    }

    /**
     * Show appropriate user message based on context
     */
    private async showUserMessage(error: Error, context: ErrorContext): Promise<void> {
        const message = context.userMessage || error.message;
        const actions = ['View Details', 'Open Log'];
        
        if (context.suggestedActions && context.suggestedActions.length > 0) {
            actions.unshift('Show Solutions');
        }

        let selectedAction: string | undefined;

        switch (context.severity) {
            case 'error':
                selectedAction = await vscode.window.showErrorMessage(message, ...actions);
                break;
            case 'warning':
                selectedAction = await vscode.window.showWarningMessage(message, ...actions);
                break;
            case 'info':
                selectedAction = await vscode.window.showInformationMessage(message, ...actions);
                break;
        }

        await this.handleUserAction(selectedAction, error, context);
    }

    /**
     * Handle user's response to error message
     */
    private async handleUserAction(action: string | undefined, error: Error, context: ErrorContext): Promise<void> {
        switch (action) {
            case 'Show Solutions':
                await this.showSolutions(context);
                break;
            case 'View Details':
                await this.showErrorDetails(error, context);
                break;
            case 'Open Log':
                this.outputChannel.show();
                break;
        }
    }

    /**
     * Show suggested solutions
     */
    private async showSolutions(context: ErrorContext): Promise<void> {
        if (!context.suggestedActions || context.suggestedActions.length === 0) {
            return;
        }

        const content = `# 🔧 Troubleshooting: ${context.operation}

## Problem
${context.userMessage}

## Suggested Solutions

${context.suggestedActions.map((action, i) => `${i + 1}. ${action}`).join('\n')}

## Technical Details
${context.technicalDetails || 'No additional details available.'}

## Component
- **Component**: ${context.component}
- **Severity**: ${context.severity}
- **Recoverable**: ${context.recoverable ? 'Yes' : 'No'}

---
*Generated by Holographic Memory Error Handler*
`;

        const doc = await vscode.workspace.openTextDocument({
            content,
            language: 'markdown'
        });

        await vscode.window.showTextDocument(doc, {
            viewColumn: vscode.ViewColumn.Beside,
            preview: true
        });
    }

    /**
     * Show detailed error information
     */
    private async showErrorDetails(error: Error, context: ErrorContext): Promise<void> {
        const content = `# ❌ Error Details: ${context.operation}

## Error Information
- **Name**: ${error.name}
- **Message**: ${error.message}
- **Component**: ${context.component}
- **Severity**: ${context.severity}
- **Recoverable**: ${context.recoverable ? 'Yes' : 'No'}

## Technical Details
\`\`\`
${context.technicalDetails || 'No additional details available.'}
\`\`\`

## Stack Trace
\`\`\`
${error.stack || 'No stack trace available.'}
\`\`\`

## Timestamp
${new Date().toISOString()}

---
*Generated by Holographic Memory Error Handler*
`;

        const doc = await vscode.workspace.openTextDocument({
            content,
            language: 'markdown'
        });

        await vscode.window.showTextDocument(doc, {
            viewColumn: vscode.ViewColumn.Beside,
            preview: true
        });
    }
}