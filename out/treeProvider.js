"use strict";
// src/treeProvider.ts - Memory explorer tree view
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
exports.MemoryTreeProvider = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
class MemoryTreeProvider {
    constructor(bridge) {
        this.bridge = bridge;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        // Create the SVG icon for capsules
        this.capsuleIconPath = path.join(__dirname, 'capsule-icon.svg');
        // Write the SVG content to the file
        const svgContent = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2Z" stroke="currentColor" stroke-width="2"/>
  <path d="M12 7V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M9 4.5C9 4.5 9 7 12 7C15 7 15 4.5 15 4.5" stroke="currentColor" stroke-width="2"/>
  <path d="M9 19.5C9 19.5 9 17 12 17C15 17 15 19.5 15 19.5" stroke="currentColor" stroke-width="2"/>
  <path d="M4.5 9C4.5 9 7 9 7 12C7 15 4.5 15 4.5 15" stroke="currentColor" stroke-width="2"/>
  <path d="M19.5 9C19.5 9 17 9 17 12C17 15 19.5 15 19.5 15" stroke="currentColor" stroke-width="2"/>
</svg>`;
        fs.writeFileSync(this.capsuleIconPath, svgContent);
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
            // Use the custom SVG icon for capsules
            if (fs.existsSync(path.join(__dirname, 'capsule-icon.svg'))) {
                this.iconPath = {
                    light: path.join(__dirname, 'capsule-icon.svg'),
                    dark: path.join(__dirname, 'capsule-icon.svg')
                };
            }
            else {
                this.iconPath = new vscode.ThemeIcon('package');
            }
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
//# sourceMappingURL=treeProvider.js.map