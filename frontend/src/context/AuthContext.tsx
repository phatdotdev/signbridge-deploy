import {
  createContext,
  useState,
  useEffect,
  useContext,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  login as loginApi,
  logout as logoutApi,
  type User,
} from "../api/authentication";

import type { Result } from "../api/validators";

interface AuthContextType {
  userInfo: User | null;
  setUserInfo: (userInfo: User | null) => void;
  isLoading: boolean;
  isAuthenticated: boolean;

  login: (username: string, password: string) => Promise<Result<User>>;

  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

// COMPONENT PROVIDER

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [userInfo, setUserInfo] = useState<User | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadUser = async () => {
      const result = await getCurrentUser();

      if (result.ok) {
        setUserInfo(result.data);
        console.log("Session restored successfully.");
      } else {
        setUserInfo(null);
        console.log(
          "Could not load User Info, user is not logged in or session has expired."
        );
      }

      setIsLoading(false);
    };

    loadUser();
  }, []);

  // login handler
  const login = async (
    username: string,
    password: string
  ): Promise<Result<User>> => {
    const loginResult = await loginApi(username, password);

    if (loginResult.ok) {
      const userResult = await getCurrentUser();

      if (userResult.ok) {
        setUserInfo(userResult.data);
        return { ok: true, data: userResult.data };
      }

      return {
        ok: false,
        error: userResult.error || "Can not get user info.",
      };
    }

    return { ok: false, error: loginResult.error };
  };

  // logout handler
  const logout = async (): Promise<void> => {
    const result = await logoutApi();

    if (!result.ok) {
      console.error("An error occurred when logout.", result.error);
    }

    setUserInfo(null);
  };

  const value: AuthContextType = {
    userInfo,
    login,
    logout,
    setUserInfo,
    isLoading,
    isAuthenticated: !!userInfo,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// CUSTOM HOOK useAuth

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
