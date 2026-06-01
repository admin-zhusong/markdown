#!/bin/bash
#
# Auto Update Script for Markdown Editor
# This script pulls the latest code from GitHub and updates the deployed service.
#
# Usage: ./auto_update.sh
#

set -e

# ==================== Configuration ====================
REPO_URL="git@github.com:admin-zhusong/markdown.git"
PROJECT_DIR="/opt/markdown_work"
VENV_DIR="${PROJECT_DIR}/venv"
SERVICE_NAME="markdown_work"
LOG_FILE="/var/log/markdown_update.log"

# ==================== Logging ====================
log() {
    echo "[$(date "+%Y-%m-%d %H:%M:%S")] $1" | tee -a "${LOG_FILE}"
}

log "========================================="
log "Starting Markdown Editor update process"
log "========================================="

# ==================== Step 1: Pull Latest Code ====================
log "Step 1/6: Pulling latest code from GitHub..."
cd "${PROJECT_DIR}"

# Ensure remote is set correctly
git remote set-url origin "${REPO_URL}" 2>/dev/null || true

# Stash any local changes to avoid conflicts
git stash 2>/dev/null || true

# Pull latest code
if git pull origin main; then
    log "  -> Code pulled successfully."
else
    log "  -> ERROR: Failed to pull code from GitHub!"
    exit 1
fi

# ==================== Step 2: Update Dependencies ====================
log "Step 2/6: Updating Python dependencies..."
if ${VENV_DIR}/bin/pip install -r "${PROJECT_DIR}/requirements.txt" --quiet; then
    log "  -> Dependencies updated successfully."
else
    log "  -> WARNING: Some dependencies may not have been updated."
fi

# Ensure urllib3 compatibility with older OpenSSL
${VENV_DIR}/bin/pip install "urllib3<2" "requests<2.32" --quiet 2>/dev/null || true

# ==================== Step 3: Run Database Migrations ====================
log "Step 3/6: Running database migrations..."
if ${VENV_DIR}/bin/python "${PROJECT_DIR}/manage.py" migrate --noinput; then
    log "  -> Migrations applied successfully."
else
    log "  -> ERROR: Database migrations failed!"
    exit 1
fi

# ==================== Step 4: Collect Static Files ====================
log "Step 4/6: Collecting static files..."
if ${VENV_DIR}/bin/python "${PROJECT_DIR}/manage.py" collectstatic --noinput 2>/dev/null; then
    log "  -> Static files collected successfully."
else
    log "  -> WARNING: Static file collection had issues (non-critical)."
fi

# ==================== Step 5: Restart Service ====================
log "Step 5/6: Restarting markdown service..."
if systemctl restart "${SERVICE_NAME}"; then
    log "  -> Service restarted successfully."
else
    log "  -> ERROR: Failed to restart service!"
    exit 1
fi

# ==================== Step 6: Verify Service ====================
log "Step 6/6: Verifying service health..."
sleep 2

if systemctl is-active --quiet "${SERVICE_NAME}"; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ 2>/dev/null || echo "000")
    if [ "${HTTP_CODE}" = "200" ]; then
        log "  -> Service is healthy! HTTP ${HTTP_CODE}"
    else
        log "  -> WARNING: Service is running but returned HTTP ${HTTP_CODE}"
    fi
else
    log "  -> ERROR: Service is not running!"
    systemctl status "${SERVICE_NAME}" --no-pager 2>&1 | tee -a "${LOG_FILE}"
    exit 1
fi

log "========================================="
log "Update completed successfully!"
log "========================================="
