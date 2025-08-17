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
exports.MemoryTreeProvider = void 0;
const vscode = __importStar(require("vscode"));
class MemoryTreeProvider {
    constructor(bridge) {
        this.bridge = bridge;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    async getChildren(element) {
        try {
            if (!element) {
                // Root level - get all capsules
                await this.bridge.ensureRunning();
                const res = await this.bridge.rpc('get_indexed_annotations', {});
                if (!Array.isArray(res)) {
                    return [];
                }
                return res.map((c) => ({
                    type: 'capsule',
                    id: c.capsule_id,
                    label: c.capsule_id,
                    source: c.source,
                    slots: c.slots,
                    weights: c.weights,
                    meta: c.meta,
                    annotation_type: c.annotation_type
                }));
            }
            if (element.type === 'capsule') {
                // Show roles for this capsule
                const roles = Object.keys(element.slots || {});
                return roles.map((role) => ({
                    type: 'role',
                    capsule: element.id,
                    role: role,
                    label: `${role}: ${element.slots[role]}`
                }));
            }
            return [];
        }
        catch (error) {
            console.error('Error getting tree children:', error);
            return [];
        }
    }
    getTreeItem(e) {
        const item = new vscode.TreeItem(e.label || e.id);
        if (e.type === 'capsule') {
            item.collapsibleState = vscode.TreeItemCollapsibleState.Collapsed;
            item.contextValue = 'holoCapsule';
            if (e.source) {
                item.tooltip = `${e.source.file} (${e.source.style})`;
            }
            // Set command to go to definition when clicked
            item.command = {
                command: 'holo.gotoCapsule',
                title: 'Open',
                arguments: [e]
            };
        }
        else {
            item.collapsibleState = vscode.TreeItemCollapsibleState.None;
        }
        return item;
    }
}
exports.MemoryTreeProvider = MemoryTreeProvider;
//# sourceMappingURL=treeData.js.map