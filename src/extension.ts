import * as vscode from 'vscode';
import { PythonBridge } from './pythonBridge';
import { HoloGraphPanel } from './graphPanel';
import { MemoryTreeProvider } from './treeProvider';
import { MemoryTreeProvider as HoloTreeProvider } from './treeData';
import { ProgressReporter, IndexingResult } from './progressReporter';
import { ErrorHandler } from './errorHandler';

// This method is called when the extension is activated
export function activate(context: vscode.ExtensionContext) {
    console.log('Activating Holographic Memory extension');
    
    // Create enhanced components
    const outputChannel = vscode.window.createOutputChannel('Holographic Memory');
    const progressReporter = new ProgressReporter();
    const errorHandler = new ErrorHandler(outputChannel);
    
    // Create the Python bridge
    const bridge = new PythonBridge(context.extensionPath);
    
    // Create tree view providers
    const treeProvider = new MemoryTreeProvider(bridge);
    const holoTreeProvider = new HoloTreeProvider(bridge);
    vscode.window.registerTreeDataProvider('holographicMemoryExplorer', treeProvider);
    vscode.window.registerTreeDataProvider('holoMemoryExplorer', holoTreeProvider);
    
    // Add to disposables
    context.subscriptions.push(outputChannel, progressReporter);
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('holographicMemory.openGraph', () => {
            HoloGraphPanel.createOrShow(context.extensionUri, bridge);
        }),
        
        vscode.commands.registerCommand('holographicMemory.newCapsule', async () => {
            const whatInput = await vscode.window.showInputBox({
                prompt: 'Enter content for WHAT role (required)'
            });

            if (!whatInput) return;

            const whereInput = await vscode.window.showInputBox({
                prompt: 'Enter content for WHERE role (optional)'
            });

            const whenInput = await vscode.window.showInputBox({
                prompt: 'Enter content for WHEN role (optional)'
            });
            
            const bindings: Record<string, string> = {
                'WHAT': whatInput
            };
                
            if (whereInput) bindings['WHERE'] = whereInput;
            if (whenInput) bindings['WHEN'] = whenInput;

            try {
                    await bridge.ensureRunning();
                const result = await bridge.rpc('create_capsule', { bindings });
                    
                if (result.success) {
                    vscode.window.showInformationMessage('Memory capsule created successfully');
                    treeProvider.refresh();

                    // Update graph view if open
                    HoloGraphPanel.currentPanel?.postMessage({
                        type: 'capsuleCreated',
                        data: result.capsule
                    });
                } else {
                    vscode.window.showErrorMessage('Failed to create memory capsule');
                }
            } catch (err) {
                vscode.window.showErrorMessage(`Error creating capsule: ${err}`);
            }
        }),
        
        vscode.commands.registerCommand('holographicMemory.queryCapsule', async () => {
            const queryInput = await vscode.window.showInputBox({
                prompt: 'Enter query as JSON: {"WHAT":"concept","WHERE":"location"}',
                validateInput: (input: string) => {
                    try {
                        JSON.parse(input);
                        return null;
                    } catch (e) {
                        return 'Invalid JSON format';
                    }
                }
            });
            
            if (!queryInput) return;

            try {
                const query = JSON.parse(queryInput);

                await bridge.ensureRunning();
                const results = await bridge.rpc('query_capsules', { query });
                
                // Open graph panel if not already open
                if (!HoloGraphPanel.currentPanel) {
                    await vscode.commands.executeCommand('holographicMemory.openGraph');

                    // Short delay to allow panel to initialize
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

                // Send results to graph panel
                HoloGraphPanel.currentPanel?.postMessage({
                    type: 'queryResults',
                    data: results
                });

                vscode.window.showInformationMessage(`Found ${results.length} matching memory capsules`);
            } catch (err) {
                vscode.window.showErrorMessage(`Error querying capsules: ${err}`);
            }
        }),
        
        vscode.commands.registerCommand('holographicMemory.explainWithLLM', async () => {
            const options = ['Explain selected capsule', 'Analyze entire memory system'];
            const selection = await vscode.window.showQuickPick(options, {
                placeHolder: 'Choose explanation type'
            });

            if (!selection) return;

            try {
                await bridge.ensureRunning();
                const result = await bridge.rpc('explain_with_llm', {
                    action: selection,
                    capsuleId: null // Will be filled in by the Python bridge if needed
                });

                // Create and show document with explanation
                const doc = await vscode.workspace.openTextDocument({
                    content: result.explanation,
                    language: 'markdown'
                });

                await vscode.window.showTextDocument(doc);
            } catch (err) {
                vscode.window.showErrorMessage(`Error generating explanation: ${err}`);
}
        }),

        vscode.commands.registerCommand('holographicMemory.refresh', () => {
            treeProvider.refresh();
            vscode.window.showInformationMessage('Memory explorer refreshed');
        }),

        vscode.commands.registerCommand('holographicMemory.indexWorkspace', async () => {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                await errorHandler.showWarning('No workspace folder open', 'Please open a workspace folder to index annotations.');
                return;
            }

            try {
                const startTime = Date.now();
                
                const result = await progressReporter.withDetailedProgress(
                    "Indexing workspace for holographic annotations",
                    async (progress) => {
                        progress.report({ increment: 10, message: "Initializing Python bridge..." });
                        
                        try {
                            await bridge.ensureRunning();
                        } catch (err) {
                            await errorHandler.handlePythonBridgeError(err as Error);
                            throw err;
                        }
                        
                        progress.report({ increment: 30, message: "Scanning workspace files..." });
                        
                        const rpcResult = await bridge.rpc('index_workspace', { 
                            workspace_path: workspaceFolder.uri.fsPath 
                        });
                        
                        progress.report({ increment: 80, message: "Processing annotations..." });
                        
                        if (rpcResult.error) {
                            throw new Error(rpcResult.error);
                        }
                        
                        progress.report({ increment: 100, message: "Indexing complete!" });
                        
                        return rpcResult;
                    }
                );

                // Add timing information
                const duration = Date.now() - startTime;
                const indexingResult: IndexingResult = {
                    ...result,
                    success: !result.error,
                    duration_ms: duration
                };

                // Log the operation
                progressReporter.logIndexingOperation(indexingResult);
                
                // Show results
                await progressReporter.showIndexingResults(indexingResult);
                
                // Refresh tree view to show new capsules
                treeProvider.refresh();
                
            } catch (err) {
                await errorHandler.handleIndexingError(err as Error);
            }
        }),

        vscode.commands.registerCommand('holographicMemory.showAnnotations', async () => {
            try {
                await bridge.ensureRunning();
                const annotations = await bridge.rpc('get_indexed_annotations', {});
                
                if (annotations.length === 0) {
                    await errorHandler.showInfo(
                        'No annotations found', 
                        'Run "Index Workspace" first to scan for holographic memory annotations.'
                    );
                    return;
                }
                
                // Create enhanced annotations summary
                const result: IndexingResult = {
                    success: true,
                    total_annotations: annotations.length,
                    files_scanned: 0,
                    files_with_annotations: new Set(annotations.map((ann: any) => ann.file_path)).size,
                    created_capsules: [],
                    annotations_by_file: annotations.reduce((acc: any, ann: any) => {
                        const file = ann.file_path;
                        if (!acc[file]) acc[file] = [];
                        acc[file].push(ann);
                        return acc;
                    }, {})
                };
                
                await progressReporter.showIndexingResults(result);
                
            } catch (err) {
                await errorHandler.handleError(err as Error, {
                    operation: 'show-annotations',
                    component: 'extension',
                    severity: 'error',
                    recoverable: true,
                    userMessage: 'Failed to retrieve annotations',
                    suggestedActions: [
                        'Check if workspace has been indexed',
                        'Try running "Index Workspace" first',
                        'Check Python bridge connection'
                    ]
                });
            }
        }),

        // Add new diagnostic commands
        vscode.commands.registerCommand('holographicMemory.showErrorStats', async () => {
            const stats = errorHandler.getErrorStats();
            const content = `# 📊 Holographic Memory Error Statistics

## Summary
- **Total Errors**: ${stats.total}
- **Components**: ${Object.keys(stats.byComponent).length}
- **Severity Levels**: ${Object.keys(stats.bySeverity).length}

## By Component
${Object.entries(stats.byComponent).map(([component, count]) => `- **${component}**: ${count}`).join('\n')}

## By Severity
${Object.entries(stats.bySeverity).map(([severity, count]) => `- **${severity}**: ${count}`).join('\n')}

## Recent Errors (Last 10)
${stats.recent.map((error, i) => `${i + 1}. **${error.operation}** (${error.timestamp.toLocaleString()}): ${error.message}`).join('\n')}

---
*Generated by Holographic Memory Error Handler*
`;

            const doc = await vscode.workspace.openTextDocument({
                content,
                language: 'markdown'
            });
            
            await vscode.window.showTextDocument(doc);
        }),

        vscode.commands.registerCommand('holographicMemory.exportErrorLog', async () => {
            await errorHandler.exportErrorLog();
        }),

        vscode.commands.registerCommand('holographicMemory.clearErrorLog', () => {
            errorHandler.clearErrorLog();
            vscode.window.showInformationMessage('Error log cleared');
        }),

        // Go to Definition command for capsules
        vscode.commands.registerCommand('holographicMemory.goToDefinition', async (source: any) => {
            if (!source || !source.file) {
                await errorHandler.showWarning('No source information available', 'This capsule does not have source location data.');
                return;
            }

            try {
                const uri = vscode.Uri.file(source.file);
                const document = await vscode.workspace.openTextDocument(uri);
                const editor = await vscode.window.showTextDocument(document);

                // Navigate to the specific line
                const lineStart = Math.max(0, (source.lineStart || 1) - 1); // Convert to 0-based
                const lineEnd = Math.max(lineStart, (source.lineEnd || source.lineStart || 1) - 1);
                
                const range = new vscode.Range(
                    new vscode.Position(lineStart, 0),
                    new vscode.Position(lineEnd, 0)
                );

                // Select the range and reveal it
                editor.selection = new vscode.Selection(range.start, range.end);
                editor.revealRange(range, vscode.TextEditorRevealType.InCenter);

                // Show a brief message
                vscode.window.setStatusBarMessage(
                    `📍 Jumped to ${source.style} annotation at line ${source.lineStart}`,
                    3000
                );

            } catch (err) {
                await errorHandler.handleFileSystemError(err as Error, source.file);
            }
        }),

        // Explain Capsule with real Ollama integration
        vscode.commands.registerCommand('holographicMemory.explainCapsule', async (capsuleId?: string) => {
            if (!capsuleId) {
                capsuleId = await vscode.window.showInputBox({
                    prompt: 'Enter capsule ID to explain',
                    placeHolder: 'e.g., cap-42'
                });
                
                if (!capsuleId) return;
            }

            try {
                await bridge.ensureRunning();
                
                const result = await progressReporter.withDetailedProgress(
                    "Generating capsule explanation with Ollama",
                    async (progress) => {
                        progress.report({ increment: 20, message: "Connecting to Ollama..." });
                        
                        const response = await bridge.rpc('explain_capsule', {
                            capsule_id: capsuleId,
                            model: 'mistral'
                        });
                        
                        progress.report({ increment: 100, message: "Explanation generated!" });
                        return response;
                    }
                );

                if (result.ok) {
                    // Show explanation in a new document
                    const content = `# 🧠 Capsule Explanation: ${capsuleId}

${result.text}

---
*Generated by Ollama/Mistral via Holographic Memory System*
`;

                    const doc = await vscode.workspace.openTextDocument({
                        content,
                        language: 'markdown'
                    });
                    
                    await vscode.window.showTextDocument(doc, {
                        viewColumn: vscode.ViewColumn.Beside,
                        preview: true
                    });
                } else {
                    await errorHandler.showWarning(
                        'Failed to generate explanation',
                        result.error || 'Unknown error occurred',
                        [
                            'Check if Ollama is running (http://localhost:11434)',
                            'Verify the capsule ID exists',
                            'Try with a different model'
                        ]
                    );
                }

            } catch (err) {
                await errorHandler.handleError(err as Error, {
                    operation: 'explain-capsule',
                    component: 'extension',
                    severity: 'error',
                    recoverable: true,
                    userMessage: 'Failed to explain capsule',
                    suggestedActions: [
                        'Check Ollama installation and service',
                        'Verify network connectivity',
                        'Try with a different capsule ID'
                    ]
                });
            }
        }),

        // Rebuild FAISS index for fast retrieval
        vscode.commands.registerCommand('holographicMemory.rebuildIndex', async () => {
            try {
                await bridge.ensureRunning();
                
                const result = await progressReporter.withDetailedProgress(
                    "Rebuilding FAISS index for fast retrieval",
                    async (progress) => {
                        progress.report({ increment: 50, message: "Building index..." });
                        
                        const response = await bridge.rpc('rebuild_faiss', {});
                        
                        progress.report({ increment: 100, message: "Index rebuilt!" });
                        return response;
                    }
                );

                if (result.ok) {
                    vscode.window.showInformationMessage(
                        `✅ FAISS index rebuilt successfully! Indexed ${result.size} capsules.`
                    );
                } else {
                    await errorHandler.showWarning(
                        'FAISS index rebuild failed',
                        result.reason || 'Unknown error',
                        [
                            'Install FAISS: pip install faiss-cpu',
                            'Check if capsules exist in memory',
                            'Verify system resources'
                        ]
                    );
                }

            } catch (err) {
                await errorHandler.handleError(err as Error, {
                    operation: 'rebuild-faiss-index',
                    component: 'extension',
                    severity: 'error',
                    recoverable: true,
                    userMessage: 'Failed to rebuild FAISS index',
                    suggestedActions: [
                        'Install FAISS: pip install faiss-cpu',
                        'Check Python environment',
                        'Verify memory system is working'
                    ]
                });
            }
        }),

        // New Holo commands
        vscode.commands.registerCommand('holo.openGraph', () => {
            HoloGraphPanel.createOrShow(context.extensionUri, bridge);
        }),

        vscode.commands.registerCommand('holo.indexWorkspace', async () => {
            await bridge.ensureRunning();
            const ws = vscode.workspace.workspaceFolders?.map(f => f.uri.fsPath) ?? [];
            
            if (ws.length === 0) {
                vscode.window.showWarningMessage('No workspace folders open');
                return;
            }

            await vscode.window.withProgress(
                { 
                    location: vscode.ProgressLocation.Notification, 
                    title: 'Holo: Indexing workspace', 
                    cancellable: false 
                },
                async () => {
                    try {
                        const res = await bridge.rpc('index_workspace', { workspace_path: ws[0] });
                        
                        vscode.window.showInformationMessage(
                            `Scanned ${res.files_scanned || 0} files • indexed ${res.total_annotations || 0} annotations (created ${res.created_capsules?.length || 0} capsules)`
                        );
                        
                        if (res.errors?.length) {
                            const items = res.errors.slice(0, 5).map((e: any) => `${e.file}: ${e.error}`);
                            vscode.window.showWarningMessage(`Holo: ${res.errors.length} issues\n${items.join('\n')}`);
                        }
                        
                        holoTreeProvider.refresh();
                        treeProvider.refresh();
                    } catch (error) {
                        vscode.window.showErrorMessage(`Indexing failed: ${error}`);
                    }
                }
            );
        }),

        vscode.commands.registerCommand('holo.queryMemory', async () => {
            const queryInput = await vscode.window.showInputBox({
                prompt: 'Enter query (JSON format)',
                placeHolder: '{"concept": "example", "domain": "ai"}',
                value: '{"concept": "memory"}'
            });

            if (!queryInput) return;

            try {
                const query = JSON.parse(queryInput);
                await bridge.ensureRunning();
                
                const result = await bridge.rpc('query_capsules', { query });
                
                if (result && Array.isArray(result)) {
                    const content = `# 🔍 Memory Query Results

Query: \`${queryInput}\`

Found ${result.length} matches:

${result.map((match: any, i: number) => `
## ${i + 1}. ${match.capsule_id || match.id}
- **Score**: ${match.score?.toFixed(3) || 'N/A'}
- **Slots**: ${JSON.stringify(match.slots || {}, null, 2)}
- **Source**: ${match.source?.file ? `${match.source.file}:${match.source.lineStart}` : 'Unknown'}
`).join('\n')}

---
*Generated by Holographic Memory Query*
`;

                    const doc = await vscode.workspace.openTextDocument({
                        content,
                        language: 'markdown'
                    });
                    
                    await vscode.window.showTextDocument(doc);
                } else {
                    vscode.window.showInformationMessage('No matches found for query');
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Query failed: ${error}`);
            }
        }),

        vscode.commands.registerCommand('holo.rebuildANN', async () => {
            try {
                await bridge.ensureRunning();
                const res = await bridge.rpc('rebuild_ann', {});
                
                if (res.ok) {
                    vscode.window.showInformationMessage(`FAISS index ready (${res.size} vectors)`);
                } else {
                    vscode.window.showWarningMessage(`FAISS not active: ${res.reason ?? 'unknown'}`);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`FAISS rebuild failed: ${error}`);
            }
        }),

        vscode.commands.registerCommand('holo.gotoCapsule', async (capsule: any) => {
            // capsule from tree node or manual call
            if (!capsule?.source?.file) {
                vscode.window.showWarningMessage('No source information available for this capsule');
                return;
            }
            
            try {
                const uri = vscode.Uri.file(capsule.source.file);
                const doc = await vscode.workspace.openTextDocument(uri);
                const editor = await vscode.window.showTextDocument(doc, { preview: false });
                
                const lineStart = Math.max(0, (capsule.source.lineStart ?? 1) - 1);
                const lineEnd = Math.max(lineStart, (capsule.source.lineEnd ?? lineStart) - 1);
                const range = new vscode.Range(lineStart, 0, lineEnd, 0);
                
                editor.revealRange(range, vscode.TextEditorRevealType.InCenter);
                editor.selection = new vscode.Selection(lineStart, 0, lineStart, 0);
                
                vscode.window.setStatusBarMessage(
                    `📍 Jumped to ${capsule.source.style} annotation at line ${capsule.source.lineStart}`,
                    3000
                );
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to open source: ${error}`);
            }
        }),

        vscode.commands.registerCommand('holo.explainCapsule', async (capsule: any) => {
            try {
                await bridge.ensureRunning();
                
                const model = await vscode.window.showInputBox({ 
                    prompt: 'Ollama model (default: mistral)', 
                    value: 'mistral' 
                });
                
                const res = await vscode.window.withProgress(
                    {
                        location: vscode.ProgressLocation.Notification,
                        title: 'Generating explanation with Ollama...',
                        cancellable: false
                    },
                    async () => {
                        return await bridge.rpc('explain_capsule', { 
                            capsule_id: capsule.id || capsule.capsule_id, 
                            model: model || 'mistral' 
                        });
                    }
                );
                
                if (res.ok) {
                    const content = `# 🧠 Capsule Explanation: ${capsule.id || capsule.capsule_id}

${res.text}

---
*Generated by Ollama/Mistral via Holographic Memory System*
`;

                    const doc = await vscode.workspace.openTextDocument({
                        content,
                        language: 'markdown'
                    });
                    
                    await vscode.window.showTextDocument(doc, {
                        viewColumn: vscode.ViewColumn.Beside,
                        preview: true
                    });
                } else {
                    vscode.window.showErrorMessage(`Explain failed: ${res.error ?? 'unknown error'}`);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Explanation failed: ${error}`);
            }
        })
    );
}

// This method is called when the extension is deactivated
export function deactivate() {
    // Clean up resources
}

