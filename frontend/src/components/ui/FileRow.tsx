import React from 'react';
import { FileCode, FileText, Image as ImageIcon, Music, Database, File } from 'lucide-react';
import type { WorkspaceFile } from '../../types';

interface FileRowProps {
  file: WorkspaceFile;
  isSelected?: boolean;
  onSelect?: (file: WorkspaceFile) => void;
}

export const FileRow: React.FC<FileRowProps> = ({ file, isSelected, onSelect }) => {
  const getIcon = (type: WorkspaceFile['type']) => {
    switch (type) {
      case 'code':
        return <FileCode className="w-4 h-4 text-cyan-600" />;
      case 'document':
        return <FileText className="w-4 h-4 text-blue-600" />;
      case 'image':
        return <ImageIcon className="w-4 h-4 text-emerald-600" />;
      case 'audio':
        return <Music className="w-4 h-4 text-amber-600" />;
      case 'data':
        return <Database className="w-4 h-4 text-indigo-600" />;
      default:
        return <File className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <tr
      onClick={() => onSelect?.(file)}
      className={`group cursor-pointer text-xs transition-colors border-b border-slate-100 ${
        isSelected
          ? 'bg-cyan-50/80 text-cyan-950 font-medium'
          : 'hover:bg-slate-50/80 text-slate-700'
      }`}
    >
      <td className="px-5 py-3.5 font-medium">
        <div className="flex items-center space-x-3">
          {getIcon(file.type)}
          <span className="font-sans text-slate-900 truncate">{file.name}</span>
        </div>
      </td>
      <td className="px-5 py-3.5 text-slate-500 font-mono text-[11px] truncate max-w-xs">{file.path}</td>
      <td className="px-5 py-3.5 text-slate-500 capitalize">{file.type}</td>
      <td className="px-5 py-3.5 text-slate-500 font-mono text-[11px]">{file.size}</td>
      <td className="px-5 py-3.5 text-slate-500 text-[11px]">{file.lastModified}</td>
      <td className="px-5 py-3.5 text-right">
        {file.isIndexed ? (
          <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            Indexed
          </span>
        ) : (
          <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200">
            Pending
          </span>
        )}
      </td>
    </tr>
  );
};
