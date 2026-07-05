import { useState } from "react";
import { PROJECT_FILES, ProjectFile } from "../data/code_files";
import { File, Folder, FolderOpen, Copy, Check, Search } from "lucide-react";

export function CodeExplorer() {
  const [selectedFile, setSelectedFile] = useState<ProjectFile>(PROJECT_FILES[0]);
  const [copied, setCopied] = useState(false);
  const [search, setSearch] = useState("");

  const handleCopy = () => {
    navigator.clipboard.writeText(selectedFile.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const filteredFiles = PROJECT_FILES.filter(
    (file) =>
      file.name.toLowerCase().includes(search.toLowerCase()) ||
      file.path.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div id="code-explorer" className="grid grid-cols-1 lg:grid-cols-12 gap-6 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
      {/* File Tree Panel */}
      <div className="lg:col-span-4 bg-slate-950/80 p-5 border-r border-slate-800 flex flex-col h-[550px]">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Project Structure</h3>
          <span className="text-xs bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded-full font-mono">
            Python 3.12
          </span>
        </div>

        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search code files..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-900 text-slate-200 pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-800 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </div>

        {/* Mock File System Hierarchy */}
        <div className="flex-1 overflow-y-auto space-y-1 font-mono text-xs text-slate-400">
          {/* Bot Root Folder */}
          <div className="flex items-center gap-2 text-slate-300 py-1 font-semibold">
            <FolderOpen className="h-4 w-4 text-yellow-500" />
            <span>bot_root /</span>
          </div>

          <div className="pl-4 space-y-1">
            {/* Database Folder */}
            <div className="flex items-center gap-2 text-slate-300 py-1">
              <Folder className="h-3.5 w-3.5 text-yellow-500" />
              <span>database /</span>
            </div>
            <div className="pl-4 space-y-1 border-l border-slate-800">
              {filteredFiles
                .filter((f) => f.path.includes("database/"))
                .map((file) => (
                  <button
                    key={file.path}
                    onClick={() => setSelectedFile(file)}
                    className={`flex items-center gap-2 w-full text-left px-2 py-1.5 rounded transition-all ${
                      selectedFile.path === file.path
                        ? "bg-cyan-500/10 text-cyan-400 font-medium"
                        : "hover:bg-slate-900 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <File className="h-3.5 w-3.5" />
                    <span className="truncate">{file.name}</span>
                  </button>
                ))}
            </div>

            {/* Other root files */}
            {filteredFiles
              .filter((f) => !f.path.includes("database/") && f.path.split("/").length <= 2)
              .map((file) => (
                <button
                  key={file.path}
                  onClick={() => setSelectedFile(file)}
                  className={`flex items-center gap-2 w-full text-left px-2 py-1.5 rounded transition-all ${
                    selectedFile.path === file.path
                      ? "bg-cyan-500/10 text-cyan-400 font-medium"
                      : "hover:bg-slate-900 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <File className="h-3.5 w-3.5" />
                  <span className="truncate">{file.name}</span>
                </button>
              ))}
          </div>
        </div>
      </div>

      {/* Code Viewer Panel */}
      <div className="lg:col-span-8 flex flex-col h-[550px] bg-slate-950">
        {/* Header Toolbar */}
        <div className="bg-slate-900/60 px-5 py-3 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-slate-400">{selectedFile.path}</span>
          </div>

          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-slate-400 hover:text-cyan-400 hover:bg-slate-800 rounded-lg transition-all"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" />
                <span>Copy Code</span>
              </>
            )}
          </button>
        </div>

        {/* Code Content */}
        <div className="flex-1 overflow-auto p-5 font-mono text-[11px] sm:text-xs leading-relaxed text-slate-300 select-all">
          <pre className="whitespace-pre">
            {selectedFile.code.split("\n").map((line, idx) => (
              <div key={idx} className="flex hover:bg-slate-900/40 py-0.5 rounded px-1 transition-colors">
                <span className="w-8 text-slate-600 select-none text-right pr-3 border-r border-slate-800/80 mr-3">
                  {idx + 1}
                </span>
                <span className="flex-1">{line}</span>
              </div>
            ))}
          </pre>
        </div>
      </div>
    </div>
  );
}
