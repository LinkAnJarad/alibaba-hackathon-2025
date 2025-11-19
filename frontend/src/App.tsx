import { Route, Routes, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import SubmitForm from "./pages/SubmitForm";
import AdminReview from "./pages/AdminReview";
import TestExtraction from "./pages/TestExtraction";
import TestPdfAutoFill from "./pages/TestPdfAutoFill";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/submit" element={<SubmitForm />} />
        <Route path="/admin/review" element={<AdminReview />} />
        <Route path="/test/extract" element={<TestExtraction />} />
        <Route path="/test/pdf-autofill" element={<TestPdfAutoFill />} />
      </Routes>
    </Layout>
  );
}
