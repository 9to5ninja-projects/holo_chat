"use strict";
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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const pythonBridge_1 = require("./pythonBridge");
const graphPanel_1 = require("./graphPanel");
const treeProvider_1 = require("./treeProvider");
// This method is called when the extension is activated
function activate(context) {
    console.log('Activating Holographic Memory extension');
    // Create the Python bridge
    const bridge = new pythonBridge_1.PythonBridge(context.extensionPath);
    // Create tree view provider
    const treeProvider = new treeProvider_1.MemoryTreeProvider(bridge);
    vscode.window.registerTreeDataProvider('holographicMemoryExplorer', treeProvider);
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('holographicMemory.openGraph', () => {
        graphPanel_1.HolographicGraphPanel.createOrShow(context.extensionUri, bridge);
    }), vscode.commands.registerCommand('holographicMemory.newCapsule', async () => {
        const whatInput = await vscode.window.showInputBox({
            prompt: 'Enter content for WHAT role (required)'
        });
        if (!whatInput)
            return;
        const whereInput = await vscode.window.showInputBox({
            prompt: 'Enter content for WHERE role (optional)'
        });
        const whenInput = await vscode.window.showInputBox({
            prompt: 'Enter content for WHEN role (optional)'
        });
        const bindings = {
            'WHAT': whatInput
        };
        if (whereInput)
            bindings['WHERE'] = whereInput;
        if (whenInput)
            bindings['WHEN'] = whenInput;
        try {
            await bridge.ensureRunning();
            const result = await bridge.rpc('create_capsule', { bindings });
            if (result.success) {
                vscode.window.showInformationMessage('Memory capsule created successfully');
                treeProvider.refresh();
                // Update graph view if open
                graphPanel_1.HolographicGraphPanel.current?.postMessage({
                    type: 'capsuleCreated',
                    data: result.capsule
                });
            }
            else {
                vscode.window.showErrorMessage('Failed to create memory capsule');
            }
        }
        catch (err) {
            vscode.window.showErrorMessage(`Error creating capsule: ${err}`);
        }
    }), vscode.commands.registerCommand('holographicMemory.queryCapsule', async () => {
        const queryInput = await vscode.window.showInputBox({
            prompt: 'Enter query as JSON: {"WHAT":"concept","WHERE":"location"}',
            validateInput: (input) => {
                try {
                    JSON.parse(input);
                    return null;
                }
                catch (e) {
                    return 'Invalid JSON format';
                }
            }
        });
        if (!queryInput)
            return;
        try {
            const query = JSON.parse(queryInput);
            await bridge.ensureRunning();
            const results = await bridge.rpc('query_capsules', { query });
            // Open graph panel if not already open
            if (!graphPanel_1.HolographicGraphPanel.current) {
                await vscode.commands.executeCommand('holographicMemory.openGraph');
                // Short delay to allow panel to initialize
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            // Send results to graph panel
            graphPanel_1.HolographicGraphPanel.current?.postMessage({
                type: 'queryResults',
                data: results
            });
            vscode.window.showInformationMessage(`Found ${results.length} matching memory capsules`);
        }
        catch (err) {
            vscode.window.showErrorMessage(`Error querying capsules: ${err}`);
        }
    }), vscode.commands.registerCommand('holographicMemory.explainWithLLM', async () => {
        const options = ['Explain selected capsule', 'Analyze entire memory system'];
        const selection = await vscode.window.showQuickPick(options, {
            placeHolder: 'Choose explanation type'
        });
        if (!selection)
            return;
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
        }
        catch (err) {
            vscode.window.showErrorMessage(`Error generating explanation: ${err}`);
        }
    }), vscode.commands.registerCommand('holographicMemory.refresh', () => {
        treeProvider.refresh();
        vscode.window.showInformationMessage('Memory explorer refreshed');
    }));
}
// This method is called when the extension is deactivated
function deactivate() {
    // Clean up resources
}
//# sourceMappingURL=extension.js.map