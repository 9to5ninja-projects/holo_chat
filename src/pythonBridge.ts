import * as vscode from 'vscode';
import * as path from 'path';
import * as cp from 'child_process';
import * as crypto from 'crypto';

type PendingRequest = {
    resolve: (value: any) => void;
    reject: (reason: any) => void;
};

export class PythonBridge {
    private process: cp.ChildProcess | undefined;
    private pendingRequests: Map<string, PendingRequest> = new Map();
    private outputChannel: vscode.OutputChannel;
    
    constructor(private extensionPath: string) {
        this.outputChannel = vscode.window.createOutputChannel('Holographic Memory');
    }
    
    async ensureRunning(): Promise<void> {
        if (this.process && !this.process.killed) {
            return;
        }
        
        return new Promise<void>((resolve, reject) => {
            try {
                const pythonPath = vscode.workspace.getConfiguration('holographicMemory').get('pythonPath', 'python');
                const scriptPath = path.join(this.extensionPath, '..', 'python', 'engine.py');
                
                this.outputChannel.appendLine(`Starting Python bridge: ${pythonPath} ${scriptPath}`);
                
                this.process = cp.spawn(pythonPath, [scriptPath], {
                    cwd: this.extensionPath,
                    env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
                });
                
                this.process.stdout?.on('data', (data: Buffer) => {
                    const lines = data.toString().trim().split('\n');
                    
                    for (const line of lines) {
                        try {
                            if (!line.startsWith('{')) {
                                this.outputChannel.appendLine(`[Python]: ${line}`);
                                continue;
                            }
                            
                            const response = JSON.parse(line);
                            
                            if (response.id && this.pendingRequests.has(response.id)) {
                                const request = this.pendingRequests.get(response.id)!;
                                this.pendingRequests.delete(response.id);
                                
                                if (response.error) {
                                    request.reject(new Error(response.error));
                                } else {
                                    request.resolve(response);
                                }
                            }
                        } catch (e) {
                            this.outputChannel.appendLine(`[Python parsing error]: ${line}`);
                        }
                    }
                });
                
                this.process.stderr?.on('data', (data: Buffer) => {
                    this.outputChannel.appendLine(`[Python Error]: ${data.toString()}`);
                });
                
                this.process.on('close', (code: number | null) => {
                    this.outputChannel.appendLine(`Python bridge process exited with code ${code}`);
                    this.process = undefined;
                    
                    // Reject all pending requests
                    for (const [id, request] of this.pendingRequests) {
                        request.reject(new Error(`Python process exited with code ${code}`));
                    }
                    this.pendingRequests.clear();
                });
                
                // Wait for startup
                setTimeout(() => {
                    if (this.process && !this.process.killed) {
                        resolve();
                    } else {
                        reject(new Error('Failed to start Python bridge'));
                    }
                }, 1000);
                
            } catch (e) {
                reject(e);
            }
        });
    }
    
    async rpc(method: string, params: any): Promise<any> {
        await this.ensureRunning();
        
        return new Promise((resolve, reject) => {
            const id = crypto.randomUUID();
            this.pendingRequests.set(id, { resolve, reject });
            
            const request = {
                id,
                method,
                params
            };
            
            if (this.process && this.process.stdin) {
                this.process.stdin.write(JSON.stringify(request) + '\n');
            } else {
                reject(new Error('Python bridge not running'));
                this.pendingRequests.delete(id);
            }
        });
    }
    
    dispose(): void {
        if (this.process && !this.process.killed) {
            this.process.kill();
        }
        this.outputChannel.dispose();
    }
}