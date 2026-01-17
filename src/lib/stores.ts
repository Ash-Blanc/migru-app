import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// --- Types ---

export type StatusType = 'Balanced' | 'Prodromal' | 'Attack' | 'Postdromal';

export interface LogEntry {
  id: string;
  date: string;
  type: 'attack' | 'relief' | 'checkin';
  severity?: number; // 1-10
  symptoms?: string[];
  notes?: string;
}

export interface AppState {
  status: {
    current: StatusType;
    hrv: string; // e.g. "45ms"
    lastCheck: string; // ISO date
  };
  forecast: {
    riskLevel: 'Low' | 'Moderate' | 'High';
    pressureTrend: 'Rising' | 'Steady' | 'Falling';
    humidity: number;
  };
  logs: LogEntry[];
}

export interface UserSettings {
  theme: string;
  notifications: {
    hydration: boolean;
    barometer: boolean;
    sleep: boolean;
  };
  profile: {
    name: string;
    email: string;
  };
}

// --- Helpers ---

function createPersistedStore<T>(key: string, startValue: T) {
  const saved = browser ? localStorage.getItem(key) : null;
  const initial = saved ? JSON.parse(saved) : startValue;
  const store = writable<T>(initial);

  if (browser) {
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }
  return store;
}

export const themes = ['light', 'dark', 'sunset', 'nord', 'abyss'];

// --- Settings Store ---

const defaultSettings: UserSettings = {
  theme: 'light',
  notifications: {
    hydration: true,
    barometer: true,
    sleep: false
  },
  profile: {
    name: 'Sarah',
    email: 'sarah@example.com'
  }
};

export const settings = createPersistedStore<UserSettings>('migru-settings', defaultSettings);

// Settings side-effects (theme application)
if (browser) {
  settings.subscribe((value) => {
    document.documentElement.setAttribute('data-theme', value.theme);
  });
}

// --- App State Store ---

const defaultAppState: AppState = {
  status: {
    current: 'Balanced',
    hrv: '65ms',
    lastCheck: new Date().toISOString()
  },
  forecast: {
    riskLevel: 'Moderate',
    pressureTrend: 'Falling',
    humidity: 45
  },
  logs: []
};

export const appState = createPersistedStore<AppState>('migru-app-state', defaultAppState);

// --- Actions ---

export function addLog(entry: Omit<LogEntry, 'id' | 'date'>) {
  appState.update(state => {
    const newEntry: LogEntry = {
      ...entry,
      id: crypto.randomUUID(),
      date: new Date().toISOString()
    };
    return { ...state, logs: [newEntry, ...state.logs] };
  });
}

export function updateStatus(status: StatusType) {
  appState.update(state => ({
    ...state,
    status: { ...state.status, current: status, lastCheck: new Date().toISOString() }
  }));
}
