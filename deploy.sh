#!/bin/bash

# Quick Deploy Script for GitHub
# Usage: ./deploy.sh "commit message"

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting deployment...${NC}"

# Check if commit message provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Please provide a commit message${NC}"
    echo "Usage: ./deploy.sh \"your commit message\""
    exit 1
fi

COMMIT_MSG="$1"
BRANCH=$(git branch --show-current)

echo -e "${BLUE}📝 Current branch: ${BRANCH}${NC}"
echo -e "${BLUE}💬 Commit message: ${COMMIT_MSG}${NC}"

# Add all changes
echo -e "${BLUE}📦 Adding files...${NC}"
git add .

# Commit
echo -e "${BLUE}💾 Committing...${NC}"
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

# Push
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
git push -u origin $BRANCH

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Your app is live at:${NC}"
echo -e "${GREEN}   https://cdn.jsdelivr.net/gh/irapad/hospital@${BRANCH}/calculator.html${NC}"
