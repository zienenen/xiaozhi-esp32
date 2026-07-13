import { createContext, ReactNode, useContext, useMemo, useState } from "react";
import { api, setBasicAuth } from "./api";

export type DemoRole = "factory_admin" | "project_admin" | "tester" | "viewer";
type AuthValue = { role: DemoRole | null; login: (role: DemoRole, username: string, password: string) => Promise<void>; logout: () => void; canManage: boolean; canSimulate: boolean };

const AuthContext = createContext<AuthValue | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<DemoRole | null>(null);
  const value = useMemo<AuthValue>(() => ({
    role,
    async login(nextRole, username, password) {
      setBasicAuth(username, password);
      try { await api.get("/demo/overview"); setRole(nextRole); }
      catch (error) { setBasicAuth(); throw error; }
    },
    logout() { setBasicAuth(); setRole(null); },
    canManage: role === "factory_admin" || role === "project_admin",
    canSimulate: role === "factory_admin" || role === "tester"
  }), [role]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("AuthProvider is missing");
  return value;
}
