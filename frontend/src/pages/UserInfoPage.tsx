import { useAuth } from "../context/AuthContext";

export default function UserInfoPage() {
  const { userInfo: user } = useAuth();

  if (!user || Object.keys(user).length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-lg text-slate-500">
          Loading or no user information available...
        </p>
      </div>
    );
  }

  const renderInfoCard = (label: string, value: any, icon: string) => {
    if (!value) return null;

    let displayValue = value;

    if (label === "Birthdate" || label === "Created At") {
      const date = new Date(value);
      displayValue = date.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });
    }

    return (
      <div className="flex items-start gap-4 p-4 bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition">
        <div className="text-2xl text-indigo-500">{icon}</div>
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
            {label}
          </p>
          <p className="text-base font-medium text-slate-800 break-words">
            {displayValue}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50/40 to-indigo-100/30 px-4 py-12">
      <div className="max-w-2xl w-full bg-white/80 backdrop-blur-md rounded-3xl shadow-xl border border-slate-100 p-8 sm:p-10">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-tr from-indigo-600 to-cyan-500 rounded-full shadow-lg mb-4">
            <span className="text-4xl text-white">👤</span>
          </div>
          <h2 className="text-3xl font-bold text-slate-800">
            User Information
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Your account details on the system
          </p>
        </div>

        {/* Info Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {renderInfoCard("Username", user.username, "🆔")}
          {renderInfoCard("Email", user.email, "📧")}
          {renderInfoCard("Gender", user.gender, "🚻")}
          {renderInfoCard("Birthdate", user.birthdate, "🎂")}
          {renderInfoCard("Role", user.role, "🛡️")}
          {renderInfoCard("Created At", user.created_at, "🗓️")}
        </div>

        {/* Note */}
        <div className="mt-10 text-center text-sm text-slate-500 italic">
          The edit profile feature is coming soon.
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-400 mt-8">
          © 2025 Sign Bridge - VOYA Team
        </p>
      </div>
    </div>
  );
}
