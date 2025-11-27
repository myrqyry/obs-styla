import React from 'react';

const ListItem = ({ children, active }: { children: React.ReactNode, active?: boolean }) => {
  return (
    <li className={`py-2 px-3 rounded cursor-pointer transition-colors ${
      active
        ? 'bg-accent text-accent-foreground'
        : 'hover:bg-muted text-foreground'
    }`}>
      {children}
    </li>
  );
};

export default ListItem;
