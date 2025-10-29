import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AdminRoutes = () => {
  const redirect = useNavigate();
  const { userInfo } = useAuth();
  useEffect(() => {
    if (!userInfo?.role || userInfo?.role !== "admin") {
      redirect("/");
    }
  }, []);
  return <Outlet />;
};

export default AdminRoutes;
