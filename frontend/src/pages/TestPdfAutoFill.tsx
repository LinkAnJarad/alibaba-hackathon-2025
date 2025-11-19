import { useState } from "react";
import { api } from "../lib/api";

interface MappingField {
  field: string;
  value: string;
}

interface Mapping {
  type: string;
  field?: string;
  value?: string;
  fields?: MappingField[];
  form_mapping: {
    type: string;
    field?: string;
    value?: string;
    fields?: MappingField[];
  };
}

interface AutoFillResult {
  filled_pdf_path: string;
  extracted_data: Record<string, any>;
  mappings: Mapping[];
  filled_fields: Record<string, any>;
  missing_fields: string[];
  message: string;
}

export default function TestPdfAutoFill() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [documentFile, setDocumentFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AutoFillResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [manualFields, setManualFields] = useState<Record<string, string>>({});

  const handleAutoFill = async () => {
    if (!pdfFile || !documentFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("pdf_form", pdfFile);
      formData.append("document", documentFile);

      const res = await api.post("/test/pdf/auto-fill", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
      
      // Initialize manual fields for missing fields
      const missing = res.data.missing_fields || [];
      const initialManual: Record<string, string> = {};
      missing.forEach((field: string) => {
        initialManual[field] = "";
      });
      setManualFields(initialManual);
      
    } catch (err: any) {
      setError(err.response?.data?.detail || "Auto-fill failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!result?.filled_pdf_path) return;

    try {
      const filename = result.filled_pdf_path.split(/[\\/]/).pop();
      const response = await api.get(`/test/pdf/download/${filename}`, {
        responseType: "blob",
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `filled_form_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err: any) {
      setError("Failed to download PDF");
    }
  };

  const updateManualField = (field: string, value: string) => {
    setManualFields(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Test PDF Auto-Fill (Qwen AI + PyPDFForm)</h1>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* PDF Form Upload */}
        <div className="border rounded-lg p-4">
          <h2 className="font-semibold mb-3">1. Upload PDF Form</h2>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
            className="block w-full text-sm"
          />
          {pdfFile && (
            <p className="text-xs text-green-600 mt-1">✓ {pdfFile.name}</p>
          )}
        </div>

        {/* Document Upload */}
        <div className="border rounded-lg p-4">
          <h2 className="font-semibold mb-3">2. Upload Document (ID, etc.)</h2>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setDocumentFile(e.target.files?.[0] || null)}
            className="block w-full text-sm"
          />
          {documentFile && (
            <p className="text-xs text-green-600 mt-1">✓ {documentFile.name}</p>
          )}
        </div>
      </div>

      {/* Auto-Fill Button */}
      <button
        onClick={handleAutoFill}
        disabled={!pdfFile || !documentFile || loading}
        className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg font-semibold disabled:opacity-50 mb-6"
      >
        {loading ? "Processing..." : "🤖 Auto-Fill PDF with AI"}
      </button>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-800 font-semibold">Error:</p>
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Success Message */}
          <div className="p-4 bg-green-50 border border-green-200 rounded">
            <p className="text-green-800 font-semibold">✓ {result.message}</p>
          </div>

          {/* Extracted Data */}
          <div className="border rounded-lg p-4">
            <h3 className="font-semibold mb-3">Extracted from Document:</h3>
            <div className="grid md:grid-cols-2 gap-2 text-sm">
              {Object.entries(result.extracted_data).map(([key, value]) => (
                <div key={key} className="border-b pb-1">
                  <span className="text-gray-600">{key}:</span>{" "}
                  <span className="font-medium">{String(value)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Field Mappings */}
          {result.mappings.length > 0 && (
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-3">AI Field Mappings:</h3>
              <div className="space-y-2 text-sm">
                {result.mappings.map((mapping, idx) => (
                  <div key={idx} className="p-2 bg-gray-50 rounded">
                    {mapping.type === "single" ? (
                      <div>
                        <span className="font-medium text-blue-600">{mapping.field}</span>
                        {" → "}
                        {mapping.form_mapping.type === "multiple" ? (
                          <span>
                            {mapping.form_mapping.fields?.map(f => f.field).join(", ")}
                          </span>
                        ) : (
                          <span className="font-medium text-green-600">
                            {mapping.form_mapping.field}
                          </span>
                        )}
                      </div>
                    ) : (
                      <div>
                        <span>
                          {mapping.fields?.map(f => f.field).join(" + ")}
                        </span>
                        {" → "}
                        <span className="font-medium text-green-600">
                          {mapping.form_mapping.field}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Filled Fields */}
          <div className="border rounded-lg p-4">
            <h3 className="font-semibold mb-3">✓ Auto-Filled Fields ({Object.keys(result.filled_fields).length}):</h3>
            <div className="grid md:grid-cols-3 gap-2 text-sm">
              {Object.entries(result.filled_fields).map(([field, value]) => (
                <div key={field} className="p-2 bg-green-50 rounded">
                  <div className="text-gray-600 text-xs">{field}</div>
                  <div className="font-medium">{String(value)}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Missing Fields - Manual Input */}
          {result.missing_fields.length > 0 && (
            <div className="border border-yellow-300 rounded-lg p-4 bg-yellow-50">
              <h3 className="font-semibold mb-3 text-yellow-800">
                ⚠️ Missing Fields ({result.missing_fields.length}) - Please Fill Manually:
              </h3>
              <div className="grid md:grid-cols-2 gap-3">
                {result.missing_fields.map((field) => (
                  <div key={field}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {field}
                    </label>
                    <input
                      type="text"
                      value={manualFields[field] || ""}
                      onChange={(e) => updateManualField(field, e.target.value)}
                      className="border rounded w-full p-2 text-sm"
                      placeholder={`Enter ${field}`}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Download Button */}
          <button
            onClick={handleDownloadPdf}
            className="w-full px-4 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700"
          >
            📥 Download Filled PDF
          </button>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded text-sm">
        <p className="font-semibold mb-2">How it works:</p>
        <ol className="list-decimal list-inside space-y-1">
          <li>Upload a fillable PDF form template</li>
          <li>Upload a document image (ID, birth certificate, etc.)</li>
          <li>AI extracts data from the document using Qwen VL</li>
          <li>AI maps extracted fields to PDF form fields using Qwen reasoning</li>
          <li>PDF is auto-filled with available data</li>
          <li>Missing fields are shown for manual input</li>
          <li>Download the completed PDF</li>
        </ol>
        <p className="mt-3 text-xs text-gray-600">
          <strong>AI Models:</strong> qwen-vl-max (extraction) + qwen-plus (mapping)
        </p>
      </div>
    </div>
  );
}
