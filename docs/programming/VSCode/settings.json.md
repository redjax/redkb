# VSCode settings.json and .code-workspace files

You can configure VSCode settings per-project using either a `settings.json` or `*.code-workspace` file. You must create these files manually, or create a Workspace in VSCode and save it as a file.

Your settings/workspace files should exist in a directory at the project's root, called `.vscode/`.

A `settings.json` file takes precedence, meaning if you set 2 different values for a single configuration, one in `settings.json` and one in a `.code-workspace` file, the option in `settings.json` will take precedence and be applied.

## settings.json configuration

If a file `.vscode/settings.json` exists at the project root, VSCode will load its configuration from that file.

### Example settings.json file

```json title=".vscode/settings.json" linenums="1"
{
    // ========================
    // Workbench Configurations
    // ========================
    "workbench.editor.labelFormat": "medium",
    "workbench.editor.highlightModifiedTabs": true,
    "workbench.editor.limit.enabled": true,
    "workbench.editor.limit.excludeDirty": true,
    "workbench.editor.limit.perEditorGroup": true,
    "workbench.editor.limit.value": 12,
    "workbench.editor.preferHistoryBasedLanguageDetection": true,
    "workbench.editor.pinnedTabSizing": "shrink",
    "workbench.editor.restoreViewState": true,
    "workbench.editor.revealIfOpen": true,
    "workbench.editor.scrollToSwitchTabs": true,
    "workbench.editor.showTabs": "multiple",
    "workbench.editor.sharedViewState": true,
    "workbench.editor.tabCloseButton": "left",
    "workbench.editor.tabSizing": "shrink",
    "workbench.editor.wrapTabs": true,
    // =====================
    // Editor Configurations
    // =====================
    "editor.acceptSuggestionOnEnter": "smart",
    "editor.autoClosingBrackets": "always",
    "editor.autoClosingQuotes": "always",
    "editor.autoIndent": "advanced",
    "editor.autoSurround": "languageDefined",
    "editor.codeLens": true,
    "editor.colorDecorators": true,
    "editor.comments.insertSpace": true,
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.cursorStyle": "block",
    "editor.cursorSurroundingLines": 8,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.detectIndentation": true,
    "editor.find.addExtraSpaceOnTop": true,
    "editor.find.autoFindInSelection": "multiline",
    "editor.find.cursorMoveOnType": false,
    "editor.find.loop": true,
    "editor.find.seedSearchStringFromSelection": "selection",
    "editor.folding": true,
    "editor.foldingHighlight": true,
    "editor.foldingStrategy": "auto",
    "editor.fontFamily": "Consolas, 'Courier New', monospace",
    "editor.fontLigatures": true,
    "editor.fontSize": 14,
    "editor.fontWeight": "normal",
    "editor.formatOnPaste": true,
    "editor.formatOnSaveMode": "modificationsIfAvailable",
    "editor.formatOnSave": true,
    "editor.guides.bracketPairs": "active",
    "editor.guides.bracketPairsHorizontal": "active",
    "editor.guides.highlightActiveBracketPair": true,
    "editor.guides.highlightActiveIndentation": "always",
    "editor.guides.indentation": true,
    "editor.inlayHints.enabled": "onUnlessPressed",
    "editor.inlineSuggest.enabled": true,
    "editor.largeFileOptimizations": true,
    "editor.linkedEditing": true,
    "editor.links": true,
    "editor.matchBrackets": "always",
    "editor.minimap.scale": 2,
    "editor.mouseWheelZoom": true,
    "editor.multiCursorMergeOverlapping": true,
    "editor.multiCursorModifier": "alt",
    "editor.occurrencesHighlight": "singleFile",
    "editor.overviewRulerBorder": true,
    "editor.parameterHints.enabled": true,
    "editor.parameterHints.cycle": true,
    "editor.quickSuggestions": {
        "other": "on",
        "comments": "off",
        "strings": "off"
    },
    "editor.rename.enablePreview": true,
    "editor.roundedSelection": true,
    "editor.selectionHighlight": true,
    "editor.semanticHighlighting.enabled": "configuredByTheme",
    "editor.showDeprecated": true,
    "editor.showFoldingControls": "always",
    "editor.showUnused": true,
    "editor.smoothScrolling": true,
    "editor.suggest.preview": true,
    "editor.suggest.shareSuggestSelections": false,
    "editor.suggest.showStatusBar": true,
    "editor.tabSize": 2,
    "editor.codeActionsOnSave": {
        "source.fixAll": "never",
        "source.fixAll.eslint": "never"
    },
    "diffEditor.codeLens": true,
    // Python Configurations
    // =====================
    "python.terminal.activateEnvironment": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.insertSpaces": true,
        "editor.tabSize": 4,
        "editor.formatOnSave": false,
        "editor.wordBasedSuggestions": "off"
    },
    "workbench.editor.tabActionLocation": "left"
}
```

## Code Workspaces

VSCode will read files in `.vscode/` (at the project's root) with a file extension of `.code-workspace` as a "workspace configuration." You can define settings in a `.code-workspace` files, like language settings or animations, and when VSCode loads the workspace, it will apply the configuration found in the file.

**Note**: `.code-workspace` configurations only apply when you open the file as a workspace. You can open the file in VSCode as if you were editing it and use the "Open Workspace" button in the bottom right of the VSCode window to open the workspace, or from the command pallette (`CTRL+SHIFT+P`) and search for: `File: Open Workspace from File`.

### Example code workspace

```code-workspace title="Example VSCode .code-workspace file" linenums="1"
{
    "folders": [
        // Workspace directories are JSON arrays with a `"path"` and `"name"` param.
        // `"name"` is optional, but you must provice a `"path"`.
        // {
        //   "path": "../",
        //   "name": "Git Root"
        // }
    ],
    "settings": {
        // ========================
        // Workbench Configurations
        // ========================
        "workbench.editor.labelFormat": "medium",
        "workbench.editor.highlightModifiedTabs": true,
        "workbench.editor.limit.enabled": true,
        "workbench.editor.limit.excludeDirty": true,
        "workbench.editor.limit.perEditorGroup": true,
        "workbench.editor.limit.value": 12,
        "workbench.editor.preferHistoryBasedLanguageDetection": true,
        "workbench.editor.pinnedTabSizing": "shrink",
        "workbench.editor.restoreViewState": true,
        "workbench.editor.revealIfOpen": true,
        "workbench.editor.scrollToSwitchTabs": true,
        "workbench.editor.showTabs": "multiple",
        "workbench.editor.sharedViewState": true,
        "workbench.editor.tabCloseButton": "left",
        "workbench.editor.tabSizing": "shrink",
        "workbench.editor.wrapTabs": true,
        // =====================
        // Editor Configurations
        // =====================
        "editor.acceptSuggestionOnEnter": "smart",
        "editor.autoClosingBrackets": "always",
        "editor.autoClosingQuotes": "always",
        "editor.autoIndent": "advanced",
        "editor.autoSurround": "languageDefined",
        "editor.codeLens": true,
        "editor.colorDecorators": true,
        "editor.comments.insertSpace": true,
        "editor.cursorSmoothCaretAnimation": "on",
        "editor.cursorStyle": "block",
        "editor.cursorSurroundingLines": 8,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.detectIndentation": true,
        "editor.find.addExtraSpaceOnTop": true,
        "editor.find.autoFindInSelection": "multiline",
        "editor.find.cursorMoveOnType": false,
        "editor.find.loop": true,
        "editor.find.seedSearchStringFromSelection": "selection",
        "editor.folding": true,
        "editor.foldingHighlight": true,
        "editor.foldingStrategy": "auto",
        "editor.fontFamily": "Consolas, 'Courier New', monospace",
        "editor.fontLigatures": true,
        "editor.fontSize": 14,
        "editor.fontWeight": "normal",
        "editor.formatOnPaste": true,
        "editor.formatOnSaveMode": "modificationsIfAvailable",
        "editor.formatOnSave": true,
        "editor.guides.bracketPairs": "active",
        "editor.guides.bracketPairsHorizontal": "active",
        "editor.guides.highlightActiveBracketPair": true,
        "editor.guides.highlightActiveIndentation": "always",
        "editor.guides.indentation": true,
        "editor.inlayHints.enabled": "onUnlessPressed",
        "editor.inlineSuggest.enabled": true,
        "editor.largeFileOptimizations": true,
        "editor.linkedEditing": true,
        "editor.links": true,
        "editor.matchBrackets": "always",
        "editor.minimap.scale": 2,
        "editor.mouseWheelZoom": true,
        "editor.multiCursorMergeOverlapping": true,
        "editor.multiCursorModifier": "alt",
        "editor.occurrencesHighlight": "singleFile",
        "editor.overviewRulerBorder": true,
        "editor.parameterHints.enabled": true,
        "editor.parameterHints.cycle": true,
        "editor.quickSuggestions": {
            "other": "on",
            "comments": "off",
            "strings": "off"
        },
        "editor.rename.enablePreview": true,
        "editor.roundedSelection": true,
        "editor.selectionHighlight": true,
        "editor.semanticHighlighting.enabled": "configuredByTheme",
        "editor.showDeprecated": true,
        "editor.showFoldingControls": "always",
        "editor.showUnused": true,
        "editor.smoothScrolling": true,
        "editor.suggest.preview": true,
        "editor.suggest.shareSuggestSelections": false,
        "editor.suggest.showStatusBar": true,
        "editor.tabSize": 2,
        "editor.codeActionsOnSave": {
            "source.fixAll": "never",
            "source.fixAll.eslint": "never"
        },
        "diffEditor.codeLens": true,
        // Python Configurations
        // =====================
        "python.terminal.activateEnvironment": true,
        "[python]": {
            "editor.insertSpaces": true,
            "editor.tabSize": 4,
            "editor.formatOnSave": true,
            "editor.wordBasedSuggestions": "off"
        },
        "workbench.editor.tabActionLocation": "left"
    }
}
```
