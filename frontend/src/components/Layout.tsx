import { Link } from "react-router-dom";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 py-3 flex gap-4 items-center">
          <span className="font-bold text-lg">SmartBarangay Forms</span>
          <nav className="flex gap-4 text-sm">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/submit">Submit Form</Link>
            <Link to="/admin/review">Admin Review</Link>
            <Link to="/test/extract" className="text-purple-600">Test AI</Link>
            <Link to="/test/pdf-autofill" className="text-pink-600">PDF Auto-Fill</Link>
            <Link to="/login" className="ml-auto">Login</Link>
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-6xl mx-auto w-full px-4 py-6">{children}</main>
      <footer className="border-t bg-white text-center text-xs py-4">© {new Date().getFullYear()} Barangay eGov</footer>
    </div>
  );
}
