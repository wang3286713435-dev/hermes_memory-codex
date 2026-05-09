'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const STATE_FILE = path.join(ROOT, '.claude', 'context', 'runtime', 'ralph-state.json');
const PROMPT_FILE = path.join(ROOT, '.claude', 'ralph', 'PROMPT.md');
const COMPLETION_SIGNAL =
  process.env.RALPH_COMPLETION_SIGNAL || 'RALPH_AUDIT_COMPLETE_NO_FINDINGS';
const PROGRESS_SIGNAL = /RALPH_ITERATION_COMPLETE:\s*(\d+)\s+findings?\s+remain/i;

function allow() {
  process.exit(0);
}

function readStdin() {
  return new Promise((resolve) => {
    let input = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => {
      input += chunk;
    });
    process.stdin.on('end', () => resolve(input));
    process.stdin.on('error', () => resolve(input));
  });
}

function loadJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return fallback;
  }
}

function clearState() {
  try {
    fs.unlinkSync(STATE_FILE);
  } catch {
    // Missing state already means no active loop.
  }
}

function blockWithPrompt(state, prompt) {
  const maxIterations = state.maxIterations || Number(process.env.RALPH_MAX_ITERATIONS || 25);
  const header = [
    `Ralph loop iteration ${state.iteration}/${maxIterations}.`,
    'Continue the same mission. Read guardrails, inspect findings, fix only in scope, then rerun validation.',
  ].join('\n');

  process.stdout.write(
    JSON.stringify({
      decision: 'block',
      reason: `${header}\n\n${prompt}`,
    })
  );
  process.exit(0);
}

async function main() {
  if (process.env.RALPH_ACTIVE !== '1') {
    allow();
  }

  const rawTranscript = await readStdin();
  const transcript = loadJsonFromString(rawTranscript);

  if (transcript && transcript.stop_hook_active) {
    allow();
  }

  if (!fs.existsSync(STATE_FILE)) {
    allow();
  }

  const assistantText =
    readAssistantTranscriptText(transcript) ||
    extractText(transcript?.message?.content ?? transcript?.content ?? transcript?.text);
  if (assistantText.includes(COMPLETION_SIGNAL)) {
    clearState();
    allow();
  }

  const state = loadJson(STATE_FILE, {});
  const now = new Date().toISOString();
  const maxIterations = Number(process.env.RALPH_MAX_ITERATIONS || state.maxIterations || 25);
  const circuitBreakerThreshold = Number(process.env.RALPH_CIRCUIT_BREAKER_THRESHOLD || 3);
  const progressMatch = assistantText.match(PROGRESS_SIGNAL);
  const findingsCount = progressMatch ? Number(progressMatch[1]) : null;

  state.iteration = Number(state.iteration || 0) + 1;
  state.startedAt = state.startedAt || now;
  state.lastRunAt = now;
  state.maxIterations = maxIterations;

  if (findingsCount !== null) {
    if (state.lastFindingsCount === findingsCount) {
      state.unchangedFindingsStreak = Number(state.unchangedFindingsStreak || 0) + 1;
    } else {
      state.unchangedFindingsStreak = 0;
    }
    state.lastFindingsCount = findingsCount;
  }

  if (state.iteration >= maxIterations) {
    clearState();
    allow();
  }

  if (Number(state.unchangedFindingsStreak || 0) >= circuitBreakerThreshold) {
    clearState();
    allow();
  }

  if (!fs.existsSync(PROMPT_FILE)) {
    clearState();
    allow();
  }

  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, `${JSON.stringify(state, null, 2)}\n`);
  blockWithPrompt(state, fs.readFileSync(PROMPT_FILE, 'utf8'));
}

function loadJsonFromString(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function readAssistantTranscriptText(input) {
  const transcriptPath = input && (input.transcript_path || input.transcriptPath);
  if (!transcriptPath || !fs.existsSync(transcriptPath)) {
    return '';
  }

  const assistantMessages = [];
  const lines = fs.readFileSync(transcriptPath, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    if (!line.trim()) continue;
    const event = loadJsonFromString(line);
    if (!event) continue;

    const role = event.role || event.type || event.message?.role;
    if (role !== 'assistant') continue;

    const text = extractText(event.message?.content ?? event.content ?? event.text);
    if (text) assistantMessages.push(text);
  }

  return assistantMessages.join('\n');
}

function extractText(value) {
  if (!value) return '';
  if (typeof value === 'string') return value;
  if (Array.isArray(value)) {
    return value
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item && typeof item.text === 'string') return item.text;
        if (item && item.type === 'text' && typeof item.content === 'string') return item.content;
        return '';
      })
      .filter(Boolean)
      .join('\n');
  }
  if (typeof value.text === 'string') return value.text;
  return '';
}

main().catch(() => allow());
