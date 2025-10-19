import React, { useContext, useState } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

const ListItem = ({ children, active }: { children: React.ReactNode, active?: boolean }) => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;
  const [hovered, setHovered] = useState(false);

  const style = {
    backgroundColor: active ? colors.list_active_selection_background : 'transparent',
    color: active ? colors.list_active_selection_text : colors.ui_text,
  };

  const hoverStyle = {
    backgroundColor: colors.list_hover_background,
  };

  return (
    <li
      style={hovered ? { ...style, ...hoverStyle } : style}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {children}
    </li>
  );
};

export default ListItem;
