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
exports.PythonBridge = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const cp = __importStar(require("child_process"));
const crypto = __importStar(require("crypto"));
class PythonBridge {
    constructor(extensionPath) {
        this.extensionPath = extensionPath;
        this.pendingRequests = new Map();
        this.outputChannel = vscode.window.createOutputChannel('Holographic Memory');
    }
    async ensureRunning() {
        if (this.process && !this.process.killed) {
            return;
        }
        return new Promise((resolve, reject) => {
            try {
                const pythonPath = vscode.workspace.getConfiguration('holographicMemory').get('pythonPath', 'python');
                const scriptPath = path.join(this.extensionPath, '..', 'python', 'engine.py');
                this.outputChannel.appendLine(`Starting Python bridge: ${pythonPath} ${scriptPath}`);
                this.process = cp.spawn(pythonPath, [scriptPath], {
                    cwd: this.extensionPath,
                    env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
                });
                this.process.stdout?.on('data', (data) => {
                    const lines = data.toString().trim().split('\n');
                    for (const line of lines) {
                        try {
                            if (!line.startsWith('{')) {
                                this.outputChannel.appendLine(`[Python]: ${line}`);
                                continue;
                            }
                            const response = JSON.parse(line);
                            if (response.id && this.pendingRequests.has(response.id)) {
                                const request = this.pendingRequests.get(response.id);
                                this.pendingRequests.delete(response.id);
                                if (response.error) {
                                    request.reject(new Error(response.error));
                                }
                                else {
                                    request.resolve(response);
                                }
                            }
                        }
                        catch (e) {
                            this.outputChannel.appendLine(`[Python parsing error]: ${line}`);
                        }
                    }
                });
                this.process.stderr?.on('data', (data) => {
                    this.outputChannel.appendLine(`[Python Error]: ${data.toString()}`);
                });
                this.process.on('close', (code) => {
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
                    }
                    else {
                        reject(new Error('Failed to start Python bridge'));
                    }
                }, 1000);
            }
            catch (e) {
                reject(e);
            }
        });
    }
    async rpc(method, params) {
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
            }
            else {
                reject(new Error('Python bridge not running'));
                this.pendingRequests.delete(id);
            }
        });
    }
    dispose() {
        if (this.process && !this.process.killed) {
            this.process.kill();
        }
        this.outputChannel.dispose();
    }
}
exports.PythonBridge = PythonBridge;
//# sourceMappingURL=pythonBridge.js.map