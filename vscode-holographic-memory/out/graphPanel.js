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
exports.HoloGraphPanel = void 0;
const vscode = __importStar(require("vscode"));
class HoloGraphPanel {
    static createOrShow(extensionUri, bridge) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        if (HoloGraphPanel.currentPanel) {
            HoloGraphPanel.currentPanel._panel.reveal(column);
            return;
        }
        const panel = vscode.window.createWebviewPanel('holoGraph', 'Holographic Memory Graph', column || vscode.ViewColumn.One, {
            enableScripts: true,
            retainContextWhenHidden: true,
            localResourceRoots: [
                vscode.Uri.joinPath(extensionUri, 'media'),
                vscode.Uri.joinPath(extensionUri, 'out', 'src')
            ]
        });
        HoloGraphPanel.currentPanel = new HoloGraphPanel(panel, extensionUri, bridge);
    }
    constructor(panel, extensionUri, bridge) {
        this.bridge = bridge;
        this._disposables = [];
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.html = this._getHtmlForWebview(this._panel.webview, extensionUri);
        this._setWebviewMessageListener(this._panel.webview);
    }
    dispose() {
        HoloGraphPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
    postMessage(message) {
        this._panel.webview.postMessage(message);
    }
    _setWebviewMessageListener(webview) {
        webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
                case 'recallSlot':
                    await this._handleRecallSlot(message.data);
                    break;
                case 'explainCapsule':
                    // Legacy support
                    await vscode.commands.executeCommand('holo.explainCapsule', { id: message.capsuleId });
                    break;
                case 'command':
                    // New command routing
                    await vscode.commands.executeCommand(`holo.${message.name}`, ...message.args);
                    break;
                case 'ready':
                    await this._loadGraphData();
                    break;
            }
        }, undefined, this._disposables);
    }
    async _handleRecallSlot(data) {
        try {
            await this.bridge.ensureRunning();
            const result = await this.bridge.rpc('query_capsules', { query: data });
            this._panel.webview.postMessage({
                type: 'recallResult',
                data: result
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Recall failed: ${error}`);
        }
    }
    async _loadGraphData() {
        try {
            await this.bridge.ensureRunning();
            const annotations = await this.bridge.rpc('get_indexed_annotations', {});
            // Convert annotations to graph data
            const nodes = [];
            const edges = [];
            if (Array.isArray(annotations)) {
                for (const ann of annotations) {
                    nodes.push({
                        data: {
                            id: ann.capsule_id,
                            label: ann.capsule_id,
                            type: ann.annotation_type,
                            source: ann.source,
                            slots: ann.slots,
                            weights: ann.weights,
                            meta: ann.meta
                        }
                    });
                    // Create edges based on shared slots
                    for (const other of annotations) {
                        if (other.capsule_id !== ann.capsule_id) {
                            const sharedSlots = Object.keys(ann.slots || {}).filter(slot => (other.slots || {})[slot] === ann.slots[slot]);
                            if (sharedSlots.length > 0) {
                                edges.push({
                                    data: {
                                        id: `${ann.capsule_id}-${other.capsule_id}`,
                                        source: ann.capsule_id,
                                        target: other.capsule_id,
                                        weight: sharedSlots.length,
                                        sharedSlots: sharedSlots
                                    }
                                });
                            }
                        }
                    }
                }
            }
            this._panel.webview.postMessage({
                type: 'graphData',
                data: { nodes, edges }
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to load graph data: ${error}`);
        }
    }
    _getHtmlForWebview(webview, extensionUri) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holographic Memory Graph</title>
    <script src="https://unpkg.com/cytoscape@3.21.0/dist/cytoscape.min.js"></script>
    <style>
        body {
            font-family: var(--vscode-font-family);
            margin: 0;
            padding: 0;
            background-color: var(--vscode-editor-background);
            color: var(--vscode-editor-foreground);
        }
        
        #toolbar {
            padding: 10px;
            background-color: var(--vscode-panel-background);
            border-bottom: 1px solid var(--vscode-panel-border);
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }
        
        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        #status {
            margin-left: auto;
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
        }
        
        #cy {
            width: 100%;
            height: calc(100vh - 60px);
            background-color: var(--vscode-editor-background);
        }
        
        .node-tooltip {
            position: absolute;
            background: var(--vscode-hover-background);
            border: 1px solid var(--vscode-hover-border);
            padding: 8px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            max-width: 300px;
        }
    </style>
</head>
<body>
    <div id="toolbar">
        <button id="btnExplain" disabled>🧠 Explain Selected</button>
        <button id="btnOpen" disabled>📍 Go to Source</button>
        <button id="btnQuery">🔍 Query Memory</button>
        <button id="btnRefresh">🔄 Refresh</button>
        <div id="status">Ready</div>
    </div>
    
    <div id="cy"></div>

    <script>
        const vscode = acquireVsCodeApi();
        let cy;
        let lastSelected = null;

        // Initialize Cytoscape
        function initGraph() {
            cy = cytoscape({
                container: document.getElementById('cy'),
                
                style: [
                    {
                        selector: 'node',
                        style: {
                            'background-color': '#4A90E2',
                            'label': 'data(label)',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'color': '#ffffff',
                            'font-size': '12px',
                            'width': '60px',
                            'height': '60px',
                            'border-width': '2px',
                            'border-color': '#2E5C8A'
                        }
                    },
                    {
                        selector: 'node[type="inline"]',
                        style: {
                            'background-color': '#E74C3C',
                            'border-color': '#C0392B'
                        }
                    },
                    {
                        selector: 'node[type="docstring"]',
                        style: {
                            'background-color': '#27AE60',
                            'border-color': '#229954'
                        }
                    },
                    {
                        selector: 'node[type="decorator"]',
                        style: {
                            'background-color': '#F39C12',
                            'border-color': '#E67E22'
                        }
                    },
                    {
                        selector: 'node:selected',
                        style: {
                            'border-width': '4px',
                            'border-color': '#FFD700'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'width': 'mapData(weight, 1, 5, 2, 8)',
                            'line-color': '#95A5A6',
                            'target-arrow-color': '#95A5A6',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier',
                            'opacity': 0.7
                        }
                    }
                ],
                
                layout: {
                    name: 'cose',
                    animate: true,
                    animationDuration: 1000,
                    nodeRepulsion: 8000,
                    idealEdgeLength: 100,
                    edgeElasticity: 100
                }
            });

            // Handle node selection
            cy.on('tap', 'node', function(evt) {
                const node = evt.target;
                lastSelected = node.data();
                updateButtonStates();
                updateStatus(\`Selected: \${node.data('label')}\`);
            });

            // Handle background tap (deselect)
            cy.on('tap', function(evt) {
                if (evt.target === cy) {
                    lastSelected = null;
                    updateButtonStates();
                    updateStatus('Ready');
                }
            });
        }

        function updateButtonStates() {
            const hasSelection = lastSelected !== null;
            const hasSource = hasSelection && lastSelected.source && lastSelected.source.file;
            
            document.getElementById('btnExplain').disabled = !hasSelection;
            document.getElementById('btnOpen').disabled = !hasSource;
        }

        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }

        // Button event handlers
        document.getElementById('btnExplain').onclick = () => {
            if (!lastSelected) return;
            updateStatus('Generating explanation...');
            vscode.postMessage({ 
                type: 'command', 
                name: 'explainCapsule', 
                args: [{ id: lastSelected.id, ...lastSelected }] 
            });
        };

        document.getElementById('btnOpen').onclick = () => {
            if (!lastSelected || !lastSelected.source) return;
            updateStatus('Opening source...');
            vscode.postMessage({ 
                type: 'command', 
                name: 'gotoCapsule', 
                args: [lastSelected] 
            });
        };

        document.getElementById('btnQuery').onclick = async () => {
            const query = prompt('Enter query (JSON format):', '{"concept": "example"}');
            if (!query) return;
            
            try {
                const queryObj = JSON.parse(query);
                updateStatus('Querying memory...');
                vscode.postMessage({ 
                    type: 'recallSlot', 
                    data: queryObj 
                });
            } catch (e) {
                alert('Invalid JSON format');
            }
        };

        document.getElementById('btnRefresh').onclick = () => {
            updateStatus('Refreshing graph...');
            vscode.postMessage({ type: 'ready' });
        };

        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.type) {
                case 'graphData':
                    cy.elements().remove();
                    cy.add(message.data.nodes);
                    cy.add(message.data.edges);
                    cy.layout({ name: 'cose', animate: true }).run();
                    updateStatus(\`Loaded \${message.data.nodes.length} capsules\`);
                    break;
                    
                case 'recallResult':
                    // Highlight matching nodes
                    cy.nodes().removeClass('highlighted');
                    if (message.data && Array.isArray(message.data)) {
                        message.data.forEach(result => {
                            const node = cy.getElementById(result.id || result.capsule_id);
                            if (node.length > 0) {
                                node.addClass('highlighted');
                            }
                        });
                        updateStatus(\`Found \${message.data.length} matches\`);
                    }
                    break;
            }
        });

        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', () => {
            initGraph();
            updateButtonStates();
            
            // Request initial data
            vscode.postMessage({ type: 'ready' });
        });
    </script>
</body>
</html>`;
    }
}
exports.HoloGraphPanel = HoloGraphPanel;
//# sourceMappingURL=graphPanel.js.map