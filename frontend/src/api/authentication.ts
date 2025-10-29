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

export type LoginResponse = {
  message: string;
  access_token: string;
  refresh_token: string;
};

export const signup = async (userData: User): Promise<Result<User>> => {
  try {
    const res = await axiosClient.post("/users", userData);
    return { ok: true, data: res.data };
  } catch (error: any) {
    return { ok: false, error: error.response?.data?.detail };
  }
};

export const login = async (
  username: string,
  password: string
): Promise<Result<LoginResponse>> => {
  try {
    const res = await axiosClient.post("/auth/login", { username, password });

    // Lưu token vào localStorage
    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("refresh_token", res.data.refresh_token);

    return { ok: true, data: res.data };
  } catch (error: any) {
    return { ok: false, error: error.response?.data?.detail };
  }
};

export const refreshToken = async (): Promise<Result<string>> => {
  console.log("Access token has expired. Trying to refresh...");
  try {
    const refresh_token = localStorage.getItem("refresh_token");
    const res = await axiosClient.post("/auth/refresh", { refresh_token });

    localStorage.setItem("access_token", res.data.access_token);
    return { ok: true, data: res.data.access_token };
  } catch (error: any) {
    return {
      ok: false,
      error: error.response?.data?.detail || "Refresh failed.",
    };
  }
};

export const getCurrentUser = async (): Promise<Result<User>> => {
  await authentication();
  try {
    const token = localStorage.getItem("access_token");
    const res = await axiosClient.get("/users/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return { ok: true, data: res.data };
  } catch (error: any) {
    return { ok: false, error: error.response?.data?.detail };
  }
};

export const logout = async (): Promise<Result<{ message: string }>> => {
  // Xóa token khỏi localStorage
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  return { ok: true, data: { message: "Logged out successfully" } };
};

export const authentication = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No access token");

    // Gọi introspect để kiểm tra token
    try {
      await axiosClient.post("/auth/introspect", { access_token: token });
    } catch {
      await refreshToken();
    }
  } catch (err) {
    console.error("Authentication error:", err);
    throw err;
  }
};
