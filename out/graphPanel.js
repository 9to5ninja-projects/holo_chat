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
exports.HolographicGraphPanel = exports.MemoryTreeProvider = void 0;
const vscode = __importStar(require("vscode"));
const child_process = __importStar(require("child_process"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class MemoryTreeProvider {
    constructor(bridge) {
        this.bridge = bridge;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    async getChildren(element) {
        try {
            await this.bridge.ensureRunning();
            if (!element) {
                // Root level - show categories
                return [
                    new MemoryItem('Capsules', 'capsules', vscode.TreeItemCollapsibleState.Collapsed),
                    new MemoryItem('Roles', 'roles', vscode.TreeItemCollapsibleState.Collapsed),
                    new MemoryItem('Metrics', 'metrics', vscode.TreeItemCollapsibleState.Collapsed)
                ];
            }
            else if (element.contextValue === 'capsules') {
                // List all capsules
                const result = await this.bridge.rpc('list_capsules', {});
                if (!result || !result.capsules) {
                    return [];
                }
                return result.capsules.map((capsule) => {
                    const item = new MemoryItem(capsule.content, 'capsule', vscode.TreeItemCollapsibleState.Collapsed);
                    item.description = `Imp: ${capsule.importance.toFixed(2)}`;
                    item.id = capsule.id;
                    return item;
                });
            }
            else if (element.contextValue === 'roles') {
                // List all roles
                const result = await this.bridge.rpc('list_roles', {});
                if (!result || !result.roles) {
                    return [];
                }
                return result.roles.map((role) => {
                    const item = new MemoryItem(role.name, 'role', vscode.TreeItemCollapsibleState.None);
                    item.description = `(${role.count})`;
                    return item;
                });
            }
            else if (element.contextValue === 'metrics') {
                // Show memory metrics
                const result = await this.bridge.rpc('explain_with_llm', { action: 'System Analysis' });
                return [
                    new MemoryItem('View Full Report', 'report', vscode.TreeItemCollapsibleState.None)
                ];
            }
            else if (element.contextValue === 'capsule') {
                // Get capsule details
                const details = await this.bridge.rpc('get_capsule_details', { id: element.id });
                const items = [];
                // Add basic info
                items.push(new MemoryItem(`Consciousness: ${details.consciousness_level}`, 'capsule-detail', vscode.TreeItemCollapsibleState.None));
                items.push(new MemoryItem(`Importance: ${details.importance.toFixed(3)}`, 'capsule-detail', vscode.TreeItemCollapsibleState.None));
                // Add role bindings
                for (const [role, data] of Object.entries(details.role_vectors)) {
                    const bindingItem = new MemoryItem(`${role}`, 'role-binding', vscode.TreeItemCollapsibleState.None);
                    // Show the top match
                    if (data.top_matches && data.top_matches.length > 0) {
                        bindingItem.description = `→ ${data.top_matches[0][0]} (${data.top_matches[0][1].toFixed(2)})`;
                    }
                    items.push(bindingItem);
                }
                return items;
            }
            return [];
        }
        catch (error) {
            vscode.window.showErrorMessage(`Error loading memory items: ${error}`);
            return [];
        }
    }
    getParent(_element) {
        return null;
    }
}
exports.MemoryTreeProvider = MemoryTreeProvider;
class MemoryItem extends vscode.TreeItem {
    constructor(label, contextValue, collapsibleState) {
        super(label, collapsibleState);
        this.label = label;
        this.contextValue = contextValue;
        this.collapsibleState = collapsibleState;
        // Set icon based on type
        if (contextValue === 'capsules') {
            this.iconPath = new vscode.ThemeIcon('database');
        }
        else if (contextValue === 'roles') {
            this.iconPath = new vscode.ThemeIcon('symbol-field');
        }
        else if (contextValue === 'metrics') {
            this.iconPath = new vscode.ThemeIcon('graph');
        }
        else if (contextValue === 'capsule') {
            this.iconPath = new vscode.ThemeIcon('package');
        }
        else if (contextValue === 'role') {
            this.iconPath = new vscode.ThemeIcon('key');
        }
        else if (contextValue === 'role-binding') {
            this.iconPath = new vscode.ThemeIcon('link');
        }
        else if (contextValue === 'report') {
            this.iconPath = new vscode.ThemeIcon('notebook');
            this.command = {
                command: 'holographicMemory.explainWithLLM',
                title: 'View Full Report'
            };
        }
    }
}
class HolographicGraphPanel {
    static createOrShow(extensionUri, bridge) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        // If we already have a panel, show it
        if (HolographicGraphPanel.current) {
            HolographicGraphPanel.current._panel.reveal(column);
            return;
        }
        // Otherwise, create a new panel
        const panel = vscode.window.createWebviewPanel('holographicMemory.graphView', 'Holographic Memory Visualization', column || vscode.ViewColumn.One, {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(extensionUri, 'src', 'webview')
            ],
            retainContextWhenHidden: true
        });
        HolographicGraphPanel.current = new HolographicGraphPanel(panel, extensionUri, bridge);
    }
    constructor(panel, extensionUri, bridge) {
        this._disposables = [];
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._bridge = bridge;
        // Set the webview's initial html content
        this._update();
        // Listen for when the panel is disposed (user closes it)
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        // Update the content based on view changes
        this._panel.onDidChangeViewState(e => {
            if (this._panel.visible) {
                this._update();
            }
        }, null, this._disposables);
        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
                case 'queryCapsule':
                    const results = await this._bridge.rpc('query_capsules', { query: message.query });
                    this.postMessage({ type: 'queryResults', data: results });
                    break;
                case 'inspectCapsule':
                    const details = await this._bridge.rpc('get_capsule_details', { id: message.id });
                    this.postMessage({ type: 'capsuleDetails', data: details });
                    break;
                case 'explainWithLLM':
                    const explanation = await this._bridge.rpc('explain_with_llm', { capsuleId: message.id });
                    this.postMessage({ type: 'llmExplanation', data: explanation });
                    break;
                case 'cleanNodeModules':
                    this.cleanNodeModules();
                    break;
            }
        }, null, this._disposables);
        // Initial load of capsules
        this._loadCapsules();
    }
    cleanNodeModules() {
        const extensionPath = this._extensionUri.fsPath;
        try {
            // Create resources directory for the icon
            const resourcesPath = path.join(extensionPath, 'resources');
            if (!fs.existsSync(resourcesPath)) {
                fs.mkdirSync(resourcesPath);
            }
            // Create webview directory
            const webviewPath = path.join(extensionPath, 'src', 'webview');
            if (!fs.existsSync(webviewPath)) {
                fs.mkdirSync(webviewPath, { recursive: true });
            }
            // Create python directory
            const pythonPath = path.join(extensionPath, 'python');
            if (!fs.existsSync(pythonPath)) {
                fs.mkdirSync(pythonPath);
            }
            // Create the SVG icon file
            const iconContent = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2Z" stroke="currentColor" stroke-width="2"/>
  <path d="M12 7V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M9 4.5C9 4.5 9 7 12 7C15 7 15 4.5 15 4.5" stroke="currentColor" stroke-width="2"/>
  <path d="M9 19.5C9 19.5 9 17 12 17C15 17 15 19.5 15 19.5" stroke="currentColor" stroke-width="2"/>
  <path d="M4.5 9C4.5 9 7 9 7 12C7 15 4.5 15 4.5 15" stroke="currentColor" stroke-width="2"/>
  <path d="M19.5 9C19.5 9 17 9 17 12C17 15 19.5 15 19.5 15" stroke="currentColor" stroke-width="2"/>
</svg>`;
            fs.writeFileSync(path.join(resourcesPath, 'memory-icon.svg'), iconContent);
            // Create Python bridge main function
            const mainFunctionContent = `def main():
    """Main function to handle incoming JSON-RPC requests"""
    # Print startup message
    print("Holographic Memory Python Bridge started")

    # Create some demo capsules if memory is empty
    if not memory_env.xpunits:
        # Add demo capsules
        memory_env.ingest_experience("I am thinking about the nature of consciousness.")
        memory_env.ingest_experience("The dog is playing in the yard.")
        memory_env.ingest_experience("I wonder how my thoughts are represented holographically.")

    while True:
        try:
            # Read a line from stdin
            line = sys.stdin.readline()
            if not line:
                break

            # Parse the request
            request = json.loads(line.strip())

            # Handle the request
            response = handle_request(request)

            # Add the request ID to the response
            response['id'] = request.get('id', 0)

            # Send the response
            sys.stdout.write(json.dumps(response, default=numpy_to_json) + '\\n')
            sys.stdout.flush()
        except Exception as e:
            # Log any errors
            print(f"Error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

            # Try to send an error response
            try:
                error_response = {
                    'id': request.get('id', 0) if 'request' in locals() else 0,
                    'error': str(e)
                }
                sys.stdout.write(json.dumps(error_response) + '\\n')
                sys.stdout.flush()
            except:
                pass

if __name__ == "__main__":
    main()`;
            fs.writeFileSync(path.join(pythonPath, 'bridge_main.py'), mainFunctionContent);
            // Create tasks.json
            const tasksPath = path.join(extensionPath, '.vscode');
            if (!fs.existsSync(tasksPath)) {
                fs.mkdirSync(tasksPath, { recursive: true });
            }
            const tasksContent = {
                "version": "2.0.0",
                "tasks": [
                    {
                        "type": "npm",
                        "script": "watch",
                        "problemMatcher": "$tsc-watch",
                        "isBackground": true,
                        "presentation": {
                            "reveal": "never"
                        },
                        "group": {
                            "kind": "build",
                            "isDefault": true
                        }
                    }
                ]
            };
            fs.writeFileSync(path.join(tasksPath, 'tasks.json'), JSON.stringify(tasksContent, null, 4));
            // Create launch.json
            const launchContent = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Run Extension",
                        "type": "extensionHost",
                        "request": "launch",
                        "args": [
                            "--extensionDevelopmentPath=${workspaceFolder}"
                        ],
                        "outFiles": [
                            "${workspaceFolder}/out/**/*.js"
                        ],
                        "preLaunchTask": "${defaultBuildTask}"
                    }
                ]
            };
            fs.writeFileSync(path.join(tasksPath, 'launch.json'), JSON.stringify(launchContent, null, 4));
            // Remove node_modules directory
            const nodeModulesPath = path.join(extensionPath, 'node_modules');
            if (fs.existsSync(nodeModulesPath)) {
                if (process.platform === 'win32') {
                    child_process.execSync('powershell -Command "Remove-Item -Recurse -Force \'' + nodeModulesPath + '\'"');
                }
                else {
                    child_process.execSync('rm -rf "' + nodeModulesPath + '"');
                }
            }
            // Remove package-lock.json
            const packageLockPath = path.join(extensionPath, 'package-lock.json');
            if (fs.existsSync(packageLockPath)) {
                fs.unlinkSync(packageLockPath);
            }
            // Install dependencies
            child_process.execSync('npm install', { cwd: extensionPath });
            child_process.execSync('npm run compile', { cwd: extensionPath });
            vscode.window.showInformationMessage('Successfully cleaned node_modules and installed dependencies');
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to clean node_modules: ${error}`);
        }
    }
    async _loadCapsules() {
        try {
            await this._bridge.ensureRunning();
            const capsules = await this._bridge.rpc('list_capsules', {});
            this.postMessage({ type: 'loadCapsules', data: capsules });
        }
        catch (e) {
            vscode.window.showErrorMessage(`Failed to load capsules: ${e}`);
        }
    }
    postMessage(message) {
        this._panel.webview.postMessage(message);
    }
    _update() {
        // Generate the HTML for the webview
        const webview = this._panel.webview;
        this._panel.webview.html = this._getHtmlForWebview(webview);
    }
    _getHtmlForWebview(webview) {
        // Get the local path to scripts run in the webview
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'src', 'webview', 'graph.js'));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'src', 'webview', 'styles.css'));
        // Get Cytoscape.js from CDN
        const cytoscapeUri = 'https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.23.0/cytoscape.min.js';
        // Use a nonce to whitelist scripts that we trust
        const nonce = getNonce();
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource} https:; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}' https:;">
            <title>Holographic Memory Visualization</title>
            <link href="${styleUri}" rel="stylesheet">
        </head>
        <body>
            <div id="toolbar">
                <div id="search-container">
                    <input type="text" id="query-input" placeholder='{"WHAT":"dog","WHERE":"lab"}'>
                    <button id="search-button">Search</button>
                </div>
                <div id="actions-container">
                    <button id="new-capsule">New Capsule</button>
                    <button id="llm-explain">Explain with LLM</button>
                    <button id="refresh">Refresh</button>
                    <button id="clean-node-modules">Clean Node Modules</button>
                </div>
            </div>
            
            <div id="content-container">
                <div id="graph-container">
                    <div id="cy"></div>
                </div>
                <div id="details-panel">
                    <h3>Capsule Details</h3>
                    <div id="capsule-info">
                        <p>Select a capsule to view details</p>
                    </div>
                    <div id="role-bindings"></div>
                    <div id="capsule-metrics"></div>
                </div>
            </div>
            
            <script nonce="${nonce}" src="${cytoscapeUri}"></script>
            <script nonce="${nonce}" src="${scriptUri}"></script>
        </body>
        </html>`;
    }
    dispose() {
        HolographicGraphPanel.current = undefined;
        // Clean up resources
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
}
exports.HolographicGraphPanel = HolographicGraphPanel;
function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
//# sourceMappingURL=graphPanel.js.map