import { useState } from "react";
import { api } from "../lib/api";

export default function Upload({ onUploaded }: { onUploaded: (url: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    const res = await api.post("/uploads/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setLoading(false);
    onUploaded(res.data.url);
  };

  return (
    <div className="border rounded p-4">
      <input
        type="file"
        accept="image/*,application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="block mb-2"
      />
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="px-3 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}
