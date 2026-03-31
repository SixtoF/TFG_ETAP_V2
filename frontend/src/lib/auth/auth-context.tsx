"use client";

import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { meRequest, loginRequest, MeResponse } from "@/lib/api/auth";
import { getToken, removeToken, saveToken } from "./token-storage";

type AuthContextType = {
  user: MeResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<MeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    removeToken();
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    const token = getToken();

    if (!token) {
      setUser(null);
      return;
    }

    try {
      const currentUser = await meRequest();
      setUser(currentUser);
    } catch {
      removeToken();
      setUser(null);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await loginRequest({ email, password });
    saveToken(response.access_token);

    const currentUser = await meRequest();
    setUser(currentUser);
  }, []);

  useEffect(() => {
    const bootstrapAuth = async () => {
      try {
        await refreshUser();
      } finally {
        setIsLoading(false);
      }
    };

    bootstrapAuth();
  }, [refreshUser]);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
      refreshUser,
    }),
    [user, isLoading, login, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}