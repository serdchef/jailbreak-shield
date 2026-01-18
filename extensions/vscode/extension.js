const vscode = require('vscode');
const axios = require('axios');

function activate(context) {
    console.log('Aegis Shield is now active!');

    let disposable = vscode.commands.registerCommand('aegis.checkPrompt', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        if (!text) {
            vscode.window.showWarningMessage('Please select some text to analyze.');
            return;
        }

        vscode.window.showInformationMessage('Aegis analyzing...');

        try {
            const response = await axios.post('http://localhost:8000/api/v1/analyze', {
                prompt: text,
                user_id: 'vscode_user'
            });

            const result = response.data;
            if (result.safe) {
                vscode.window.showInformationMessage(`✅ Safe (Risk: ${result.risk_score}%)`);
            } else {
                vscode.window.showErrorMessage(`🚫 Blocked: ${result.attack_type} (Risk: ${result.risk_score}%)`);
            }
        } catch (error) {
            vscode.window.showErrorMessage('Analysis failed. Is Aegis running?');
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
}
