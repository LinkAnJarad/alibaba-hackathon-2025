import { useState } from "react";
import Upload from "../components/Upload";
import { api } from "../lib/api";

export default function SubmitForm() {
  const [documentUrl, setDocumentUrl] = useState<string | null>(null);
  const [fields, setFields] = useState<Record<string, string> | null>(null);

  const runExtract = async () => {
    if (!documentUrl) return;
    const res = await api.post("/ai/extract", { document_url: documentUrl });
    setFields(res.data.fields);
  };

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">Submit a Form</h1>
      <div className="space-y-4">
        <Upload onUploaded={setDocumentUrl} />
        {documentUrl && (
          <div className="flex items-center gap-2">
            <span className="text-sm">Uploaded: {documentUrl}</span>
            <button onClick={runExtract} className="px-3 py-2 bg-green-600 text-white rounded">
              Auto-fill with AI
            </button>
          </div>
        )}
        {fields && (
          <div className="border rounded p-4">
            <h2 className="font-semibold mb-2">Extracted Fields</h2>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(fields).map(([k, v]) => (
                <label key={k} className="text-sm">
                  <span className="block text-gray-600">{k}</span>
                  <input defaultValue={v} className="border rounded w-full p-2" />
                </label>
              ))}
            </div>
            <button className="mt-3 px-3 py-2 bg-blue-600 text-white rounded">Submit</button>
          </div>
        )}
      </div>
    </div>
  );
}
