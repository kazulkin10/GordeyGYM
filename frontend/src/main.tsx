import React from 'react'
import ReactDOM from 'react-dom/client'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { BrowserRouter } from 'react-router-dom'
import App from './App'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0b5ed7'
    },
    secondary: {
      main: '#0abf88'
    }
  },
  typography: {
    fontFamily: 'Inter, Roboto, sans-serif'
  }
})

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter basename="/GordeyGYM">
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
)
