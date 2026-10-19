#!/bin/bash
# Installs Blender 5.2 (the bpy module from PyPI) for headless asset conversion.
# Run scripts with: blender5 script.py [args]
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

BPY_VERSION=5.2.2
VENV=/opt/blender5

if ! "$VENV/bin/python" -c "import bpy,sys; sys.exit(bpy.app.version_string.split()[0] != '$BPY_VERSION')" 2>/dev/null; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q "bpy==$BPY_VERSION"
fi

cat > /usr/local/bin/blender5 <<'LAUNCHER'
#!/bin/sh
# Blender 5.2 (bpy module). Usage: blender5 script.py [args...]
exec /opt/blender5/bin/python "$@"
LAUNCHER
chmod +x /usr/local/bin/blender5
