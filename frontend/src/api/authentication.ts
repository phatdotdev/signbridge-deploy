// authApi.ts
import axiosClient from "./axiosClient";
import type { Result } from "./validators";

export type User = {
  id?: number;
  username: string;
  email: string;
  password?: string;
  gender: string;
  birthdate: string;
  role: string;
  created_at?: Date;
};

export const signup = async (userData: User): Promise<Result<User>> => {
  try {
    const res = await axiosClient.post("/users", userData);
    return {
      ok: true,
      data: res.data,
    };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail,
    };
  }
};

export const login = async (
  username: string,
  password: string
): Promise<Result<string>> => {
  try {
    const res = await axiosClient.post("/auth/login", { username, password });

    return { ok: true, data: res.data };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail,
    };
  }
};

export const introspect = async (): Promise<Result<string>> => {
  try {
    const res = await axiosClient.post("/auth/introspect");
    return { ok: true, data: res.data };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail || "Introspect failed.",
    };
  }
};

export const getCurrentUser = async (): Promise<Result<User>> => {
  await authentication();
  try {
    const res = await axiosClient.get("/users/me");
    return { ok: true, data: res.data };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail,
    };
  }
};

export const refreshToken = async (): Promise<Result<string>> => {
  console.log("Acess token has expired. Try to refresh token.");
  try {
    const res = await axiosClient.post("/auth/refresh");
    return { ok: true, data: res.data };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail || "refresh failed.",
    };
  }
};

export const logout = async (): Promise<Result<{ message: string }>> => {
  try {
    const res = await axiosClient.post("/auth/logout");
    return { ok: true, data: res.data };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail || "logout failed.",
    };
  }
};

export const authentication = async () => {
  try {
    const res = await introspect();
    if (!res.ok) {
      await refreshToken();
    }
  } catch (err) {
    console.error("Authentication error:", err);
    throw err;
  }
};
