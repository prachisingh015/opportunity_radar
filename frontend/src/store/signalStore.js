import { create } from 'zustand'

export const useSignalStore = create((set) => ({
  alerts: [],
  setAlerts: (alerts) => set({ alerts }),
  addAlert: (alert) => set((state) => ({ alerts: [alert, ...state.alerts] })),
  clearAlerts: () => set({ alerts: [] }),
}))
