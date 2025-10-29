import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import Button from "../components/ui/Button";
// Giả định bạn có một hàm `signup` trong file authentication.ts để gọi API đăng ký
import { signup, type User } from "../api/authentication";

// Giới tính cho dropdown
const GENDER_OPTIONS = [
  { value: "male", label: "Nam" },
  { value: "female", label: "Nữ" },
  { value: "other", label: "Khác" },
];

export default function SignupPage() {
  // State cho các trường input
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [gender, setGender] = useState("male");
  const [birthdate, setBirthdate] = useState("");

  // State cho UI
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (password !== confirmPassword) {
      setError("Mật khẩu và Mật khẩu xác nhận không khớp.");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError("Mật khẩu phải có ít nhất 6 ký tự.");
      setLoading(false);
      return;
    }

    const userData: User = {
      username,
      email,
      password,
      gender,
      role: "user",
      birthdate: birthdate.toString(),
    };

    try {
      console.log(userData);
      const response = await signup(userData);
      console.log("Signup response:", response);
      navigate("/login", {
        state: {
          message: "Đăng ký tài khoản thành công! Vui lòng đăng nhập.",
        },
      });
    } catch (err: any) {
      console.error("Signup error:", err);

      if (err.response?.status === 409) {
        setError("Tên đăng nhập hoặc Email đã tồn tại.");
      } else if (err.response?.status === 500) {
        setError("Lỗi máy chủ. Vui lòng thử lại sau.");
      } else {
        setError(err instanceof Error ? err.message : "Đăng ký thất bại");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20 px-4 py-8">
      <div className="max-w-xl w-full">
        {/* Logo/Brand */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-indigo-500 to-cyan-500 rounded-2xl shadow-lg shadow-indigo-500/25 mb-4">
            <span className="text-3xl">🤟</span>
          </div>
          <h1 className="text-3xl font-bold text-slate-800 mb-2">
            Tạo Tài Khoản Mới
          </h1>
          <p className="text-slate-600">
            Hệ thống thu thập dữ liệu ngôn ngữ ký hiệu
          </p>
        </div>

        {/* Signup Form Container */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-200/50 p-8">
          <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">
            Đăng ký
          </h2>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-start">
              <svg
                className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Tên đăng nhập & Email */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Tên đăng nhập */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Tên đăng nhập
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Tên đăng nhập"
                  required
                />
              </div>
              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="example@voya.com"
                  required
                />
              </div>
            </div>

            {/* Mật khẩu */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Mật khẩu */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Mật khẩu
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Mật khẩu (ít nhất 6 ký tự)"
                  required
                />
              </div>
              {/* Xác nhận Mật khẩu */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Xác nhận Mật khẩu
                </label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Nhập lại mật khẩu"
                  required
                />
              </div>
            </div>

            {/* Giới tính & Ngày sinh */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Giới tính */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Giới tính
                </label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all appearance-none bg-white"
                  required
                >
                  {GENDER_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
              {/* Ngày sinh */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Ngày sinh
                </label>
                <input
                  type="date"
                  value={birthdate}
                  onChange={(e) => setBirthdate(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-500 to-cyan-500 text-white py-3 rounded-lg font-medium shadow-lg shadow-indigo-500/25 hover:shadow-xl hover:shadow-indigo-500/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-6"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Đang đăng ký...
                </span>
              ) : (
                "Hoàn tất Đăng ký"
              )}
            </Button>
          </form>

          {/* Login Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-slate-600">
              Đã có tài khoản?{" "}
              <Link
                to="/login"
                className="text-indigo-600 hover:text-indigo-700 font-medium transition-colors"
              >
                Đăng nhập ngay
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-slate-600 mt-6">
          © 2025 Sign Bridge - VOYA Team
        </p>
      </div>
    </div>
  );
}
