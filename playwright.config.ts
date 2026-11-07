import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: /e2e\/.*\.spec\.ts|unit\/.*\.test\.ts/,
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 180000,
  expect: { timeout: 10000 },
  reporter: [['list']],
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    launchOptions: { args: ['--no-sandbox', '--disable-dev-shm-usage'] },
    trace: 'off',
  },
  webServer: {
    command: 'python3 -m http.server 3000',
    cwd: '.',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 60000,
  },
});