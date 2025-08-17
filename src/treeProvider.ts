// src/treeProvider.ts - Memory explorer tree view

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { PythonBridge } from './pythonBridge';

export class MemoryTreeProvider implements vscode.TreeDataProvider<MemoryItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<MemoryItem | undefined | null | void> = new vscode.EventEmitter<MemoryItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<MemoryItem | undefined | null | void> = this._onDidChangeTreeData.event;
    private capsuleIconPath: string;

    constructor(private bridge: PythonBridge) {
        // Create the SVG icon for capsules
        this.capsuleIconPath = path.join(__filename, '..', 'capsule-icon.svg');

        // Write the SVG content to the file
        const svgContent = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2Z" stroke="currentColor" stroke-width="2"/>
  <path d="M12 7V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M9 4.5C9 4.5 9 7 12 7C15 7 15 4.5 15 4.5" stroke="currentColor" stroke-width="2"/>
  <path d="M9 19.5C9 19.5 9 17 12 17C15 17 15 19.5 15 19.5" stroke="currentColor" stroke-width="2"/>
  <path d="M4.5 9C4.5 9 7 9 7 12C7 15 4.5 15 4.5 15" stroke="currentColor" stroke-width="2"/>
  <path d="M19.5 9C19.5 9 17 9 17 12C17 15 19.5 15 19.5 15" stroke="currentColor" stroke-width="2"/>
</svg>`;

        try {
            fs.writeFileSync(this.capsuleIconPath, svgContent);
        } catch (error) {
            console.warn('Could not create capsule icon:', error);
        }
    }
    
    refresh(): void {
        this._onDidChangeTreeData.fire();
    }
    
    getTreeItem(element: MemoryItem): vscode.TreeItem {
        return element;
    }
    
    async getChildren(element?: MemoryItem): Promise<MemoryItem[]> {
        try {
            await this.bridge.ensureRunning();

            if (!element) {
                // Root level - show categories
                return [
                    new MemoryItem('Capsules', 'capsules', vscode.TreeItemCollapsibleState.Collapsed),
                    new MemoryItem('Roles', 'roles', vscode.TreeItemCollapsibleState.Collapsed),
                    new MemoryItem('Metrics', 'metrics', vscode.TreeItemCollapsibleState.Collapsed)
                ];
            } else if (element.contextValue === 'capsules') {
                // List all capsules and annotations with source info
                const [capsulesResult, annotationsResult] = await Promise.all([
                    this.bridge.rpc('list_capsules', {}),
                    this.bridge.rpc('get_indexed_annotations', {})
                ]);
                
                const items: MemoryItem[] = [];
                
                // Add regular capsules
                if (capsulesResult && capsulesResult.capsules) {
                    items.push(...capsulesResult.capsules.map((capsule: any) => {
                        const item = new MemoryItem(
                            capsule.content,
                            'capsule',
                            vscode.TreeItemCollapsibleState.Collapsed
                        );
                        item.description = `Imp: ${capsule.importance.toFixed(2)}`;
                        item.id = capsule.id;
                        return item;
                    }));
                }
                
                // Add indexed annotations with Go to Definition support
                if (annotationsResult && Array.isArray(annotationsResult)) {
                    items.push(...annotationsResult.map((annotation: any) => {
                        const item = new MemoryItem(
                            `📍 ${annotation.capsule_id}`,
                            'annotation',
                            vscode.TreeItemCollapsibleState.Collapsed,
                            annotation.source
                        );
                        item.description = `${annotation.annotation_type} - ${path.basename(annotation.file_path)}:${annotation.line_start}`;
                        item.id = annotation.capsule_id;
                        
                        // Enable Go to Definition command
                        item.command = {
                            command: 'holographicMemory.goToDefinition',
                            title: 'Go to Definition',
                            arguments: [annotation.source]
                        };
                        
                        return item;
                    }));
                }
                
                return items;
            } else if (element.contextValue === 'roles') {
                // List all roles
                const result = await this.bridge.rpc('list_roles', {});
                if (!result || !result.roles) {
                    return [];
                }
    
                return result.roles.map((role: any) => {
                    const item = new MemoryItem(
                        role.name,
                        'role',
                        vscode.TreeItemCollapsibleState.None
                    );
                    item.description = `(${role.count})`;
                    return item;
                });
            } else if (element.contextValue === 'metrics') {
                // Show memory metrics
                const result = await this.bridge.rpc('explain_with_llm', { action: 'System Analysis' });

                return [
                    new MemoryItem('View Full Report', 'report', vscode.TreeItemCollapsibleState.None)
                ];
            } else if (element.contextValue === 'capsule') {
                // Get capsule details
                const details = await this.bridge.rpc('get_capsule_details', { id: element.id });

                const items: MemoryItem[] = [];

                // Add basic info
                items.push(new MemoryItem(`Consciousness: ${details.consciousness_level}`, 'capsule-detail', vscode.TreeItemCollapsibleState.None));
                items.push(new MemoryItem(`Importance: ${details.importance.toFixed(3)}`, 'capsule-detail', vscode.TreeItemCollapsibleState.None));

                // Add role bindings
                for (const [role, data] of Object.entries(details.role_vectors)) {
                    const bindingItem = new MemoryItem(
                        `${role}`,
                        'role-binding',
                        vscode.TreeItemCollapsibleState.None
                    );

                    // Show the top match
                    const roleData = data as any;
                    if (roleData.top_matches && roleData.top_matches.length > 0) {
                        bindingItem.description = `→ ${roleData.top_matches[0][0]} (${roleData.top_matches[0][1].toFixed(2)})`;
                    }

                    items.push(bindingItem);
                }

                return items;
            }
            return [];
        } catch (error) {
            vscode.window.showErrorMessage(`Error loading memory items: ${error}`);
            return [];
        }
    }
            
    getParent(_element: MemoryItem): vscode.ProviderResult<MemoryItem> {
        return null;
    }
}

class MemoryItem extends vscode.TreeItem {
    public id?: string;
    public source?: {
        file: string;
        lineStart: number;
        lineEnd: number;
        style: string;
    };

    constructor(
        public readonly label: string,
        public readonly contextValue: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        source?: any
    ) {
        super(label, collapsibleState);
        this.contextValue = contextValue;
        this.source = source;

        // Set icon based on type
        if (contextValue === 'capsules') {
            this.iconPath = new vscode.ThemeIcon('database');
        } else if (contextValue === 'roles') {
            this.iconPath = new vscode.ThemeIcon('symbol-field');
        } else if (contextValue === 'metrics') {
            this.iconPath = new vscode.ThemeIcon('graph');
        } else if (contextValue === 'capsule') {
            // Use the custom SVG icon for capsules
            const iconPath = path.join(path.dirname(__filename), 'capsule-icon.svg');
            if (fs.existsSync(iconPath)) {
                this.iconPath = {
                    light: vscode.Uri.file(iconPath),
                    dark: vscode.Uri.file(iconPath)
                };
            } else {
                this.iconPath = new vscode.ThemeIcon('package');
            }
        } else if (contextValue === 'role') {
            this.iconPath = new vscode.ThemeIcon('key');
        } else if (contextValue === 'role-binding') {
            this.iconPath = new vscode.ThemeIcon('link');
        } else if (contextValue === 'report') {
            this.iconPath = new vscode.ThemeIcon('notebook');
            this.command = {
                command: 'holographicMemory.explainWithLLM',
                title: 'View Full Report'
            };
        }
    }
}