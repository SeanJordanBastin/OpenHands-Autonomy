task: Fix Vite React UI for Chat Agent
goals:
  - Detect if src/App.jsx is still showing the Vite boilerplate
  - Ensure src/components/ChatAgentUI.jsx exists and is correctly implemented
  - Automatically replace App.jsx with one that renders ChatAgentUI
  - Auto-create ChatAgentUI.jsx if missing
  - Retry frontend and confirm localhost:5173 renders chat UI
  - If any file is broken or malformed, ask ChatGPT to regenerate it
  - Backup existing versions before overwriting

steps:
  - run: echo "🔍 Checking App.jsx for Vite boilerplate"
  - run: grep "Vite" src/App.jsx || echo "✅ No Vite boilerplate found"
  - run: |
      if grep -q "Vite" src/App.jsx; then
        echo "🛠 Replacing App.jsx with ChatAgentUI import"
        echo 'import React from "react";
import ChatAgentUI from "./components/ChatAgentUI";
function App() {
  return <ChatAgentUI />;
}
export default App;' > src/App.jsx
      fi
  - run: echo "📁 Checking ChatAgentUI.jsx existence"
  - run: |
      if [ ! -f src/components/ChatAgentUI.jsx ]; then
        echo "❗ ChatAgentUI.jsx missing, asking GPT for regeneration"
        # fallback to ChatGPT fix
        curl -X POST http://localhost:3001/api/gpt/fix \
          -H "Content-Type: application/json" \
          -d '{"file": "ChatAgentUI.jsx", "purpose": "React component for chat UI", "fallback": true}'
      else
        echo "✅ ChatAgentUI.jsx exists"
      fi
  - run: echo "💾 Backing up original files"
  - run: |
      mkdir -p fixed_backups
      cp src/App.jsx fixed_backups/App_backup.jsx || true
      cp src/components/ChatAgentUI.jsx fixed_backups/ChatAgentUI_backup.jsx || true
  - run: echo "🚀 Restarting frontend"
  - run: npm run dev
  - run: echo "🔁 Checking if frontend renders chat interface"
  - run: curl -s http://localhost:5173 | grep -q "Say something" && echo "✅ Chat UI is live" || echo "❌ Chat UI not detected"

