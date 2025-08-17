"use strict";
/**
 * Enhanced Error Handler for Holographic Memory Operations
 * Provides comprehensive error handling, logging, and user feedback
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorHandler = void 0;
const vscode = __importStar(require("vscode"));
class ErrorHandler {
    constructor(outputChannel) {
        this.errorLog = [];
        this.outputChannel = outputChannel;
    }
    /**
     * Handle errors with context and user-friendly messaging
     */
    async handleError(error, context) {
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
    async handlePythonBridgeError(error) {
        const context = {
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
    async handleIndexingError(error, details) {
        const context = {
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
    async handleMemorySystemError(error, operation) {
        const context = {
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
    async handleFileSystemError(error, filePath) {
        const context = {
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
    async handleJsonError(error, data) {
        const context = {
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
    async showWarning(message, details, actions) {
        const context = {
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
    async showInfo(message, details) {
        const context = {
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
    getErrorStats() {
        const byComponent = {};
        const bySeverity = {};
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
    clearErrorLog() {
        this.errorLog = [];
        this.outputChannel.appendLine('Error log cleared');
    }
    /**
     * Export error log for debugging
     */
    async exportErrorLog() {
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
    logError(error, context) {
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
    async showUserMessage(error, context) {
        const message = context.userMessage || error.message;
        const actions = ['View Details', 'Open Log'];
        if (context.suggestedActions && context.suggestedActions.length > 0) {
            actions.unshift('Show Solutions');
        }
        let selectedAction;
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
    async handleUserAction(action, error, context) {
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
    async showSolutions(context) {
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
    async showErrorDetails(error, context) {
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
exports.ErrorHandler = ErrorHandler;
//# sourceMappingURL=errorHandler.js.map