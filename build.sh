#!/usr/bin/env bash
set -o errexit
set -o pipefail

# ====== CRITICAL FIXES ======
# 1. Use Render's explicit Python path (matches runtime environment)
PYTHON_PATH="/opt/render/project/src/.venv/bin/python"
PIP_PATH="/opt/render/project/src/.venv/bin/pip"
export PATH="/opt/render/project/src/.venv/bin:$PATH"

# 2. Clean environment
echo "--- CLEANING PREVIOUS INSTALLS ---"
rm -rf ~/.cache/pip || true
pip cache purge || true

# 3. Core setup
echo "--- UPGRADING PIP/WHEEL ---"
$PIP_PATH install --upgrade pip==24.0 wheel==0.43.0 setuptools==68.2.2

# 4. Install ALL dependencies (including Gunicorn)
echo "--- INSTALLING REQUIREMENTS ---"
$PIP_PATH install --no-cache-dir -r requirements.txt

# 5. VERIFY GUNICORN EXPLICITLY
echo "--- VERIFYING GUNICORN INSTALL ---"
$PYTHON_PATH -c "
import gunicorn
print(f'GUNICORN VERIFIED: {gunicorn.__version__}')
" || { echo "!!! GUNICORN NOT FOUND !!!"; exit 1; }

# 6. Django setup
echo "--- DJANGO SETUP ---"
$PYTHON_PATH manage.py collectstatic --noinput || echo "Collectstatic warning (continuing)"
$PYTHON_PATH manage.py migrate

echo "+++ BUILD SUCCESSFUL +++"