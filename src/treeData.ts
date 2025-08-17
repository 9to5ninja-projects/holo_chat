import * as vscode from 'vscode';
import { PythonBridge } from './pythonBridge';

export class MemoryTreeProvider implements vscode.TreeDataProvider<any> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  onDidChangeTreeData = this._onDidChangeTreeData.event;
  
  constructor(private bridge: PythonBridge) {}
  
  refresh() { 
    this._onDidChangeTreeData.fire(); 
  }

  async getChildren(element?: any) {
    try {
      if (!element) {
        // Root level - get all capsules
        await this.bridge.ensureRunning();
        const res = await this.bridge.rpc('get_indexed_annotations', {});
        
        if (!Array.isArray(res)) {
          return [];
        }
        
        return res.map((c: any) => ({ 
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
        return roles.map((role: string) => ({
          type: 'role',
          capsule: element.id,
          role: role,
          label: `${role}: ${element.slots[role]}`
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Error getting tree children:', error);
      return [];
    }
  }

  getTreeItem(e: any): vscode.TreeItem {
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
      
    } else {
      item.collapsibleState = vscode.TreeItemCollapsibleState.None;
    }
    
    return item;
  }
}