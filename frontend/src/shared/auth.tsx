import { createContext, ReactNode, useContext, useMemo, useState } from "react";

export type DemoRole = "factory_admin" | "project_admin" | "tester" | "viewer";
type AuthValue = { role: DemoRole | null; login: (role: DemoRole) => void; logout: () => void; canManage: boolean; canSimulate: boolean };

const AuthContext = createContext<AuthValue | null>(null);
const storageKey = "blindbox_demo_role";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<DemoRole | null>(() => sessionStorage.getItem(storageKey) as DemoRole | null);
  const value = useMemo<AuthValue>(() => ({
    role,
    login(nextRole) { sessionStorage.setItem(storageKey, nextRole); setRole(nextRole); },
    logout() { sessionStorage.removeItem(storageKey); setRole(null); },
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
