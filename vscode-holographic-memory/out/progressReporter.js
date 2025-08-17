"use strict";
/**
 * Enhanced Progress Reporter for Holographic Memory Operations
 * Provides detailed progress tracking and error handling for indexing operations
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
exports.ProgressReporter = void 0;
const vscode = __importStar(require("vscode"));
class ProgressReporter {
    constructor() {
        this.outputChannel = vscode.window.createOutputChannel('Holographic Memory');
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    }
    /**
     * Show enhanced progress with detailed status updates
     */
    async withDetailedProgress(title, operation) {
        return vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title,
            cancellable: true
        }, async (progress, token) => {
            // Show in status bar
            this.statusBarItem.text = `$(sync~spin) ${title}`;
            this.statusBarItem.show();
            try {
                const result = await operation(progress);
                // Success status
                this.statusBarItem.text = `$(check) Indexing Complete`;
                setTimeout(() => this.statusBarItem.hide(), 3000);
                return result;
            }
            catch (error) {
                // Error status
                this.statusBarItem.text = `$(error) Indexing Failed`;
                setTimeout(() => this.statusBarItem.hide(), 5000);
                throw error;
            }
        });
    }
    /**
     * Show indexing results with rich formatting
     */
    async showIndexingResults(result) {
        if (!result.success) {
            await this.showIndexingErrors(result);
            return;
        }
        // Show success notification
        const message = `✅ Found ${result.total_annotations} annotations in ${result.files_with_annotations} files. Created ${result.created_capsules?.length || 0} capsules.`;
        const action = await vscode.window.showInformationMessage(message, 'View Details', 'Show Annotations', 'Open Log');
        switch (action) {
            case 'View Details':
                await this.showDetailedResults(result);
                break;
            case 'Show Annotations':
                await this.showAnnotationsSummary(result);
                break;
            case 'Open Log':
                this.outputChannel.show();
                break;
        }
    }
    /**
     * Show detailed results in a formatted document
     */
    async showDetailedResults(result) {
        const content = this.formatDetailedResults(result);
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
     * Show annotations summary in a user-friendly format
     */
    async showAnnotationsSummary(result) {
        const content = this.formatAnnotationsSummary(result);
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
     * Show indexing errors with actionable information
     */
    async showIndexingErrors(result) {
        const errors = result.errors || [];
        const warnings = result.warnings || [];
        let message = '❌ Indexing failed';
        if (errors.length > 0) {
            message += ` with ${errors.length} error(s)`;
        }
        if (warnings.length > 0) {
            message += ` and ${warnings.length} warning(s)`;
        }
        const action = await vscode.window.showErrorMessage(message, 'View Errors', 'Open Log', 'Retry');
        switch (action) {
            case 'View Errors':
                await this.showErrorDetails(result);
                break;
            case 'Open Log':
                this.outputChannel.show();
                break;
            case 'Retry':
                // Trigger retry (would need to be handled by caller)
                vscode.commands.executeCommand('holographicMemory.indexWorkspace');
                break;
        }
    }
    /**
     * Show error details in a formatted document
     */
    async showErrorDetails(result) {
        const content = this.formatErrorDetails(result);
        const doc = await vscode.workspace.openTextDocument({
            content,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);
    }
    /**
     * Log detailed information to output channel
     */
    logIndexingOperation(result) {
        this.outputChannel.appendLine('='.repeat(60));
        this.outputChannel.appendLine(`Holographic Memory Indexing - ${new Date().toISOString()}`);
        this.outputChannel.appendLine('='.repeat(60));
        if (result.success) {
            this.outputChannel.appendLine(`✅ SUCCESS`);
            this.outputChannel.appendLine(`📊 Statistics:`);
            this.outputChannel.appendLine(`   - Files scanned: ${result.files_scanned}`);
            this.outputChannel.appendLine(`   - Files with annotations: ${result.files_with_annotations}`);
            this.outputChannel.appendLine(`   - Total annotations: ${result.total_annotations}`);
            this.outputChannel.appendLine(`   - Capsules created: ${result.created_capsules?.length || 0}`);
            if (result.duration_ms) {
                this.outputChannel.appendLine(`   - Duration: ${result.duration_ms}ms`);
            }
        }
        else {
            this.outputChannel.appendLine(`❌ FAILED`);
            if (result.errors) {
                this.outputChannel.appendLine(`🚨 Errors (${result.errors.length}):`);
                result.errors.forEach((error, i) => {
                    this.outputChannel.appendLine(`   ${i + 1}. ${error}`);
                });
            }
            if (result.warnings) {
                this.outputChannel.appendLine(`⚠️ Warnings (${result.warnings.length}):`);
                result.warnings.forEach((warning, i) => {
                    this.outputChannel.appendLine(`   ${i + 1}. ${warning}`);
                });
            }
        }
        this.outputChannel.appendLine('');
    }
    /**
     * Format detailed results for display
     */
    formatDetailedResults(result) {
        const duration = result.duration_ms ? ` (${result.duration_ms}ms)` : '';
        return `# 🧠 Holographic Memory Indexing Results${duration}

## 📊 Summary
- **Files Scanned**: ${result.files_scanned.toLocaleString()}
- **Files with Annotations**: ${result.files_with_annotations}
- **Total Annotations Found**: ${result.total_annotations}
- **Memory Capsules Created**: ${result.created_capsules?.length || 0}

## 💾 Created Capsules

${result.created_capsules?.map((capsule, i) => `
### ${i + 1}. \`${capsule.capsule_id}\`
- **File**: \`${capsule.file}\`
- **Line**: ${capsule.line}
- **Slots**: ${JSON.stringify(capsule.slots, null, 2)}
`).join('') || 'No capsules created.'}

## 📁 Files with Annotations

${Object.entries(result.annotations_by_file || {}).map(([file, annotations]) => `
### \`${file}\`
- **Annotations**: ${annotations.length}
${annotations.map((ann, i) => `  ${i + 1}. \`${ann.capsule_id}\` (${ann.annotation_type}) - Line ${ann.line_start}`).join('\n')}
`).join('')}

---
*Generated by Holographic Memory System*
`;
    }
    /**
     * Format annotations summary for display
     */
    formatAnnotationsSummary(result) {
        const annotationsByType = {};
        // Group annotations by type
        Object.values(result.annotations_by_file || {}).flat().forEach((ann) => {
            const type = ann.annotation_type || 'unknown';
            if (!annotationsByType[type]) {
                annotationsByType[type] = [];
            }
            annotationsByType[type].push(ann);
        });
        return `# 🏷️ Holographic Memory Annotations Summary

## 📊 Overview
- **Total Annotations**: ${result.total_annotations}
- **Annotation Types**: ${Object.keys(annotationsByType).length}
- **Files**: ${result.files_with_annotations}

## 📋 By Annotation Type

${Object.entries(annotationsByType).map(([type, annotations]) => `
### ${type.charAt(0).toUpperCase() + type.slice(1)} Annotations (${annotations.length})

${annotations.map((ann, i) => `
#### ${i + 1}. \`${ann.capsule_id}\`
- **File**: \`${ann.file_path}\`
- **Lines**: ${ann.line_start}-${ann.line_end}
- **Slots**: ${Object.keys(ann.slots).length > 0 ? JSON.stringify(ann.slots, null, 2) : 'None'}
- **Weights**: ${Object.keys(ann.weights).length > 0 ? JSON.stringify(ann.weights, null, 2) : 'None'}
- **Meta**: ${Object.keys(ann.meta).length > 0 ? JSON.stringify(ann.meta, null, 2) : 'None'}
`).join('')}
`).join('')}

---
*Generated by Holographic Memory System*
`;
    }
    /**
     * Format error details for display
     */
    formatErrorDetails(result) {
        return `# ❌ Holographic Memory Indexing Errors

## 🚨 Errors (${result.errors?.length || 0})

${result.errors?.map((error, i) => `
### ${i + 1}. Error
\`\`\`
${error}
\`\`\`
`).join('') || 'No errors recorded.'}

## ⚠️ Warnings (${result.warnings?.length || 0})

${result.warnings?.map((warning, i) => `
### ${i + 1}. Warning
\`\`\`
${warning}
\`\`\`
`).join('') || 'No warnings recorded.'}

## 🔧 Troubleshooting

### Common Issues:
1. **File encoding errors**: Some files may have non-UTF-8 encoding
2. **Permission errors**: Check file/directory permissions
3. **Syntax errors**: Malformed annotations in Python files
4. **Memory errors**: Large workspaces may require more memory

### Solutions:
- Check the Output panel for detailed logs
- Verify Python files have proper encoding
- Ensure workspace is accessible
- Try indexing smaller directories first

---
*Generated by Holographic Memory System*
`;
    }
    dispose() {
        this.outputChannel.dispose();
        this.statusBarItem.dispose();
    }
}
exports.ProgressReporter = ProgressReporter;
//# sourceMappingURL=progressReporter.js.map