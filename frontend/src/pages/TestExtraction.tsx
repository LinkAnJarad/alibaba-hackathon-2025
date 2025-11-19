import { useState, useEffect } from "react";
import { api } from "../lib/api";

interface ExtractedFields {
  [key: string]: any;
}

interface Sample {
  name: string;
  size: number;
  type: string;
}

export default function TestExtraction() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExtractedFields | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [selectedSample, setSelectedSample] = useState<string>("");

  useEffect(() => {
    loadSamples();
  }, []);

  const loadSamples = async () => {
    try {
      const res = await api.get("/test/list-samples");
      setSamples(res.data.samples || []);
    } catch (err) {
      console.error("Failed to load samples:", err);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      
      const res = await api.post("/test/extract-upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      setResult(res.data.extracted_fields);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Extraction failed");
    } finally {
      setLoading(false);
    }
  };

  const handleTestSample = async () => {
    if (!selectedSample) return;
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await api.post("/test/extract-sample", {
        test_file: selectedSample,
      });
      
      setResult(res.data.extracted_fields);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Extraction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Test Document Extraction (Qwen VL)</h1>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Upload Section */}
        <div className="border rounded-lg p-4">
          <h2 className="font-semibold mb-3">Upload Document</h2>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm mb-3"
          />
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 w-full"
          >
            {loading ? "Extracting..." : "Upload & Extract"}
          </button>
        </div>

        {/* Test Sample Section */}
        <div className="border rounded-lg p-4">
          <h2 className="font-semibold mb-3">Test with Sample</h2>
          <select
            value={selectedSample}
            onChange={(e) => setSelectedSample(e.target.value)}
            className="border rounded w-full p-2 mb-3"
          >
            <option value="">-- Select Sample --</option>
            {samples.map((s) => (
              <option key={s.name} value={s.name}>
                {s.name} ({(s.size / 1024).toFixed(1)} KB)
              </option>
            ))}
          </select>
          <button
            onClick={handleTestSample}
            disabled={!selectedSample || loading}
            className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 w-full"
          >
            {loading ? "Extracting..." : "Extract Sample"}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-800 font-semibold">Error:</p>
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded">
          <h3 className="font-semibold text-lg mb-3">Extracted Fields:</h3>
          
          {result.error ? (
            <div className="text-red-600">
              <p className="font-semibold">Extraction Error:</p>
              <p>{result.error}</p>
            </div>
          ) : result.raw_text ? (
            <div>
              <p className="text-sm text-gray-600 mb-2">Raw AI Response:</p>
              <pre className="bg-white p-3 rounded border text-sm overflow-auto">
                {result.raw_text}
              </pre>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 gap-3">
              {Object.entries(result).map(([key, value]) => (
                <div key={key} className="border-b pb-2">
                  <span className="text-sm text-gray-600 font-medium">
                    {key.replace(/_/g, " ").toUpperCase()}:
                  </span>
                  <p className="text-gray-900">
                    {value !== null && value !== undefined ? String(value) : "N/A"}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded text-sm">
        <p className="font-semibold mb-2">How to test:</p>
        <ol className="list-decimal list-inside space-y-1">
          <li>Upload an ID card, birth certificate, or any document image</li>
          <li>Or select a sample from <code className="bg-white px-1 rounded">backend/test_data</code></li>
          <li>Click extract to see Qwen VL extract the information</li>
          <li>Add your own test images to <code className="bg-white px-1 rounded">backend/test_data</code> folder</li>
        </ol>
        <p className="mt-3 text-xs text-gray-600">
          Model: <strong>qwen-vl-max</strong> (configurable in ai_service.py)
        </p>
      </div>
    </div>
  );
}
