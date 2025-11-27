import React, { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';

const ThemeExporter = () => {
  const { state } = useContext(ThemeContext);
  const { metadata, colors } = state;

  const generateOVT = () => {
    const themeVariables = Object.entries(colors)
      .map(([key, value]) => `    --${key}: ${value};`)
      .join('\n');

    const ovtTemplate = `
@OBSThemeMeta {
    name: '${metadata.name}';
    id: '${metadata.id}';
    extends: '${metadata.extends}';
    author: '${metadata.author}';
    dark: '${metadata.dark}';
}

@OBSThemeVars {
${themeVariables}
}

/* Add custom QSS rules here */
`;
    return ovtTemplate;
  };

  const handleExport = () => {
    const ovtContent = generateOVT();
    const blob = new Blob([ovtContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${metadata.id}.ovt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Export Theme</h3>
      <button
        onClick={handleExport}
        className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
      >
        Export .ovt File
      </button>
    </div>
  );
};

export default ThemeExporter;
