#!/usr/bin/env node
const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🚀 Starting Crewlyze Setup...');

const projectRoot = path.resolve(__dirname, '..');
const venvDir = path.join(projectRoot, '.venv');
const requirementsPath = path.join(projectRoot, 'requirements.txt');
const mainPyPath = path.join(projectRoot, 'main.py');

// 1. Check if Python is installed
let pythonCmd = 'python3';
try {
  execSync('python3 --version', { stdio: 'ignore' });
} catch (e) {
  try {
    execSync('python --version', { stdio: 'ignore' });
    pythonCmd = 'python';
  } catch (err) {
    console.error('❌ Error: Python 3 is not installed or not in PATH.');
    process.exit(1);
  }
}

// 2. Create virtual environment if it doesn't exist
if (!fs.existsSync(venvDir)) {
  console.log(`📦 Creating Python virtual environment in ${venvDir}...`);
  execSync(`${pythonCmd} -m venv .venv`, { cwd: projectRoot, stdio: 'inherit' });
}

const pipCmd = process.platform === 'win32'
  ? path.join(venvDir, 'Scripts', 'pip')
  : path.join(venvDir, 'bin', 'pip');

const uvicornCmd = process.platform === 'win32'
  ? path.join(venvDir, 'Scripts', 'uvicorn')
  : path.join(venvDir, 'bin', 'uvicorn');

// 3. Install dependencies
console.log('📦 Installing Python dependencies... This may take a moment.');
execSync(`"${pipCmd}" install -r requirements.txt`, { cwd: projectRoot, stdio: 'inherit' });

// 4. Start the server
console.log('🚀 Starting Crewlyze server...');
const serverProcess = spawn(uvicornCmd, ['main:app', '--host', '127.0.0.1', '--port', '8000', '--reload'], {
  cwd: projectRoot,
  stdio: 'inherit'
});

serverProcess.on('close', (code) => {
  console.log(`Server exited with code ${code}`);
});
