import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Header } from './Header';
import { TabProvider } from '../contexts/TabContext';

describe('Header', () => {
  it('renders the header', () => {
    render(
      <TabProvider>
        <Header />
      </TabProvider>
    );
    expect(screen.getByText('OBS Styla')).toBeInTheDocument();
  });
});
