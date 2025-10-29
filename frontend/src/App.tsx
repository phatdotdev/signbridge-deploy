import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Layout from "./components/Layout";
import { Suspense, lazy } from "react";
import LabelsPage from "./pages/LabelsPage";
import JobsPage from "./pages/JobsPage";
import SamplesPage from "./pages/SamplesPage";
import LoginPage from "./pages/LoginPage";
import { AuthProvider } from "./context/AuthContext";
import SignupPage from "./pages/SignupPage";
import AdminRoutes from "./components/AdminRoutes";
import UserInfoPage from "./pages/UserInfoPage";

// const DashboardPage = lazy(() => import("./components/dashboard/AnalyticsOverview"));
// const LabelsPage = lazy(() => import("./pages/LabelsPage"));
const UploadPage = lazy(() => import("./pages/UploadPage"));
// const JobsPage = lazy(() => import("./pages/JobsPage"));
// const SamplesPage = lazy(() => import("./pages/SamplesPage"));

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Suspense fallback={<div className="p-6">Loading...</div>}>
            <Routes>
              <Route element={<AdminRoutes />}>
                <Route path="/dashboard" />
                <Route path="/labels" element={<LabelsPage />} />
                <Route path="/jobs" element={<JobsPage />} />
                <Route path="/samples" element={<SamplesPage />} />
              </Route>
              {/* <Route path="/dashboard" element={<DashboardPage />} /> */}

              <Route path="/upload" element={<UploadPage />} />
              <Route path="/" element={<Navigate to="/upload" />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/me" element={<UserInfoPage />} />
            </Routes>
          </Suspense>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App;
